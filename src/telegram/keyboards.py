from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
)

mailing_settings = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Разослать", callback_data="MAIL")).add(
    InlineKeyboardButton("Править текст", callback_data="CHANGE_TEXT"))

markup_main = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Информация о конкурсе')
).add(
    KeyboardButton('Задать вопрос о поступлении')
)

questions_keyboard = InlineKeyboardMarkup(row_width=2).insert(
    InlineKeyboardButton("Ответить на этот вопрос", callback_data="ASK_QUESTION")).add(
    InlineKeyboardButton('⬅️', callback_data="NEXT_QUESTION")).add(
    InlineKeyboardButton('➡️', callback_data="PREV_QUESTION")).add(
    InlineKeyboardButton("Удалить вопрос", callback_data="DELETE_QUESTION"))


async def get_users_departments():
    pass
