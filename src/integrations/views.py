from django.core.exceptions import ValidationError
from django.http import JsonResponse

from smartkassa.validators import validate_inn
from .clients import FakturaClient
from smartkassa.utils import parse_birth_date


def get_company_info_by_inn(request, inn: str):
    try:
        validate_inn(inn)
    except ValidationError as exp:
        return JsonResponse({"success": False, "error": str(exp.message)})

    faktura = FakturaClient()
    company_info = faktura.get_company_basic_details(inn)

    if company_info and company_info.get("CompanyInn", None):
        company_info["BirthDate"] = parse_birth_date(company_info.get("Pinfl"))
        return JsonResponse({"success": True, **company_info})
    return JsonResponse({"success": False, "error": "Не удалось найти организацию!"})
