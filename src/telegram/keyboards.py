from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
)

mailing_settings = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Разослать", callback_data="MAIL")).add(
    InlineKeyboardButton("Править текст", callback_data="CHANGE_TEXT"))

asking_settings = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Отправить", callback_data="MAIL")).add(
    InlineKeyboardButton("Править текст", callback_data="CHANGE_TEXT"))

add_to_cash = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Да", callback_data="ADD_TO_CASH")).add(
    InlineKeyboardButton("Нет", callback_data="DONT_ADD_TO_CASH"))

continue_answer = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Да", callback_data="CONTINUE_ANSWER")).add(
    InlineKeyboardButton("Нет", callback_data="STOP_ANSWER"))

markup_main = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Информация о конкурсе')
).add(
    KeyboardButton('Задать вопрос о поступлении')
)


def get_questions_keyboard(chat_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=2).insert(
        InlineKeyboardButton("Ответить на этот вопрос", callback_data="ASK_QUESTION {}".format(chat_id))).add(
        InlineKeyboardButton('Пропустить', callback_data="NEXT_QUESTION {}".format(chat_id))).add(
        InlineKeyboardButton("Удалить вопрос", callback_data="DELETE_QUESTION"))


async def get_users_departments():
    pass
