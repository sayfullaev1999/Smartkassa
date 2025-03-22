from django.contrib import admin
from .models import Device, ClientService


class DeviceInline(admin.TabularInline):
    model = Device
    extra = 0
    classes = ("collapse",)


class ClientServiceInline(admin.TabularInline):
    model = ClientService
    extra = 0
    classes = ("collapse",)
    fields = ("service",)
    readonly_fields = ("created_at",)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
