import src
from src.sqlite.sqlite_database import SqliteDatabase
from src.telegram.telegram_messenger import TelegramMessenger
from src.kernel import Kernel


USING_MODULES = {
    'database': SqliteDatabase,
    'messenger': TelegramMessenger
}

BOT_CONFIG = {
    'API_TOKEN' : '909308261:AAHJmfqOW2D5-epx5XePYHRuVuEgVML4Odw'
}






kernel: Kernel = Kernel()
