from django.contrib import admin
from .models import Device


class DeviceInline(admin.TabularInline):
    model = Device
    extra = 0
    classes = ("collapse",)

    def save_model(self, request, obj, form, change):
        if not obj.client:
            obj.client = form.instance
        super().save_model(request, obj, form, change)
