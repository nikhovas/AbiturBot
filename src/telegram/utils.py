from aiogram.dispatcher.filters.state import State, StatesGroup


class AdmMailing(StatesGroup):
    mailing_text = State()
    check_text = State()