from src.database import Database
import aiopg
from src.models import *
from typing import List
import asyncio


class SqliteDatabase(Database):
    def __init__(self, kernel):
        super().__init__()

        self.kernel = kernel

        self._user = "user1"
        self._password = "11111111"
        self._dsn = 'postgresql://rc1c-5z1z7shu9girllca.mdb.yandexcloud.net:6432/db1'

        self._conn = None
        self._cur = None

    async def connect(self):
        self._conn = await aiopg.connect(dsn=self._dsn, user=self._user, password=self._password)
        self._cur = await self._conn.cursor()

    def is_connected(self):
        return self._conn is not None

    async def get_user_by_phone(self, phone: str) -> int:
        if not self.is_connected():
            await self.connect()

        await self._cur.execute('SELECT user_id FROM bot_user where phone = \'{}\''.format(phone))
        return (await self._cur.fetchone())[0]

    async def get_user_by_chat_id(self, chat_id: int):
        if not self.is_connected():
            await self.connect()

        try:
            await self._cur.execute('SELECT user_id FROM user_id_x_chat_id where chat_id = {}'.format(chat_id))
            return (await self._cur.fetchone())[0]
        except ...:
            return None

    async def get_all_user_competitions(self, user_id: int) -> List[UserComptetition]:
        if not self.is_connected():
            await self.connect()

        await self._cur.execute('SELECT competition_element.direction_id, phys_tech_school_name, direction_name, '
                                'competition_element.competition_type, sum'
                                'FROM competitions_for_user WHERE user_id = {}'.format(user_id))

        result = list()
        for i in await self._cur.fetchall():
            result.append(UserComptetition(*i))

        return result

    async def get_competition_list(self, direction_id: int, competition_type: int) -> List[CompetitionInfo]:
        if not self.is_connected():
            await self.connect()

        await self._cur.execute('SELECT competition_element.direction_id, phys_tech_school_name, direction_name, '
                                'competition_element.competition_type, sum'
                                'FROM competition_view WHERE direction_id = {} and competition_type = {}',
                                (direction_id, competition_type))

        result = list()
        for i in await self._cur.fetchall():
            result.append(CompetitionInfo(*i))

        return result

    async def is_user_admin(self, user_id: int) -> bool:
        if not self.is_connected():
            await self.connect()

        await self._cur.execute('SELECT type FROM bot_user where user_id = {}'.format(user_id))
        return (await self._cur.fetchone())[0] is 1

    async def does_user_exist(self, phone: str) -> bool:
        if not self.is_connected():
            await self.connect()

        await self._cur.execute('SELECT user_id FROM bot_user where phone = {}'.format(phone))
        return (await self._cur.fetchone())[0] is not None

    async def get_all_chat_ids(self) -> List[int]:
        if not self.is_connected():
            await self.connect()

        await self._cur.execute('SELECT * FROM user_id_x_chat_id')

        result = List[int]()
        for i in await self._cur.fetchall():
            result.append(i[1])

        return result

    async def set_chat_id_for_user(self, user_id: int, chat_id: int):
        if not self.is_connected():
            await self.connect()

        await self._cur.execute('SELECT chat_id FROM user_id_x_chat_id where user_id = %s', (user_id, ))

        database_chat_id = await self._cur.fetchone()

        if database_chat_id is None:
            await self._cur.execute('INSERT INTO user_id_x_chat_id(user_id, chat_id) VALUES (%s, %s)',
                                    (user_id, chat_id))
        elif database_chat_id is not chat_id:
            await self._cur.execute('UPDATE user_id_x_chat_id SET chat_id = %s where user_id = %s',
                                    (chat_id, user_id))
