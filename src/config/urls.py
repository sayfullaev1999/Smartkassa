from django.urls import path
from smartkassa.admin import admin_site


urlpatterns = [
    path("", admin_site.urls),
]
