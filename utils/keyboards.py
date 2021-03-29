from aiogram import types
from aiogram.dispatcher import FSMContext

from utils.consts import (
    GRADES, CALLBACK_GRADES,
    LANGUAGES, CALLBACK_LANGUAGES,
    LEVELS, CALLBACK_LEVELS,
)


# Manager authorization keyboard
async def getManagerLoginKeyboard() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton(text='Изменить email', callback_data='change_manager_email'),
        types.InlineKeyboardButton(text='Изменить password', callback_data='change_manager_password'),
        types.InlineKeyboardButton(text='Авторизоваться', callback_data='authorize_manager')
    )
    return keyboard

# Manager post authorization Menu keyboard
async def getManagerMenuKeyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(
        types.KeyboardButton(text='Сгенерировать код')
    )
    return keyboard

# Teacher initial keyboard
async def getTeacherTypeKeyboard() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("Учитель", callback_data="teacher"),
        types.InlineKeyboardButton("Демо Учитель", callback_data="demo_teacher")
    )
    return keyboard

# Teacher subject keyboard
async def getTeacherSubjectKeyboard() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text="Физ/Мат", callback_data="fizmat"),
        types.InlineKeyboardButton(text="Английский", callback_data="english")
    )
    return keyboard

# Dynamic keyboard for Grades
async def configureKeyboardForGrades(state: FSMContext) -> types.InlineKeyboardMarkup:
    data = await state.get_data()
    state_grades = data['subject_grades'].split(', ')
    state_grades_length = len(state_grades)

    keyboard = types.InlineKeyboardMarkup(row_width=state_grades_length)
    for grade in GRADES:
        if grade in state_grades:
            continue
        keyboard.add(
            types.InlineKeyboardButton(
                text=CALLBACK_GRADES[grade]['text'],
                callback_data=CALLBACK_GRADES[grade]['data']
            )
        )

    return keyboard

# Dynamic keyboard for Languages
async def configureKeyboardForLanguages(state: FSMContext) -> types.InlineKeyboardMarkup:
    data = await state.get_data()
    state_languages = data['subject_languages'].split(', ')
    state_languages_length = len(state_languages)

    keyboard = types.InlineKeyboardMarkup(row_width=state_languages_length)
    for language in LANGUAGES:
        if language in state_languages:
            continue
        elif language == 'confirm':
            if data['subject'] == 'fizmat':
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=CALLBACK_LANGUAGES[language]['text'],
                        callback_data=CALLBACK_LANGUAGES[language]['data'][0]
                    )
                )
                continue
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=CALLBACK_LANGUAGES[language]['text'],
                        callback_data=CALLBACK_LANGUAGES[language]['data'][1]
                    )
                )
                continue
        keyboard.add(
            types.InlineKeyboardButton(
                text=CALLBACK_LANGUAGES[language]['text'],
                callback_data=CALLBACK_LANGUAGES[language]['data']
            )
        )

    return keyboard

# Dynamic keyboard for Levels
async def configureKeyboardForLevels(state: FSMContext) -> types.InlineKeyboardMarkup:
    data = await state.get_data()
    state_levels = data['subject_levels'].split(', ')
    state_levels_length = len(state_levels)

    keyboard = types.InlineKeyboardMarkup(row_width=state_levels_length)
    for level in LEVELS:
        if level in state_levels:
            continue
        keyboard.add(
            types.InlineKeyboardButton(
                text=CALLBACK_LEVELS[level]['text'],
                callback_data=CALLBACK_LEVELS[level]['data']
            )
        )

    return keyboard
