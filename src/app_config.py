import src


USING_MODULES = {
    'database': src.sqlite.sqlite_database.SqliteDatabase,
    'messenger': src.telegram.telegram_messenger.TelegramMessenger
}


class RawFiles:
    PHYS_TECH_SCHOOLS_INFO_FILE = "/data/phys_tech_schools_info.txt"
