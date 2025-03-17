from django.contrib.admin import AdminSite
from django.contrib import admin

class CustomAdminSite(AdminSite):
    site_header = "Smart Kassa"
    site_title = "Smart Kassa"
    index_title = "Welcome to Smart Kassa Panel"

    def each_context(self, request):
        context = super().each_context(request)
        context["logo"] = "/static/logo.png"
        return context


admin_site = CustomAdminSite(name="custom_admin")
