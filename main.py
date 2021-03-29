from aiogram import executor

from config import dp
from handlers import *


executor.start_polling(dp, skip_updates=True)
