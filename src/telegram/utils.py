from aiogram.dispatcher.filters.state import State, StatesGroup


class QuestionInfo:
    def __init__(self, text, chat_id):
        self.text = text
        self.chat_id = chat_id


class MainUser(StatesGroup):
    main = State()
    show_comp_info = State()


class AdmMailing(StatesGroup):
    mailing_text = State()
    check_text = State()


class AdmAskQuestions(StatesGroup):
    asking = State()
    get_answer = State()
    check_text = State()
    send = State()
    continue_answer = State()
