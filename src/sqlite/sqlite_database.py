from src.database import Database
import aiopg
from src.models import *
from typing import List


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
        except Exception:
            return None

    async def get_all_user_competitions(self, user_id: int) -> List[UserComptetition]:
        if not self.is_connected():
            await self.connect()

        await self._cur.execute('''SELECT user_id, direction_id, phys_tech_school_name, direction_name,
                                competition_type, val, c.name
                                FROM competitions_for_user as cfu inner join competition as c on cfu.competition_type = c.competition_type_id
                                WHERE user_id = {}'''.format(user_id))

        result = list()
        for i in await self._cur.fetchall():
            result.append(UserComptetition(*i))

        return result

    async def get_competition_list(self, direction_id: int, competition_type: int) -> List[CompetitionInfo]:
        if not self.is_connected():
            await self.connect()

        await self._cur.execute('''SELECT *
                                FROM competition_view WHERE direction_id = %s and competition_type = %s''',
                                (direction_id, competition_type))

        result = list()
        for i in await self._cur.fetchall():
            result.append(CompetitionInfo(*i))

        return result

    async def get_competition_list_rn(self, direction_id: int, competition_type: int) -> List[CompetitionInfo]:
        if not self.is_connected():
            await self.connect()

        await self._cur.execute('''SELECT *, row_number() over (order by sum desc) as rn
                                FROM competition_view WHERE direction_id = %s and competition_type = %s''',
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

    async def get_all_chat_ids(self) -> list:
        if not self.is_connected():
            await self.connect()

        await self._cur.execute('SELECT * FROM user_id_x_chat_id')

        result = list()
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

    async def get_relative_list(self, user_id: int, direction_id: int, competition_type: int) -> RelativeCompetitionInfo:
        competition_list = await self.get_competition_list(direction_id,competition_type)
        first_row: CompetitionInfo = competition_list[0]
        last_row: CompetitionInfo = competition_list[-1]
        if first_row.user_id is user_id:
            if len(competition_list) is 1:
                return RelativeCompetitionInfo(None, None, first_row, None)
            else:
                return RelativeCompetitionInfo(None, None, first_row, competition_list[1])
        elif last_row.user_id is user_id:
            if len(competition_list) is 2:
                return RelativeCompetitionInfo(None, competition_list[0], competition_list[1], None)
            else:
                return RelativeCompetitionInfo(first_row, competition_list[-2], competition_list[-1], None)
        else:
            second_row: CompetitionInfo = competition_list[1]
            if second_row.user_id is user_id:
                return RelativeCompetitionInfo(None, first_row, second_row, competition_list[2])
            else:
                n = 0
                for i in range(len(competition_list)):
                    if competition_list[i].user_id is user_id:
                        n = i
                        break

                return RelativeCompetitionInfo(competition_list[0], competition_list[n - 1], competition_list[n],
                                               competition_list[n + 1])

    async def get_chat_id_by_user_id(self, user_id: int) -> int:
        if not self.is_connected():
            await self.connect()

        await self._cur.execute('SELECT chat_id FROM user_id_x_chat_id where user_id = {}'.format(user_id))
        return (await self._cur.fetchone())[0]

    async def is_user_admin_by_chat_id(self, chat_id) -> bool:
        if not self.is_connected():
            await self.connect()

        await self._cur.execute('SELECT bot_user.type FROM user_id_x_chat_id '
                                'INNER JOIN bot_user on user_id_x_chat_id.user_id = bot_user.user_id '
                                'where chat_id = {}'.format(chat_id))
        return (await self._cur.fetchone())[0] is 1
