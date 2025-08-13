from graphene import Mutation, Field, ID
from graphene.types.generic import GenericScalar
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from parler.utils.context import switch_language

from apps.permission import is_admin
from transactions.models import Category, Transaction, Debt, Payment
from transactions.types import DebtInputObjectType, PaymentInputObjectType
from transactions.types import CategoryInputObjectType, TransactionInputObject
from transactions.types import DebtDjangoObjectType, PaymentDjangoObjectType
from transactions.types import TransactionDjangoObjectType, CategoryDjangoObjectType


class CategoryMutation(Mutation):
    class Arguments:
        input = CategoryInputObjectType()

    category = Field(CategoryDjangoObjectType)

    @login_required
    @is_admin
    def mutate(self, info, input: CategoryInputObjectType):
        category = Category()
        for trans in input.translation:
            lang = trans.language_code
            with switch_language(category, lang):
                category.name = trans.name
                category.save()
        return CategoryMutation(category=category)


class TransactionCreateMutation(Mutation):
    class Arguments:
        input = TransactionInputObject()

    transaction = Field(TransactionDjangoObjectType)

    @login_required
    @is_admin
    def mutate(self, info, input: TransactionInputObject):
        transaction = Transaction(
            data=input.date,
            category_id=input.category_id,
            receiver=input.receiver,
            amount=input.amount
        )

        for trans in input.translation:
            lang = trans.language_code

            with switch_language(transaction, lang):
                transaction.name = trans.name
                transaction.save()
        transaction.save()

        return TransactionCreateMutation(transaction=transaction)


class TransactionUpdateMutation(Mutation):
    class Arguments:
        pk = ID(required=True)
        input = TransactionInputObject()

    transaction = Field(TransactionDjangoObjectType)

    @login_required
    @is_admin
    def mutate(self, info, input: TransactionInputObject, pk):
        transaction = Transaction.objects.filter(pk=pk).first()
        if input.date:
            transaction.data = input.date
        if input.amount:
            transaction.amount = input.amount
        if input.receiver:
            transaction.receiver = input.receiver
        if input.amount:
            transaction.amount = input.amount
        if input.category_id:
            transaction.category_id = input.category_id
        if input.translation:
            for trans in input.translation:
                lang = trans.language_code
                with switch_language(transaction, lang):
                    transaction.name = trans.name
                    transaction.save()
        transaction.save()
        return TransactionUpdateMutation(transaction=transaction)


class TransactionDeleteMutation(Mutation):
    class Arguments:
        pk = ID(required=True)

    success = GenericScalar()

    @login_required
    @is_admin
    def mutate(self, info, pk):
        transaction = Transaction.objects.filter(pk=pk).first()
        if not transaction:
            raise GraphQLError('Transaction not found')
        transaction.delete()
        return TransactionDeleteMutation(success={'message': 'transaction delete', 'status': 205})


class DebtMutation(Mutation):
    class Arguments:
        input = DebtInputObjectType()

    debt = Field(DebtDjangoObjectType)

    def mutate(self, info, input: DebtInputObjectType):
        debt = Debt.objects.create(**input.__dict__)
        return DebtMutation(debt=debt)


class PaymentMutation(Mutation):
    class Arguments:
        input = PaymentInputObjectType(required=True)

    payment = Field(PaymentDjangoObjectType)

    def mutate(self, info, input:PaymentInputObjectType):
        payment = Payment.objects.create(**input.__dict__)
        return PaymentMutation(payment=payment)
