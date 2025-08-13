import json
import random
import uuid

from django.contrib.auth.hashers import make_password
from graphene import Mutation, Field, ID, String
from graphene.types.generic import GenericScalar
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from parler.utils.context import switch_language

from apps.models import Course, User, Group, Room, Attendance
from apps.permission import is_admin, is_teacher
from apps.tasks import send_code_phone_number
from apps.types import AttendanceInputObjectType, AttendanceDjangoObjectTyp, UserInputObjectType
from apps.types import CourseInputObjectType, CourseDjangoObjectTyp, RoomInputObjectType
from apps.types import GroupInputObjectType, GroupDjangoObjectTyp, RoomDjangoObjectType
from apps.types import RegisterInputObjectType, UserDjangoObjectTyp, VerifyInputObjectTyp
from root.settings import redis


# ============================================Register============================

class RegisterMutation(Mutation):
    class Arguments:
        input = RegisterInputObjectType()

    response = GenericScalar()

    def mutate(self, info, input: RegisterInputObjectType):
        pk = str(uuid.uuid4())
        code = random.randrange(10 ** 5, 10 ** 6)
        if len(input.phone_number) <= 10:
            raise GraphQLError('Wrong phone number')
        query = User.objects.filter(phone_number=input.phone_number)
        if query.exists():
            raise GraphQLError('Phone number already exists')
        user = {
            'first_name': input.first_name,
            'last_name': input.last_name,
            'phone_number': input.phone_number,
            'password': make_password(input.password),
        }
        data = {
            'code': code,
            'user': user,
        }

        send_code_phone_number.delay(user, code)
        redis.mset({pk: json.dumps(data)})
        return RegisterMutation(response={'message': 'Send verify code', 'pk': pk})


class VerifyMutation(Mutation):
    class Arguments:
        input = VerifyInputObjectTyp()

    user = Field(UserDjangoObjectTyp())

    def mutate(self, info, input: VerifyInputObjectTyp):
        pk = input.pk
        redis_data = redis.get(pk)
        if not redis_data:
            raise GraphQLError('Expire code')
        data = json.loads(redis_data)
        code = data.get('code')
        verify_code = input.code
        if verify_code != str(code):
            raise GraphQLError('Verify code incorrect')
        user = User.objects.create(**data.get('user'))
        return VerifyMutation(user=user)


# ============================================Course============================

class CourseMutation(Mutation):
    class Arguments:
        input = CourseInputObjectType()

    course = Field(CourseDjangoObjectTyp)

    @login_required
    @is_admin
    def mutate(self, info, input: CourseInputObjectType):
        course = Course()
        course.price = input.price
        for trans in input.translations:
            lang = trans.language_code
            with switch_language(course, lang):
                course.name = trans.name
                course.save()
        return CourseMutation(course=course)


# ===========================================Room========================================

class RoomMutation(Mutation):
    class Arguments:
        input = RoomInputObjectType()

    room = Field(RoomDjangoObjectType)

    @login_required
    @is_admin
    def mutate(self, info, input: RoomInputObjectType):
        room = Room(capacity=input.capacity)
        room.save()
        for trans in input.translations:
            lang = trans.language_code
            with switch_language(room, lang):
                room.name = trans.name
                room.save()
        return RoomMutation(room=room)


# ===========================================Group========================================


class GroupMutation(Mutation):
    class Arguments:
        input = GroupInputObjectType(required=True)

    group = Field(GroupDjangoObjectTyp)

    @login_required
    @is_admin
    def mutate(self, info, input: GroupInputObjectType):
        # Avval groupni yaratamiz
        group = Group(
            teacher_id=input.teacher_id,
            room_id=input.room_id,
            course_id=input.course_id,
            time=input.time,
            days=input.days.value
        )
        group.save()  # kerakli joy — FOR tashqarisida

        # Endi tarjimalarni saqlaymiz
        for trans in input.translations:
            lang = trans.language_code
            with switch_language(group, lang):
                group.name = trans.name
                group.save()  # har til uchun alohida save

        return GroupMutation(group=group)


class UpdateGroupMutation(Mutation):
    class Arguments:
        input = GroupInputObjectType()
        id = ID()

    group = Field(GroupDjangoObjectTyp)

    @login_required
    @is_admin
    def mutate(self, info, input: GroupInputObjectType, id):
        group = Group.objects.filter(pk=id).first()
        if not group:
            raise GraphQLError('Group not found')
        if input.teacher_id:
            group.teacher_id = input.teacher_id
        if input.course_id:
            group.room_id = input.room_id
        if input.course_id:
            group.course_id = input.course_id
        if input.time:
            group.time = input.time
        if input.days:
            group.days = input.days.value

        group.save()
        if input.translations:
            for trans in input.translations:
                lang = trans.language_code
                with switch_language(group, lang):
                    group.name = trans.name
                    group.save()
        return UpdateGroupMutation(group=group)


class DeleteGroupMutation(Mutation):
    class Arguments:
        id = ID()

    success = GenericScalar()

    def mutate(self, info, id):
        group = Group.objects.filter(pk=id).first()
        if not group:
            raise GraphQLError('Group not found')
        group.delete()
        return DeleteGroupMutation(success={'message': 'group deleted', 'status': 205})


# ==================================Attendance====================================

class AttendanceMutation(Mutation):
    class Arguments:
        input = AttendanceInputObjectType()

    attendance = Field(AttendanceDjangoObjectTyp)

    @login_required
    @is_teacher
    def mutate(self, info, input: AttendanceInputObjectType):
        attendance = Attendance.objects.create(**input.__dict__)
        return AttendanceMutation(attendance=attendance)


# ==================================User====================================


class CreateUserMutation(Mutation):
    class Arguments:
        input = UserInputObjectType()

    user = Field(UserDjangoObjectTyp)

    @login_required
    @is_admin
    def mutate(self, info, input: UserInputObjectType):
        if len(input.phone_number) <= 10:
            raise GraphQLError('Phone number must be between 1 and 12 characters')
        user = User.objects.create_user(**input.__dict__)
        return CreateUserMutation(user=user)


class UpdateUserMutation(Mutation):
    class Arguments:
        input = UserInputObjectType()
        id = ID()
        avatar = String()

    user = Field(UserDjangoObjectTyp)

    @login_required
    def mutate(self, info, input: UserInputObjectType, id, avatar=None):
        user = User.objects.filter(pk=id).first()
        if not user:
            raise GraphQLError('User not found')
        if avatar:
            user.avatar = avatar
        if input.role:
            user.role = input.role.value
        if input.gender:
            user.gender = input.gender.value
        if input.birthday:
            user.birthday = input.birthday.value
        if input.first_name:
            user.first_name = input.first_name
        if input.last_name:
            user.last_name = input.last_name
        if input.phone_number:
            user.phone_number = input.phone_number
        if user.password:
            user.password = make_password(user.password)
        user.save()

        return UpdateUserMutation(user=user)


class DeleteUserMutation(Mutation):
    class Arguments:
        id = ID()

    success = GenericScalar()

    @login_required
    def mutate(self, info, id):
        user = User.objects.filter(pk=id).first()
        if not user:
            raise GraphQLError('User not found')
        user.delete()
        return DeleteUserMutation(success={'message': 'user deleted', 'status': 205})
