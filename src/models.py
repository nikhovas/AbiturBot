from enum import Enum


class UserType(Enum):
    ABITURIENT = 0
    OPERATOR = 1
    ADMIN = 2


class Model(object):
    def __init__(self, record_id: int):
        self.record_id = record_id


class User(Model):
    def __init__(self, record_id: int, user_type: UserType, phone: int, surname: str, name: str, father_name: str):
        super().__init__(record_id)

        self.record_id = record_id
        self.user_type = user_type
        self.phone = phone
        self.surname = surname
        self.name = name
        self.father_name = father_name


class PhysTechSchool(Model):
    def __init__(self, record_id: int, name: str):
        super().__init__(record_id)

        self.name = name


class Department(Model):
    def __init__(self, record_id: int, name: str, phys_tech_school: PhysTechSchool):
        super().__init__(record_id)

        self.name = name
        self.phys_tech_school = phys_tech_school


class Direction(Model):
    def __init__(self, record_id: int, name: str, phys_tech_school: PhysTechSchool):
        super().__init__(record_id)

        self.name = name
        self.phys_tech_school = phys_tech_school


# class CompetitionInfo(Model):
#     def __init__(self, record_id: int, user: User, direction: Direction, score: int):
#         super().__init__(record_id)
#
#         self.user = user
#         self.direction = direction
#         self.score = score


class UserComptetition:
    def __init__(self, user_id, direction_id, phys_tech_school_name: str, direction_name: str, competition_type: int,
                 val: int, competition_name):
        self._direction_id = direction_id
        self._user_id = user_id
        self._direction_name = direction_name
        self._phys_tech_school_name = phys_tech_school_name
        self._competition_type = competition_type
        self._competition_name = competition_name
        self.val = val

    def get_button_text(self):
        return '{} {}'.format(self._phys_tech_school_name, self._direction_name)

    def get_callback_data(self):
        return '{} {} {}'.format(self._user_id, self._direction_id, self._competition_type)

    def get_description(self):
        return '*{} {}*\n Форма поступления:  {}\n Сумма баллов:             {}\n\n'.format(self._phys_tech_school_name, self._direction_name, self._competition_name, self.val)


class CompetitionInfo:
    def __init__(self, direction_id: int, user_id: int, surname: int, name: int, father_name: int,
                 competition_type: int, sum: int, rn = None):
        self.diection_id = direction_id
        self.user_id = user_id
        self.surname = surname
        self.name = name
        self.father_name = father_name
        self.competition_type = competition_type
        self.sum = sum
        self.rn = rn


class RelativeCompetitionInfo:
    def __init__(self, first_user, previous_user, current_user: CompetitionInfo,
                 next_user):
        self.first_user = first_user
        self.previous_user = previous_user
        self.current_user = current_user
        self.next_user = next_user

    def de_json(self) -> str:
        result = ''
        if self.first_user is not None:
            result += '{}. {} {} {} {}\n  ...\n'.format(self.first_user.rn, self.first_user.surname, self.first_user.name[0] + '.',
                                                    self.first_user.father_name[0] + '.', self.first_user.sum)
        if self.previous_user is not None:
            result += '{}. {} {} {} {}\n'.format(self.previous_user.rn, self.previous_user.surname, self.previous_user.name[0] + '.',
                                             self.previous_user.father_name[0] + '.', self.previous_user.sum)
        result += '*{}. {} {} {} {}*'.format(self.current_user.rn, self.current_user.surname, self.current_user.name[0] + '.',
                                         self.current_user.father_name[0] + '.', self.current_user.sum)
        if self.next_user is not None:
            result += '\n{}. {} {} {} {}'.format(self.next_user.rn, self.next_user.surname, self.next_user.name[0] + '.',
                                             self.next_user.father_name[0] + '.', self.next_user.sum)
        return result
