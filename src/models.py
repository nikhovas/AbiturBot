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
    def __init__(self, user_id: int, phys_tech_school_name: str, direction_name: str, comptetition_type: int, val: int,
                 row_number: int):
        self.user_id = user_id
        self.phys_tech_school_name = phys_tech_school_name
        self.comptetition_type = comptetition_type
        self.val = val
        self.row_number = row_number


class CompetitionInfo:
    def __init__(self, direction_id: int, user_id: int, surname: int, name: int, father_name: int,
                 competition_type: int, sum: int):
        self.direction_id = direction_id
        self.user_id = user_id
        self.surname = surname
        self.name = name
        self.father_name = father_name
        self.competition_type = competition_type
        self.sum = sum


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
            result += '{} {} {} {}\n  ...\n'.format(self.first_user.surname, self.first_user.name,
                                                   self.first_user.father_name, self.first_user.sum)
        if self.previous_user is not None:
            result += '{} {} {} {}\n'.format(self.previous_user.surname, self.previous_user.name,
                                             self.previous_user.father_name, self.previous_user.sum)
        result += '*{} {} {} {}*'.format(self.current_user.surname, self.current_user.name,
                                         self.current_user.father_name, self.current_user.sum)
        if self.next_user is not None:
            result += '\n{} {} {} {}'.format(self.next_user.surname, self.next_user.name,
                                                  self.next_user.father_name, self.next_user.sum)
        return result
