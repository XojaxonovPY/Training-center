from graphene import InputObjectType, String, List, Int, Decimal, Date


class TranslationInput(InputObjectType):
    language_code = String(required=True)
    name = String()


class CategoryInputObjectType(InputObjectType):
    translation = List(TranslationInput, required=True)


class TransactionInputObject(InputObjectType):
    translation = List(TranslationInput)
    category_id = Int()
    receiver = String()
    date = Date()
    amount = Decimal()


class DebtInputObjectType(InputObjectType):
    user_id=Int()
    comment=String()
    amount=Decimal()


class PaymentInputObjectType(InputObjectType):
    amount=Decimal()
    comment=String()
    group_id=Int()
    owner_id=Int()
    count=Int()
