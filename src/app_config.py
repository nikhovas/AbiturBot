import src


USING_MODULES = {
    'database': src.sqlite.sqlite_database.SqliteDatabase,
    'messenger': src.telegram.telegram_messenger.TelegramMessenger
}