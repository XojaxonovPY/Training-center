from django.db.models import Sum
from graphene import ObjectType, List, Field
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from transactions.filter import TransactionFilter
from transactions.models import Category, Debt, Payment
from transactions.types import CategoryDjangoObjectType, TransactionDjangoObjectType
from transactions.types import DebtDjangoObjectType, PaymentDjangoObjectType


class Query(ObjectType):
    all_categories = List(CategoryDjangoObjectType)
    all_transactions = DjangoFilterConnectionField(TransactionDjangoObjectType, filterset_class=TransactionFilter)
    all_debt = List(DebtDjangoObjectType)
    user_payment = Field(PaymentDjangoObjectType)

    @login_required
    def resolve_all_categories(self, info):
        return Category.objects.all()

    @login_required
    def resolve_all_debt(self, info):
        return Debt.objects.all().annotate(total_price=Sum('amount'))

    @login_required
    def resolve_user_payment(self, info):
        return Payment.objects.filter(owner=info.context.user).first()
