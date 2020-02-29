from src.models import *


class Signal:
    pass


class RatingInCompetition(Signal):
    def __init__(self, competition_info: CompetitionInfo):
        self.competition_info = competition_info


class GetPhysTechSchoolsInfo(Signal):
    def __init__(self):
        pass


# other classes
