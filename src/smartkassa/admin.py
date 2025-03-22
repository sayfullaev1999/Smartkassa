from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .filters import BalanceFilter
from .inlines import DeviceInline, ClientServiceInline
from .models import Client, Device, BalanceTransaction, Service


class SmartKassaAdminSite(admin.AdminSite):
    site_header = _("Smart Kassa")
    site_title = _("Smart Kassa")
    index_title = _("Welcome to Smart Kassa")

    def each_context(self, request):
        context = super().each_context(request)
        context["logo"] = "/static/logo.png"
        return context


class ClientAdmin(admin.ModelAdmin):
    list_display = ("inn", "name", "pinfl", "balance", "phone", "bank_name", "address", "created_at")
    search_fields = ("inn", "name", "pinfl", "phone", "bank_name", "address")
    list_filter = (BalanceFilter,)
    exclude = ("balance",)
    inlines = [DeviceInline, ClientServiceInline]

    class Media:
        js = ("admin/js/client_auto_fill.js",)


class BalanceTransactionAdmin(admin.ModelAdmin):
    list_display = ("client", "amount", "comment", "created_at")
    search_fields = ("client", "amount")
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class DeviceAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    list_display = ("name", "kkm_serial_number", "fm_serial_number", "owner_type", "client")
    list_filter = ("is_active", "owner_type")
    search_fields = ("name", "kkm_serial_number", "fm_serial_number")
    readonly_fields = ("client",)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active", "created_at")
    list_filter = ("is_active", )
    search_fields = ("name", "description")


admin_site = SmartKassaAdminSite(name="smartkassa")
admin_site.register(Client, ClientAdmin)
admin_site.register(BalanceTransaction, BalanceTransactionAdmin)
admin_site.register(Device, DeviceAdmin)
admin_site.register(Service, ServiceAdmin)
