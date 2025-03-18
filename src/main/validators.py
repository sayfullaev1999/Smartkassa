from django.core.exceptions import ValidationError

def validate_inn(value):
    if not value.isdigit():
        raise ValidationError("ИНН должен содержать только цифры.")
    if len(value) != 14:
        raise ValidationError("ИНН должен содержать ровно 14 цифр.")
    if value.startswith("0"):
        raise ValidationError("ИНН не должен начинаться с 0.")
