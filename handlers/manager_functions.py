from aiogram import types
from aiogram.utils.markdown import markdown_decoration as md
from aiogram.dispatcher import FSMContext

from config import bot, dp
from utils.api import (
    getConfirmationCode,
    postponeDemoLesson,
    confirmDemoLesson,
    postponeInterview,
    confirmInterview,
)


@dp.message_handler(lambda m: m.text == 'Сгенерировать код')
async def send_confirmation_code(message: types.Message):
    chat_id = message.chat.id
    code = await getConfirmationCode(chat_id)
    if code == 'no access':
        await message.answer('Вы не можете сгенерировать пароль, так как вы не зарегестрированы.')
    else:
        text = md.code(code)
        await message.answer(text, parse_mode=types.ParseMode.MARKDOWN_V2)

@dp.callback_query_handler(lambda c: c.data in [
    'postpone_bid_from_manager',
    'cancel_bid_from_manager',
    'confirm_bid_from_manager',
], state='*')
async def process_bid_handler(callback: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )

    if callback.data == 'postpone_bid_from_manager':

        reserve_id = callback.message.text.split('\n')[0].split('-')[0][1:]
        chat_id = callback.message.chat.id
        await postponeDemoLesson(chat_id, reserve_id)
        await callback.message.answer('Учитель будет оповещен, резерв был удален!')

    elif callback.data == 'cancel_bid_from_manager':

        reserve_id = callback.message.text.split('\n')[0].split('-')[0][1:]
        chat_id = callback.message.chat.id
        await postponeDemoLesson(chat_id, reserve_id, change_time=False)
        await callback.message.answer('Заявка отклонена, Учитель будет уведомлен!')

    else:
        reserve_id = callback.message.text.split('\n')[0].split('-')[0][1:]
        chat_id = callback.message.chat.id
        await confirmDemoLesson(chat_id, reserve_id)

@dp.callback_query_handler(lambda c: c.data in [
    'postpone_interview_from_manager',
    'cancel_interview_from_manager',
    'confirm_interview_from_manager',
], state='*')
async def process_interview_handler(callback: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )

    if callback.data == 'postpone_interview_from_manager':

        reserve_id = callback.message.text.split('\n')[0].split('-')[0][1:]
        chat_id = callback.message.chat.id
        await postponeInterview(chat_id, reserve_id)
        await callback.message.answer('Учитель будет оповещен, резерв был удален!')

    elif callback.data == 'cancel_interview_from_manager':

        reserve_id = callback.message.text.split('\n')[0].split('-')[0][1:]
        chat_id = callback.message.chat.id
        await postponeInterview(chat_id, reserve_id, change_time=False)
        await callback.message.answer('Интервью отклонено, Учитель будет уведомлен!')

    else:
        reserve_id = callback.message.text.split('\n')[0].split('-')[0][1:]
        chat_id = callback.message.chat.id
        await confirmInterview(chat_id, reserve_id)
