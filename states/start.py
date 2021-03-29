from aiogram.dispatcher.filters.state import State, StatesGroup


class Start(StatesGroup):
    code = State()


class ManagerStart(StatesGroup):
    email = State()
    password = State()

    # Authorization
    change_email = State()
    change_password = State()
