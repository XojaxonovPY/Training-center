from graphene import String,relay,Decimal
from graphene_django import DjangoObjectType

from transactions.models import Category, Transaction, Debt, Payment


class CategoryDjangoObjectType(DjangoObjectType):
    name = String()

    class Meta:
        model = Category
        fields = ('id', 'name')

    def resolve_name(self, info):
        return self.safe_translation_getter('name', any_language=True)


class TransactionDjangoObjectType(DjangoObjectType):
    name = String()

    class Meta:
        model = Transaction
        fields = ('id', 'category', 'amount', 'created_at', 'receiver', 'data')

        interfaces = (relay.Node, )

    def resolve_name(self, info):
        return self.safe_translation_getter('name', any_language=True)


class DebtDjangoObjectType(DjangoObjectType):
    total_price = Decimal()

    class Meta:
        model = Debt
        fields = '__all__'


class PaymentDjangoObjectType(DjangoObjectType):
    class Meta:
        model = Payment
        fields = '__all__'
