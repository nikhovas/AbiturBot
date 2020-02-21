from src.kernel import Kernel
from src.database import Database
from sqlalchemy import create_engine


class SqliteDatabase(Database):
    def __init__(self, kernel: Kernel):
        super().__init__(kernel)

        self.engine = create_engine('sqlite:///:memory:', echo=True)
