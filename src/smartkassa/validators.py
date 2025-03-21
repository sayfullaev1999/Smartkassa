from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_inn(value):
    if not value.isdigit():
        raise ValidationError(_("INN must contain only digits."))
    if len(value) not in [9, 14]:
        raise ValidationError(_("INN must be either 9 or 14 digits long."))
    if value.startswith("0"):
        raise ValidationError(_("INN must not start with 0."))
