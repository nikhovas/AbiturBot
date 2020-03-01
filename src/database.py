# from src.module import Module
from src.models import *
from typing import List


class Database:
    async def get_user_by_phone(self, phone: str) -> int:
        pass

    async def get_user_by_chat_id(self, chat_id: int):
        pass

    async def get_all_user_competitions(self, user_id: int) -> List[UserComptetition]:
        pass

    async def get_competition_list(self, direction_id: int, competition_type: int) -> List[CompetitionInfo]:
        pass

    async def is_user_admin(self, user_id: int) -> bool:
        pass

    async def does_user_exist(self, phone: str) -> bool:
        pass

    async def get_all_chat_ids(self) -> List[int]:
        pass

    async def set_chat_id_for_user(self, user_id: int, chat_id: int):
        pass

    async def get_relative_list(self, user_id, direction_id: int, competition_type: int):
        pass

    async def get_chat_id_by_user_id(self, user_id: int) -> int:
        pass

    async def is_user_admin_by_chat_id(self, chat_id) -> bool:
        pass
