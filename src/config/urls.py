from django.contrib import admin
from django.urls import path, include
from main.admin import admin_site


urlpatterns = [
    path("admin/", admin_site.urls),
]
