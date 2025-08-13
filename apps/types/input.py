from graphene import InputObjectType, String, List, Int, Time, Date, Boolean, Decimal

from apps.filters import DayTypeEnum, UserRoleType, UserGenderType


class RegisterInputObjectType(InputObjectType):
    first_name = String()
    last_name = String()
    phone_number = String(required=True)
    password = String(required=True)


class UserInputObjectType(InputObjectType):
    first_name = String()
    last_name = String()
    phone_number = String()
    password = String()
    role = UserRoleType()
    gender = UserGenderType()
    birthday = Date()
    group_id = Int()


class VerifyInputObjectTyp(InputObjectType):
    pk = String(required=True)
    code = String(required=True)


class TranslationInput(InputObjectType):
    language_code = String(required=True)
    name = String()


class CourseInputObjectType(InputObjectType):
    translations = List(TranslationInput, required=True)
    price = Decimal(required=True)


class RoomInputObjectType(InputObjectType):
    translations = List(TranslationInput, required=True)
    capacity = Int(required=True)
    count = Int(required=True)


class GroupInputObjectType(InputObjectType):
    translations = List(TranslationInput)
    time = Time()
    course_id = Int()
    teacher_id = Int()
    room_id = Int()
    days = DayTypeEnum()


class AttendanceInputObjectType(InputObjectType):
    date = Date(required=True)
    is_present = Boolean(required=True)
    student_id = Int(required=True)
    group_id = Int(required=True)
