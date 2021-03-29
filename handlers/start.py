from aiogram import types
from aiogram.dispatcher import FSMContext

from config import bot, dp
from utils.api import activateCode
from utils.keyboards import getTeacherTypeKeyboard
from states import Start, Teacher

# Start message - Regular ( Teacher )
@dp.message_handler(commands='start')
async def start_handler(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='Подать заявку', callback_data='register_new_bid')
    )
    await message.answer(
        text='Добрый день. Для того, чтобы подать заявку нажмите на кнопку ниже.',
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data == 'register_new_bid')
async def register_new_bid_handler(callback: types.CallbackQuery):
    await Start.code.set()
    await callback.message.edit_text('Введите код:')

# Handling confirmation code - Teacher
@dp.message_handler(state=Start.code)
async def confirmation_code_handler(message: types.Message, state: FSMContext):
    code_resp = await activateCode(code=message.text, chat_id=message.chat.id)

    if code_resp == 'Такого кода не существует':
        await message.answer('Вы ввели неверный код\nВведите код: ')

    elif code_resp == 'Ваш код подтвержден':
        await state.finish()
        await Teacher.type.set()
        keyboard = await getTeacherTypeKeyboard()
        text = \
            f'Выберите тип учителя:\n' +\
            f'1) Учитель - проводит постоянные уроки с учениками\n' +\
            f'2) Демо учитель - проводят только пробные уроки на определение уровня ученика.'
        await message.answer(text, reply_markup=keyboard)
