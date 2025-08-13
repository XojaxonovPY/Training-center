import graphene
import graphql_jwt

from apps import schema as apps
from transactions import schema as transactions


class Query(apps.Query, transactions.Query):
    pass


class Mutation(graphene.ObjectType):
    # ----------------- AUTH -----------------
    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    register_user = apps.RegisterMutation.Field()
    verify_code = apps.VerifyMutation.Field()
    # ---------------- COURSE ----------------
    course_create = apps.CourseMutation.Field()
    # ---------------- COURSE    ----------------
    room_create = apps.RoomMutation.Field()
    # ---------------- GROUP ----------------
    group_create = apps.GroupMutation.Field()
    group_update = apps.UpdateGroupMutation.Field()
    group_delete = apps.DeleteGroupMutation.Field()
    # ----------------- ATTENDANCE -----------------
    attendance_create = apps.AttendanceMutation.Field()
    # ----------------- USER -----------------
    user_create = apps.CreateUserMutation.Field()
    user_update = apps.UpdateUserMutation.Field()
    user_delete = apps.DeleteUserMutation.Field()
    # ----------------- TRANSACTIONS -----------------
    category_create = transactions.CategoryMutation.Field()
    transaction_create = transactions.TransactionCreateMutation.Field()
    transaction_delete = transactions.TransactionDeleteMutation.Field()
    transaction_update = transactions.TransactionUpdateMutation.Field()
    debt_create = transactions.DebtMutation.Field()
    payment_create = transactions.PaymentMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
