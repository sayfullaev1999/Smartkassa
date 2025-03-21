from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from smartkassa.admin import admin_site

urlpatterns = i18n_patterns(
    path("admin/", admin_site.urls),
    path("api/", include("integrations.urls")),
    prefix_default_language=False,
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
