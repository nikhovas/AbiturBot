from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
)

mailing_settings = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Разослать", callback_data="MAIL")).add(
    InlineKeyboardButton("Править текст", callback_data="CHANGE_TEXT"))


async def get_users_departments():
    pass
