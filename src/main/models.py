from django.core.exceptions import ValidationError
from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True


def validate_14_digits(value):
    if not value.isdigit() or len(value) != 14:
        raise ValidationError("Должно содержать ровно 14 цифр.")


def extract_birthdate_and_gender(pinfl):
    if len(pinfl) != 14 or not pinfl.isdigit():
        return None, None

    day = int(pinfl[1:3])
    month = int(pinfl[3:5])
    year_suffix = int(pinfl[5:7])

    year = 1900 + year_suffix if year_suffix > 30 else 2000 + year_suffix

    try:
        birthdate = f"{year}-{month:02d}-{day:02d}"
    except ValueError:
        return None, None

    gender = "Мужской" if int(pinfl[-1]) % 2 else "Женский"

    return birthdate, gender


class Client(BaseModel):
    inn = models.CharField(
        max_length=14, unique=True, verbose_name="СТИР", validators=[validate_14_digits]
    )
    name = models.CharField(max_length=255, verbose_name="Имя пользователя")
    pinfl = models.CharField(
        max_length=14, blank=True, unique=True, verbose_name="ПИНФЛ", validators=[validate_14_digits]
    )
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    bank_name = models.CharField(max_length=255, verbose_name="Банк")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    date_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    gender = models.CharField(max_length=10, blank=True, verbose_name="Пол")

    def save(self, *args, **kwargs):
        if self.pinfl:
            self.date_birth, self.gender = extract_birthdate_and_gender(self.pinfl)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name