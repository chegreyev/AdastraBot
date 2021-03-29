import os
import json
import pytz
import requests
from datetime import datetime
from dotenv import load_dotenv

from utils.tools import order_weekdays, sort_weekdays_by_today

load_dotenv()
API_URL = os.getenv('API_URL')

async def authorizeManager(data: dict):
    responce = requests.post(
        url=API_URL+'users/managers/login/',
        data={
            'chat_id': data['chat_id'],
            'email': data['email'],
            'password': data['password']
        }
    )

    data = json.loads(responce.text)
    if data['detail'] == 'wrong password':
        return 'Неверный пароль'
    elif data['detail'] == 'wrong email':
        return 'Такого пользователя не существует'
    elif data['detail'] == 'success':
        return 'Вы успешно авторизовались'

async def getConfirmationCode(chat_id):
    responce = requests.post(
        url=API_URL+'users/managers/generate_code/',
        data={
            'chat_id': chat_id
        }
    )
    data = json.loads(responce.text)
    return data['detail']

async def activateCode(code: str, chat_id: str):
    responce = requests.post(
        url=API_URL+'users/teachers/activate_code/',
        data={
            'chat_id': chat_id,
            'code': code
        }
    )
    data = json.loads(responce.text)
    if data['detail'] == 'Code is not exists':
        return 'Такого кода не существует'
    elif data['detail'] == 'Code is approved':
        return 'Ваш код подтвержден'

async def getDays(chat_id) -> list:
    today = datetime.now(pytz.timezone("Asia/Almaty"))
    response = requests.post(
        url=API_URL+'users/managers/available_days/',
        data={
            'chat_id': chat_id,
        }
    )
    data = json.loads(response.text)
    working_days = order_weekdays(data['detail'])
    sorted_days = sort_weekdays_by_today(working_days, today)
    return sorted_days

async def getHours(chat_id, date) -> list:
    response = requests.post(
        url=API_URL+'users/managers/available_time/',
        data={
            'chat_id': chat_id,
            'date': date,
        }
    )
    data = json.loads(response.text)
    return data['detail']

async def getInterviewDays() -> list:
    today = datetime.now(pytz.timezone("Asia/Almaty"))
    response = requests.post(
        url=API_URL + 'users/managers/available_interview_days/',
    )
    data = json.loads(response.text)
    working_days = order_weekdays(data['detail'])
    sorted_days = sort_weekdays_by_today(working_days, today)
    return sorted_days

async def getInterviewHours(date) -> list:
    response = requests.post(
        url=API_URL + 'users/managers/available_interview_time/',
        data={
            'date': date,
        }
    )
    data = json.loads(response.text)
    return data['detail']

async def registerDemoLesson(data: dict):
    responce = requests.post(
        url=API_URL + 'users/teachers/register_demo_lesson/',
        data=data
    )
    data = json.loads(responce.text)

async def postponeDemoLesson(chat_id, reserve_id, change_time = True):
    responce = requests.post(
        url=API_URL + 'users/managers/cancel_bid/',
        data={
            'chat_id': chat_id,
            'reserve_id': reserve_id,
            'change_time': change_time
        }
    )

async def confirmDemoLesson(chat_id, reserve_id):
    responce = requests.post(
        url=API_URL + 'users/managers/confirm_bid/',
        data={
            'chat_id': chat_id,
            'reserve_id': reserve_id,
        }
    )

async def registerInterview(data: dict):
    responce = requests.post(
        url=API_URL + 'users/managers/register_interview/',
        data=data
    )
    data = json.loads(responce.text)

async def postponeInterview(chat_id, reserve_id, change_time = True):
    responce = requests.post(
        url=API_URL + 'users/managers/cancel_interview/',
        data={
            'chat_id': chat_id,
            'reserve_id': reserve_id,
            'change_time': change_time
        }
    )

async def confirmInterview(chat_id, reserve_id):
    responce = requests.post(
        url==API_URL + 'users/managers/confirm_interview/',
        data={
            'chat_id': chat_id,
            'reserve_id': reserve_id,
        }
    )
