from django.contrib import admin


class BalanceFilter(admin.SimpleListFilter):
    title = "Баланс"
    parameter_name = "balance"

    def lookups(self, request, model_admin):
        return [
            ('positive', 'С положительным балансом'),
            ('negative', 'С отрицательным балансом'),
            ('zero', 'С нулевым балансом'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'positive':
            return queryset.filter(balance__gt=0)
        if self.value() == 'negative':
            return queryset.filter(balance__lt=0)
        if self.value() == 'zero':
            return queryset.filter(balance=0)
        return queryset
