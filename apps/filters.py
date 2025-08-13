from graphene import Enum


class DayTypeEnum(Enum):
    ODD_DAYS = 'odd days'
    COUPLE_DAYS = 'couple days'
    MONDAY = 'monday'
    TUESDAY = 'tuesday'
    WEDNESDAY = 'wednesday'
    THURSDAY = 'thursday', 'Thursdays'
    FRIDAY = 'friday', 'Fridays'
    SATURDAY = 'saturday', 'Saturdays'


class UserRoleType(Enum):
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'

class UserGenderType(Enum):
    MALE = 'male'
    FEMALE = 'female'

