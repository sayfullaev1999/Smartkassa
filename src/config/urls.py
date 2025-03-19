from django.urls import path, include
from smartkassa.admin import admin_site


urlpatterns = [
    path("admin/", admin_site.urls),
    path("api/", include("integrations.urls")),
]
