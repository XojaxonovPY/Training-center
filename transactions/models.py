from django.db.models import CharField, Model, ForeignKey, SET_NULL, DateField, DateTimeField, IntegerField
from django.db.models.fields import DecimalField, BooleanField
from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=CharField(max_length=100)
    )

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)


class Transaction(TranslatableModel):
    translations = TranslatedFields(
        name=CharField(max_length=100)
    )
    category = ForeignKey(
        'transactions.Category',
        on_delete=SET_NULL,
        related_name='transactions',
        null=True,
        blank=True
    )
    receiver = CharField(max_length=100)
    data = DateField(db_index=True)
    created_at = DateTimeField(auto_now_add=True)
    amount = DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)


class Debt(Model):
    user = ForeignKey('apps.User', on_delete=SET_NULL, related_name='debts', null=True, blank=True)
    comment = CharField(max_length=100, null=True, blank=True)
    amount = DecimalField(max_digits=10, decimal_places=2)


class Payment(Model):
    group = ForeignKey('apps.Group', on_delete=SET_NULL, related_name='payments', null=True, blank=True)
    comment = CharField(max_length=100, null=True, blank=True)
    owner = ForeignKey('apps.User', on_delete=SET_NULL, related_name='payments', null=True, blank=True)
    count = IntegerField()
    amount = DecimalField(max_digits=10, decimal_places=2)
    created_at = DateTimeField(auto_now_add=True,null=True,blank=True)
