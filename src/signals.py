from src.models import *


class Signal:
    pass


class RatingInCompetition(Signal):
    def __init__(self, direction: Direction):
        self.direction = direction


class GetPhysTechSchoolsInfo(Signal):
    def __init__(self):
        pass


class GetCompetitionInfo(Signal):
    def __init__(self, direction: Direction):
        self.direction = direction
