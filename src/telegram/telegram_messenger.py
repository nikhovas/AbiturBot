from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils import executor

from src.messenger import Messenger
from . import keyboards
from . import utils

bot = Bot(token='909308261:AAHJmfqOW2D5-epx5XePYHRuVuEgVML4Odw')
dispatcher = Dispatcher(bot, storage=MemoryStorage())


class TelegramMessenger(Messenger):
    def __init__(self, kernel):
        self.kernel = kernel
        super().__init__()

    def start_pooling(self):
        executor.start_polling(dispatcher)

    @dispatcher.message_handler(commands=['start'])
    async def process_start_command(msg: types.Message):
        await bot.send_message(msg.from_user.id, "Добро пожаловать! Отправьте свой номер телефона.",
                               reply_markup=keyboards.markup_request)

    @dispatcher.message_handler(content_types=['contact'])
    async def process_get_contact(msg: types.Message):
        await bot.send_message(msg.from_user.id, "Ваш номер телефона {}.".format(msg.contact['phone_number']),
                               reply_markup=ReplyKeyboardRemove())

        # data base working

    @dispatcher.message_handler(commands=['mailing'])
    async def process_admin_mailing(msg: types.Message):
        await bot.send_message(msg.from_user.id, "Введите текст рассылки.")
        await utils.AdmMailing.mailing_text.set()

    @dispatcher.message_handler(content_types=['text'], state=utils.AdmMailing.mailing_text)
    async def get_mailing_text(msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['text'] = msg.text

        await bot.send_message(msg.from_user.id, msg.text,
                               reply_markup=keyboards.mailing_settings)

        await utils.AdmMailing.check_text.set()

    @dispatcher.callback_query_handler(lambda call: call.data == 'CHANGE_TEXT', state=utils.AdmMailing.check_text)
    async def change_mailing_text(call: types.CallbackQuery, state: FSMContext):
        await bot.edit_message_text("Введите новый текст", call.from_user.id,
                                call.message.message_id)

    @dispatcher.message_handler(content_types=['text'], state=utils.AdmMailing.check_text)
    async def get_new_text(msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['text'] = msg.text

        await bot.send_message(msg.from_user.id, msg.text,
                               reply_markup=keyboards.mailing_settings)

    @dispatcher.callback_query_handler(lambda call: call.data == 'MAIL', state=utils.AdmMailing.check_text)
    async def send_mailing_text(call: types.CallbackQuery, state: FSMContext):
        pass



