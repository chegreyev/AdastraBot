from aiogram import types
from aiogram.utils.markdown import markdown_decoration as md
from aiogram.dispatcher import FSMContext

from config import bot, dp
from utils.keyboards import getManagerLoginKeyboard, getManagerMenuKeyboard
from utils.api import authorizeManager
from states import ManagerStart


# Registration to Bot from Manager
@dp.message_handler(commands='register_manager')
async def register_manager_handler(message: types.Message):
    await ManagerStart.email.set()
    await message.answer('Введите email:')


@dp.message_handler(state=ManagerStart.email)
async def register_manager_email_handler(message: types.Message, state: FSMContext):
    await ManagerStart.password.set()
    await state.update_data(email=message.text)

    await message.answer('Введите пароль:')

@dp.message_handler(state=ManagerStart.password)
async def register_manager_password_handler(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton(text='Изменить email', callback_data='change_manager_email'),
        types.InlineKeyboardButton(text='Изменить password', callback_data='change_manager_password'),
        types.InlineKeyboardButton(text='Авторизоваться', callback_data='authorize_manager')
    )
    await check_credentials(message, state)

@dp.callback_query_handler(lambda c: c.data in [
    'change_manager_email',
    'change_manager_password',
    'authorize_manager',
], state='*')
async def process_register_manager(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'change_manager_email':
        await ManagerStart.change_email.set()
        await callback.message.edit_text('Введите email:')

        @dp.message_handler(state=ManagerStart.change_email)
        async def change_manager_email_handler(message: types.Message, state: FSMContext):
            await state.update_data(email=message.text)
            await check_credentials(message, state)

    elif callback.data == 'change_manager_password':
        await ManagerStart.change_password.set()
        await callback.message.edit_text('Введите пароль:')

        @dp.message_handler(state=ManagerStart.change_password)
        async def change_manager_password_handler(message: types.Message, state: FSMContext):
            await state.update_data(password=message.text)
            await check_credentials(message, state)

    elif callback.data == 'authorize_manager':
        data = await state.get_data()
        data['chat_id'] = callback.message.chat.id
        response_auth = await authorizeManager(data)

        if response_auth == 'Такого пользователя не существует':
            await ManagerStart.change_email.set()
            await callback.message.edit_text(response_auth + '\n' + 'Введите email:')

            @dp.message_handler(state=ManagerStart.change_email)
            async def change_manager_email_auth_handler(message: types.Message, state: FSMContext):
                await state.update_data(email=message.text)
                await check_credentials(message, state)

        elif response_auth == 'Неверный пароль':
            await ManagerStart.change_password.set()
            await callback.message.edit_text(response_auth + '\n' + 'Введите пароль:')

            @dp.message_handler(state=ManagerStart.change_password)
            async def change_manager_password_auth_handler(message: types.Message, state: FSMContext):
                await state.update_data(password=message.text)
                await check_credentials(message, state)

        else:
            await state.finish()
            keyboard = await getManagerMenuKeyboard()

            await bot.delete_message(callback.message.chat.id, callback.message.message_id)
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text='Вы успешно авторизовались!',
                reply_markup=keyboard
            )

async def check_credentials(message: types.Message, state: FSMContext):

    data = await state.get_data()

    keyboard = await getManagerLoginKeyboard()

    await message.answer(
        text=f'Ваши данные:\n📬: {data["email"]}\n🔓: {data["password"]}',
        reply_markup=keyboard
    )

