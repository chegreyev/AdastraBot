from aiogram import types
from aiogram.dispatcher import FSMContext

from config import bot, dp


@dp.callback_query_handler(state='*')
async def test(callback: types.CallbackQuery):
    print(callback.data)