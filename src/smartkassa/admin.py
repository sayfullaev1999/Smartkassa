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


class ClientAdmin(admin.ModelAdmin):
    search_fields = ("inn", "name", "pinfl", "phone")

    class Media:
        js = ("admin/js/client_auto_fill.js",)


class DeviceAdmin(admin.ModelAdmin):
    pass


admin_site = SmartKassaAdminSite(name="smartkassa")
admin_site.register(Client, ClientAdmin)
admin_site.register(Device, DeviceAdmin)
