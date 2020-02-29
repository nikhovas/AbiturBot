# from src.module import Module
from src.models import *
from typing import List


class Database:
    async def get_user_by_phone(self, phone: str) -> User:
        pass

    async def get_phys_tech_schools_info(self):
        pass

    async def get_full_competition_list(self, competition: Direction) -> List[CompetitionInfo]:
        pass

    async def get_place_in_competition(self, user: User, competition: Direction) -> int:
        pass
