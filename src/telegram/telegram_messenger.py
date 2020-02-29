from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


import src.telegram.keyboards as keyboards
from src.messenger import Messenger


class TelegramMessenger(Messenger):
    bot = Bot(token='909308261:AAHJmfqOW2D5-epx5XePYHRuVuEgVML4Odw')
    dispatcher = None

    def __init__(self, event_loop, kernel: Kernel):
        # super().__init__(kernel)
        super().__init__(kernel)
        self._event_loop = event_loop

        self.dispatcher = Dispatcher(self.bot, loop=event_loop, storage=MemoryStorage())

    def start_pooling(self):
        executor.start_polling(self.dispatcher)

    @dispatcher.message_handler(commands=['start'])
    async def process_start_command(self, msg: types.Message):
        await self.bot.send_message("Добро пожаловать! Отправьте свой номер телефона.",
                                     reply_markup=keyboards.markup_request)


