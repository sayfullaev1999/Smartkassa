from django.urls import path

from .views import get_company_info_by_inn

urlpatterns = [
    path("get-company-info/<str:inn>/", get_company_info_by_inn, name="get_company_info_by_inn"),
]
