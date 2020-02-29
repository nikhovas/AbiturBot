from src.database import Database
from sqlalchemy import create_engine


class SqliteDatabase(Database):
    def __init__(self):
        super().__init__()

        self.engine = create_engine('sqlite:///:memory:', echo=True)
