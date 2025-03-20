from django.contrib import admin
from .models import Client, Device


class SmartKassaAdminSite(admin.AdminSite):
    site_header = "Smart Kassa"
    site_title = "Smart Kassa"
    index_title = "Welcome to Smart Kassa"

    def each_context(self, request):
        context = super().each_context(request)
        context["logo"] = "/static/logo.png"
        return context


class DeviceInline(admin.TabularInline):
    model = Device
    extra = 0

    def save_model(self, request, obj, form, change):
        if not obj.client:
            obj.client = form.instance
        super().save_model(request, obj, form, change)


class ClientAdmin(admin.ModelAdmin):
    list_display = ("inn", "name", "pinfl", "phone", "bank_name", "address")
    search_fields = ("inn", "name", "pinfl", "phone", "bank_name", "address")
    inlines = [DeviceInline]

    class Media:
        js = ("admin/js/client_auto_fill.js",)


class DeviceAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    list_display = ("name", "kkm_serial_number", "fm_serial_number", "owner_type", "client")
    list_filter = ("is_active", "owner_type")
    search_fields = ("name", "kkm_serial_number", "fm_serial_number")


admin_site = SmartKassaAdminSite(name="smartkassa")
admin_site.register(Client, ClientAdmin)
admin_site.register(Device, DeviceAdmin)
