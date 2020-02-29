from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from app_config import BOT_CONFIG

from src.messenger import Messenger


class TelegramMessenger(Messenger):
    def __init__(self, event_loop, kernel: Kernel):
        super().__init__(kernel)
        self._event_loop = event_loop

        self._bot = BOT(token=BOT_CONFIG['API_TOKEN'])
        self._dispatcher = Dispatcher(bot, storage=MemoryStorage())

    @self._dispatcher.message_handler(commands=['start'])
    async def process_start_command(self, msg: types.Message):
        pass