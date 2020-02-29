from src.database import Database
from sqlalchemy import create_engine
import aiopg
from src.models import *
from typing import List

class SqliteDatabase(Database):
    def __init__(self, kernel):
        super().__init__()

        self._dbname = "some name"
        self._user = "user"
        self._password = "11111111"
        self._host = "fds"

        self._conn = None
        self._cur = None

    async def connect(self):
        self._conn = await aiopg.connect(database=self._dbname,
                                         user=self._user,
                                         password=self._password,
                                         host=self._host)
        self._cur = await self._conn.cursor()

    def is_connected(self):
        return self._conn is not None

    async def is_user_exists(self, user_id):
        if not self.is_connected():
            await self.connect()

        await self._cur.execute('SELECT * FROM user where  = {}', (user_id,))
        ret = await self._cur.fetchone()
        return ret is not None

    async def add_user(self, id, lang, loc):
        if not self.is_connected():
            await self.connect()

        await self._cur.execute('INSERT INTO to_do_list.user_info(user_id, time_zone, lang) VALUES (%s, %s, %s)',
                                (id, loc, lang))

    async def add_task(self, user_id, text, date=None):
        if not self.is_connected():
            await self.connect()

        await self._cur.execute("INSERT INTO to_do_list.tasks(user_id, date, text) values (%s, %s, %s)",
                                (user_id, date, text))

    async def add_list(self, user_id, name):
        if not self.is_connected():
            await self.connect()

        await self._cur.execute("INSERT INTO to_do_list.lists(user_id, name) values (%s, %s)", (user_id, name))

    async def get_lists(self, user_id):
        if not self.is_connected():
            await self.connect()

        await self._cur.execute("SELECT * FROM to_do_list.lists where user_id = %s", (user_id,))
        return await self._cur.fetchall()

    async def get_tasks_page_with_dates(self, page_num, user_id):
        if not self.is_connected():
            await self.connect()

        await self._cur.execute('''WITH T1 AS (SELECT task_id, date, text, is_important, lists.name, row_number() over (order by date) as rn
                                    FROM to_do_list.tasks 
                                        LEFT JOIN to_do_list.lists 
                                            ON tasks.list_id = lists.list_id 
                                    WHERE   tasks.user_id = %s 
                                            and NOT is_active 
                                            AND date IS NOT NULL)
                                    SELECT task_id, date, text, is_important, name FROM T1 WHERE rn >= 5 * %s + 1 and rn <= 5 * %s + 6''',
                                (user_id, page_num, page_num))
        return await self._cur.fetchall()

    async def get_user_by_phone(self, phone: str) -> int:
        if not self.is_connected():
            await self.connect()

        await self._cur.execute('SELECT user_id FROM bot_user where phone = {}'.format(phone))
        return await self._cur.fetchone()[0]

    async def get_user_by_chat_id(self, chat_id: int):
        if not self.is_connected():
            await self.connect()

        try:
            await self._cur.execute('SELECT user_id FROM user_id_x_chat_id where chat_id = {}'.format(chat_id))
            return await self._cur.fetchone()[0]
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
        return await self._cur.fetchone()[0] is 1

    async def does_user_exist(self, phone: str) -> bool:
        if not self.is_connected():
            await self.connect()

        await self._cur.execute('SELECT user_id FROM bot_user where phone = {}'.format(phone))
        return await self._cur.fetchone()[0] is not None





