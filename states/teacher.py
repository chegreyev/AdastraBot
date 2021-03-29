from aiogram.dispatcher.filters.state import State, StatesGroup


class Teacher(StatesGroup):
    type = State()

    subject = State()
    subject_grades = State()
    subject_languages = State()
    subject_levels = State()

    demo_lesson_day = State()
    demo_lesson_time = State()

    interview_day = State()
    interview_time = State()

    fio = State()
    city = State()
    address = State()
    phone_number = State()
    email = State()
    iin = State()
    iban = State()
