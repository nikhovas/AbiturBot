from src.messenger import Messenger
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from . import keyboards
# from src.app_config import kernel

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

