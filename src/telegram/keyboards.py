from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from src.models import *
from typing import List

markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
)

mailing_settings = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Разослать", callback_data="MAIL")).add(
    InlineKeyboardButton("Править текст", callback_data="CHANGE_TEXT"))

asking_settings = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Отправить", callback_data="MAIL")).add(
    InlineKeyboardButton("Править текст", callback_data="CHANGE_TEXT"))

add_to_cash = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Да", callback_data="ADD_TO_CASH")).add(
    InlineKeyboardButton("Нет", callback_data="DONT_ADD_TO_CASH"))

continue_answer = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Да", callback_data="CONTINUE_ANSWER")).add(
    InlineKeyboardButton("Нет", callback_data="STOP_ANSWER"))

markup_main = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Информация о конкурсе')
).add(
    KeyboardButton('Задать вопрос о поступлении')
)

mini_main = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Задать вопрос о поступлении')
)

back = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Назад", callback_data='BACK'))

is_correct = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Корректный ответ", callback_data='CORRECT')).add(
    InlineKeyboardButton("Не корректный ответ", callback_data='NOT_CORRECT'))


def get_questions_keyboard(chat_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=2).insert(
        InlineKeyboardButton("Ответить на этот вопрос", callback_data="ASK_QUESTION {}".format(chat_id))).add(
        InlineKeyboardButton('Пропустить', callback_data="NEXT_QUESTION {}".format(chat_id))).add(
        InlineKeyboardButton("Удалить вопрос", callback_data="DELETE_QUESTION"))


def get_competition_keyboard(competitions: List[UserComptetition]):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for i in competitions:
        keyboard.add(InlineKeyboardButton(i.get_button_text(), callback_data=i.get_callback_data()))
    keyboard.add(InlineKeyboardButton('Главное меню', callback_data='MAIN_MENU'))
    return keyboard
