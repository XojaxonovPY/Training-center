from graphene import String, ObjectType, Int
from graphene_django import DjangoObjectType

from apps.models import User, Course, Room, Group, Attendance


class UserDjangoObjectTyp(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'avatar', 'group', 'birthday', 'role', 'gender')


class CourseDjangoObjectTyp(DjangoObjectType):
    name = String()

    class Meta:
        model = Course
        fields = ('id', 'name', 'price')

    def resolve_name(self, info):
        return self.safe_translation_getter('name', any_language=True)


class RoomDjangoObjectType(DjangoObjectType):
    name = String()

    class Meta:
        model = Room
        fields = ('id', 'name', 'count', 'capacity')

    def resolve_name(self, info):
        return self.safe_translation_getter('name', any_language=True)


class GroupDjangoObjectTyp(DjangoObjectType):
    name = String()

    class Meta:
        model = Group
        fields = '__all__'

    def resolve_name(self, info):
        return self.safe_translation_getter('name', any_language=True)


class AttendanceDjangoObjectTyp(DjangoObjectType):
    class Meta:
        model = Attendance
        fields = '__all__'


class StatisticObjectType(ObjectType):
    employee_count = Int()
    student_count = Int()
    groups = Int()
    debtors = Int()
    payments = Int()
    left_the_group = Int()
