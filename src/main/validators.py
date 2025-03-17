from django.core.exceptions import ValidationError

def validate_14_digits(value):
    if not value.isdigit() or len(value) != 14:
        raise ValidationError("Должно содержать ровно 14 цифр.")
