from src.module import Module
from src.models import *
from typing import List


class Database(Module):
    async def get_phys_tech_schools_info(self):
        pass

    async def get_full_competition_list(self) -> List[Direction]:
        pass

    async def get_place_in_competition(self, user: User, competition: Direction) -> CompetitionInfo:
        pass
