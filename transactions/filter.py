from django_filters import FilterSet, DateFilter

from transactions.models import Transaction


class TransactionFilter(FilterSet):
    from_date = DateFilter(field_name='data', lookup_expr='gte')
    to_date = DateFilter(field_name='data', lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ('data',)
