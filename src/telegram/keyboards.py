from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
)


async def get_users_departments():
    pass
