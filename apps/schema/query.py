from graphene import ObjectType, List, Field
from graphql_jwt.decorators import login_required
from apps.models import User, Course, Room, Group, Attendance
from apps.permission import is_admin, is_teacher
from apps.types import AttendanceDjangoObjectTyp, GroupDjangoObjectTyp, StatisticObjectType
from apps.types import UserDjangoObjectTyp, CourseDjangoObjectTyp, RoomDjangoObjectType
from transactions.models import Debt, Payment
from django.utils.timezone import now


class Query(ObjectType):
    all_users = List(UserDjangoObjectTyp)
    all_courses = List(CourseDjangoObjectTyp)
    all_rooms = List(RoomDjangoObjectType)
    all_groups = List(GroupDjangoObjectTyp)
    all_attendances = List(AttendanceDjangoObjectTyp)
    teacher_group = List(GroupDjangoObjectTyp)
    statistic = Field(StatisticObjectType)
    one_user = Field(UserDjangoObjectTyp)

    @login_required
    @is_admin
    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    @login_required
    def resolve_all_courses(self, info, **kwargs):
        return Course.objects.all()

    @login_required
    def resolve_all_rooms(self, info, **kwargs):
        return Room.objects.all()

    @login_required
    def resolve_all_groups(self, info, **kwargs):
        return Group.objects.all()

    @login_required
    def resolve_all_attendances(self, info, **kwargs):
        return Attendance.objects.all()

    @login_required
    @is_teacher
    def resolve_teacher_group(self, info, **kwargs):
        return Group.objects.filter(teacher=info.context.user).all()

    @login_required
    def resolve_statistic(self, info):
        today = now()
        statistic = {
            'employee_count': User.objects.filter(role=User.RoleType.TEACHER).count(),
            'student_count': User.objects.filter(role=User.RoleType.STUDENT).count(),
            'groups': Group.objects.all().count(),
            'debtors': Debt.objects.all().count(),
            'payments': Payment.objects.filter(created_at__year=today.year, created_at__month=today.month).count(),
            'left_the_group': User.objects.filter(is_group=True).count()
        }
        return StatisticObjectType(**statistic)

    @login_required
    def resolve_one_user(self, info, **kwargs):
        return User.objects.filter(pk=info.context.user.pk).first()
