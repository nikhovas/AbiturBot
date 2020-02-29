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


class CompetitionInfo:
    def __init__(self, record_id: int, user: User, direction: Direction):
        super().__init__(record_id)

        self.user = user
        self.direction = direction
