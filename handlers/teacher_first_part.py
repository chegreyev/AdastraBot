from aiogram import types
from aiogram.dispatcher import FSMContext

from config import bot, dp
from utils.tools import (
    gradeFromCallback,
    languagesFromCallback,
    levelsFromCallback,
)
from utils.keyboards import (
    getTeacherSubjectKeyboard,
    configureKeyboardForGrades, # dynamic
    configureKeyboardForLanguages, # dynamic
    configureKeyboardForLevels, # dynamic
)
from utils.api import (
    getDays,
    getHours,
    registerDemoLesson,
    getInterviewDays,
    getInterviewHours,
    registerInterview,
)
from states import Teacher


# Choose Teacher type
@dp.callback_query_handler(lambda c: c.data in ['teacher', 'demo_teacher'], state=Teacher.type)
async def teacher_type_handler(callback: types.CallbackQuery, state: FSMContext):
    await Teacher.subject.set()
    await state.update_data(type=callback.data)

    keyboard = await getTeacherSubjectKeyboard()
    await callback.message.edit_text('Выберите предмет:', reply_markup=keyboard)

# Process of choosing Grades, Languages and Levels
# Grades
@dp.callback_query_handler(lambda c: c.data in ['fizmat', 'english'], state=Teacher.subject)
async def fizmat(callback: types.CallbackQuery, state: FSMContext):

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

    await Teacher.subject_grades.set()
    if callback.data in ['fizmat', 'english']:
        await state.update_data(subject = callback.data)

    keyboard = types.InlineKeyboardMarkup()
    # TODO: Refactor this
    keyboard.add(
        types.InlineKeyboardButton(text="1-5", callback_data="configure_next_grades__primary"),
        types.InlineKeyboardButton(text="6-9", callback_data="configure_next_grades__middle"),
        types.InlineKeyboardButton(text="10+", callback_data="configure_next_grades__high"),
    )

    await bot.send_message(callback.message.chat.id, "Выберите классы преподавания: ", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data in [
        'configure_next_grades__primary',
        'configure_next_grades__middle',
        'configure_next_grades__high',
    ], state = Teacher.subject_grades)
async def configure_subject_grades(callback: types.CallbackQuery, state: FSMContext):

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

    data = await state.get_data()
    try:
        # Проверяю длину пришедшего ответа от пользователя
        # -> Если ничего не пришло, значит человек ошибся с выбором и ему нужно заново запустить функцию
        # -> Если что то пришло, значит нужно дальше запускать функцию
        if len(data['subject_grades']):
            await state.update_data(subject_grades=f"{data['subject_grades']}, " + gradeFromCallback(callback) )
        else:
            await state.update_data(subject_grades=f"{gradeFromCallback(callback)}")
        data = await state.get_data()
    except KeyError:
        # Если пользователь впервые нажал на кнопку выбора класса
        await state.update_data(subject_grades=gradeFromCallback(callback))
        data = await state.get_data()

    keyboard = await configureKeyboardForGrades(state)

    await bot.send_message(callback.message.chat.id, f"Вы выбрали классы обучения: {data['subject_grades']}\nВыберете вариант из ниже перечисленных: ", reply_markup=keyboard)

# Languages
@dp.callback_query_handler(lambda c: c.data == 'confirm_grades', state = Teacher.subject_grades)
async def confirm_grades(callback: types.CallbackQuery, state: FSMContext):

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

    await Teacher.next()
    data = await state.get_data()

    keyboard = types.InlineKeyboardMarkup()
    # TODO: Refactor this
    keyboard.add(
        types.InlineKeyboardButton(text="казахский", callback_data="configure_next_language__kazakh"),
        types.InlineKeyboardButton(text="русский", callback_data="configure_next_language__russian"),
        types.InlineKeyboardButton(text="английский", callback_data="configure_next_language__english"),
    )

    await bot.send_message(callback.message.chat.id, f"Давайте выберем язык/и обучения: ", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data in [
        'configure_next_language__kazakh',
        'configure_next_language__russian',
        'configure_next_language__english',
    ], state=Teacher.subject_languages)
async def configure_subject_languages(callback: types.CallbackQuery, state: FSMContext):

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

    data = await state.get_data()
    try:
        # Проверяю длину пришедшего ответа от пользователя
        # -> Если ничего не пришло, значит человек ошибся с выбором и ему нужно заново запустить функцию
        # -> Если что то пришло, значит нужно дальше запускать функцию
        if len(data['subject_languages']):
            await state.update_data(subject_languages=f"{data['subject_languages']}, " + languagesFromCallback(callback))
        else:
            await state.update_data(subject_languages=f"{languagesFromCallback(callback)}")
        data = await state.get_data()
    except KeyError:
        # Если пользователь впервые нажал на кнопку выбора класса
        await state.update_data(subject_languages=languagesFromCallback(callback))
        data = await state.get_data()

    keyboard = await configureKeyboardForLanguages(state)

    await bot.send_message(callback.message.chat.id, f"Вы выбрали языки обучения: {data['subject_languages']}\nВыберете вариант из ниже перечисленных: ", reply_markup=keyboard)

# Levels
@dp.callback_query_handler(lambda c: c.data == 'confirm_languages__english', state = Teacher.subject_languages)
async def confirm_languages(callback: types.CallbackQuery, state: FSMContext):

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

    await Teacher.next()
    data = await state.get_data()

    keyboard = types.InlineKeyboardMarkup()
    # TODO: Refactor this
    keyboard.add(
        types.InlineKeyboardButton(text="beginner", callback_data="configure_next_level__beginner"),
        types.InlineKeyboardButton(text="elementary", callback_data="configure_next_level__elementary"),
        types.InlineKeyboardButton(text="pre-intermediate", callback_data="configure_next_level__pre_intermediate"),
        types.InlineKeyboardButton(text="intermediate", callback_data="configure_next_level__intermediate"),
        types.InlineKeyboardButton(text="upper-intermediate", callback_data="configure_next_level__upper_intermediate"),
    )

    await bot.send_message(callback.message.chat.id, f"Давайте выберем уровни преподавания: ", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data in [
        "configure_next_level__beginner",
        "configure_next_level__elementary",
        "configure_next_level__pre_intermediate",
        "configure_next_level__intermediate",
        "configure_next_level__upper_intermediate",
    ], state=Teacher.subject_levels)
async def configure_subject_levels(callback: types.CallbackQuery, state: FSMContext):

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

    data = await state.get_data()
    try:
        # Проверяю длину пришедшего ответа от пользователя
        # -> Если ничего не пришло, значит человек ошибся с выбором и ему нужно заново запустить функцию
        # -> Если что то пришло, значит нужно дальше запускать функцию
        if len(data['subject_levels']):
            await state.update_data(subject_levels=f"{data['subject_levels']}, " + levelsFromCallback(callback))
        else:
            await state.update_data(subject_levels=f"{levelsFromCallback(callback)}")
        data = await state.get_data()
    except KeyError:
        # Если пользователь впервые нажал на кнопку выбора класса
        await state.update_data(subject_levels=levelsFromCallback(callback))
        data = await state.get_data()

    keyboard = await configureKeyboardForLevels(state)

    await bot.send_message(callback.message.chat.id, f"Вы выбрали уровни обучения: {data['subject_levels']}\nВыберете вариант из ниже перечисленных: ", reply_markup=keyboard)

# Changing values of Grades, Languages, Levels
@dp.callback_query_handler(lambda c: c.data == 'change_grades', state = Teacher.subject_grades)
async def change_grades(callback: types.CallbackQuery, state: FSMContext):

    await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)
    await Teacher.previous()

    async with state.proxy() as data:
        data["subject_grades"] = ''

    # Направляет на функцию выбора классов обучения
    await fizmat(callback, state)

@dp.callback_query_handler(lambda c: c.data == 'change_languages', state = Teacher.subject_languages)
async def change_languages(callback: types.CallbackQuery, state: FSMContext):

    await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)
    await Teacher.previous()

    async with state.proxy() as data:
        data["subject_languages"] = ''

    # Направляет на функцию выбора языков обучения
    await confirm_grades(callback, state)

@dp.callback_query_handler(lambda c: c.data == 'change_levels', state = Teacher.subject_levels)
async def change_levels(callback: types.CallbackQuery, state: FSMContext):

    await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)
    await Teacher.previous()

    async with state.proxy() as data:
        data["subject_levels"] = ''

    # Направляет на функцию выбора уровня обучения
    await confirm_languages(callback, state)

# Getting request to show time slots
@dp.callback_query_handler(lambda c: c.data in [
    'confirm_languages__fizmat',
    'confirm_levels',
    'change_lesson_time'
], state='*')
async def lesson_day_handler(callback: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    await Teacher.demo_lesson_day.set()
    days = await getDays(callback.message.chat.id)

    keyboard = types.InlineKeyboardMarkup()
    for day in days:
        keyboard.add(
            types.InlineKeyboardButton(text=day, callback_data=f'configure_day_{day}')
        )

    await callback.message.answer(
        text='Выберите день пробного урока:',
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: 'configure_day_' in c.data, state=Teacher.demo_lesson_day)
async def lesson_time_handler(callback: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )

    await Teacher.demo_lesson_time.set()
    await state.update_data(demo_lesson_day=callback.data.split('configure_day_')[1])

    hours = await getHours(
        chat_id=callback.message.chat.id,
        date=callback.data.split(' - ')[1]
    )
    keyboard = types.InlineKeyboardMarkup()
    for hour in hours:
        keyboard.add(
            types.InlineKeyboardButton(text=hour, callback_data=f'configure_hour_{hour}')
        )

    await callback.message.answer(
        text=f'Выберите время пробного урока в/во {callback.data.split("configure_day_")[1]}',
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: 'configure_hour_' in c.data, state=Teacher.demo_lesson_time)
async def lesson_configure_handler(callback: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )

    await state.update_data(demo_lesson_time=callback.data.split('configure_hour_')[1])
    data = await state.get_data()

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='Изменить', callback_data='change_lesson_time'),
        types.InlineKeyboardButton(text='Отправить заявку', callback_data='confirm_lesson_time'),
    )
    text = \
        f'Ваша заявку на демо-урок:\n' +\
        f'День: {data["demo_lesson_day"]}\n' +\
        f'Время: {data["demo_lesson_time"]}'

    await callback.message.answer(
        text=text,
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data == 'confirm_lesson_time', state='*')
async def lesson_confirm_time(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data['chat_id'] = callback.message.chat.id
    await registerDemoLesson(data)
    await callback.message.answer('Ваша заявка успешно отправлена. Ожидайте ответа Менеджера!')

@dp.callback_query_handler(lambda c: c.data in ['choose_interview_date', 'change_interview_time'], state='*')
async def interview_day_handler(callback: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )

    await Teacher.interview_day.set()
    days = await getInterviewDays()

    keyboard = types.InlineKeyboardMarkup()
    for day in days:
        keyboard.add(
            types.InlineKeyboardButton(text=day, callback_data=f'configure_interview_day_{day}')
        )

    await callback.message.answer(
        text='Выберите день собеседования:',
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: 'configure_interview_day_' in c.data, state=Teacher.interview_day)
async def interview_time_handler(callback: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )

    await Teacher.interview_time.set()
    await state.update_data(interview_day=callback.data.split('configure_interview_day_')[1])

    hours = await getInterviewHours(
        date=callback.data.split(' - ')[1]
    )

    keyboard = types.InlineKeyboardMarkup()
    for hour in hours:
        keyboard.add(
            types.InlineKeyboardButton(text=hour, callback_data=f'configure_interview_hour_{hour}')
        )

    await callback.message.answer(
        text=f'Выберите время интервью в/во {callback.data.split("configure_interview_day_")[1]}',
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: 'configure_interview_hour_' in c.data, state=Teacher.interview_time)
async def interview_configure_handler(callback: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )

    await state.update_data(interview_time=callback.data.split('configure_interview_hour_')[1])
    data = await state.get_data()

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='Изменить', callback_data='change_interview_time'),
        types.InlineKeyboardButton(text='Отправить заявку', callback_data='confirm_interview_time'),
    )
    text = \
        f'Ваша заявку на интервью:\n' + \
        f'День: {data["interview_day"]}\n' + \
        f'Время: {data["interview_time"]}'

    await callback.message.answer(
        text=text,
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data == 'confirm_interview_time', state='*')
async def interview_confirm_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data['chat_id'] = callback.message.chat.id
    await registerInterview(data)
    await callback.message.answer('Ваша заявка на интервью успешно отправлена. Ожидайте ответа Менеджера!')

@dp.callback_query_handler(lambda c: c.data == 'continue_registration_after_interview', state='*')
async def continue_registration(callback: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await Teacher.fio.set()
    await callback.message.answer('Введите ваше ФИО (полностью нужно для составления документа): ')

@dp.message_handler(state=Teacher.fio)
async def fio_handler(message: types.Message, state: FSMContext):
    await Teacher.city.set()
    await state.update_data(fio=message.text)
    await message.answer('Введите город проживания: ')

@dp.message_handler(state=Teacher.city)
async def city_handler(message: types.Message, state: FSMContext):
    await Teacher.address.set()
    await state.update_data(city=message.text)
    await message.answer('Введите адресс проживания: ')

@dp.message_handler(state=Teacher.address)
async def address_handler(message: types.Message, state: FSMContext):
    await Teacher.phone_number.set()
    await state.update_data(address=message.text)
    await message.answer('Введите номер телефона: ')

@dp.message_handler(state=Teacher.phone_number)
async def phone_number_handler(message: types.Message, state: FSMContext):
    await Teacher.email.set()
    await state.update_data(phone_number=message.text)
    await message.answer('Введите адрес почты (email): ')

@dp.message_handler(state=Teacher.email)
async def email_handler(message: types.Message, state: FSMContext):
    await Teacher.iin.set()
    await state.update_data(email=message.text)
    await message.answer('Введите ИИН:')

@dp.message_handler(state=Teacher.iin)
async def iin_handler(message: types.Message, state: FSMContext):
    await Teacher.iban.set()
    await state.update_data(iin=message.text)
    await message.answer("Введите счет IBAN (вводите вместе с KZ):")

@dp.message_handler(state=Teacher.iban)
async def iban_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(iban=message.text)
