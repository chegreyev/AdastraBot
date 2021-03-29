from aiogram import types
from datetime import timedelta


def levelsFromCallback(callback: types.CallbackQuery) -> str:
    if callback.data == 'configure_next_level__beginner':
        return 'beginner'
    elif callback.data == 'configure_next_level__elementary':
        return 'elementary'
    elif callback.data == 'configure_next_level__pre_intermediate':
        return 'pre-intermediate'
    elif callback.data == 'configure_next_level__intermediate':
        return 'intermediate'
    else:
        return 'upper-intermediate'

def languagesFromCallback(callback: types.CallbackQuery) -> str:
    if callback.data == 'configure_next_language__kazakh':
        return 'казахский'
    elif callback.data == 'configure_next_language__russian':
        return 'русский'
    else:
        return 'английский'

def gradeFromCallback(callback: types.CallbackQuery) -> str:
    if callback.data == 'configure_next_grades__primary':
        return '1-5'
    elif callback.data == 'configure_next_grades__middle':
        return '6-9'
    else:
        return '10+'

def order_weekdays(days: list) -> list:
    ordered_weekdays = []
    for day in days:
        if day == 'Понедельник':
            ordered_weekdays.append({'name': day, 'order': 0})
        elif day == 'Вторник':
            ordered_weekdays.append({'name': day, 'order': 1})
        elif day == 'Среда':
            ordered_weekdays.append({'name': day, 'order': 2})
        elif day == 'Четверг':
            ordered_weekdays.append({'name': day, 'order': 3})
        elif day == 'Пятница':
            ordered_weekdays.append({'name': day, 'order': 4})
        elif day == 'Суббота':
            ordered_weekdays.append({'name': day, 'order': 5})
    return ordered_weekdays

def sort_weekdays_by_today(weekdays: list, today):
    sorted_weekdays = []
    weekdays_with_date = []

    for day in weekdays:
        if day['order'] >= today.weekday():
            name = f'{day["name"]}'
            sorted_weekdays.append(name)

    for day in sorted_weekdays:
        date_name = f'{day} - {today.day}.{today.month}.{today.year}'
        weekdays_with_date.append(date_name)
        today += timedelta(days=1)

    return weekdays_with_date
