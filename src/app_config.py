import src


USING_MODULES = {
    'database': src.sqlite.sqlite_database.SqliteDatabase,
    'messenger': src.telegram.telegram_messenger.TelegramMessenger
}

BOT_CONFIG = {
    'API_TOKEN' : '909308261:AAHJmfqOW2D5-epx5XePYHRuVuEgVML4Odw'
}



class RawFiles:
    PHYS_TECH_SCHOOLS_INFO_FILE = "/data/phys_tech_schools_info.txt"
