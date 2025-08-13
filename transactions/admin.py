from django.contrib import admin
from parler.admin import TranslatableAdmin

from transactions.models import Category, Transaction


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('name',)


@admin.register(Transaction)
class TransactionAdmin(TranslatableAdmin):
    list_display = ('name', 'receiver', 'data')
