import datetime

from django.db import models
from django.core.exceptions import ValidationError
from .validators import validate_inn


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True


class Client(BaseModel):
    class Genders(models.TextChoices):
        MALE = 'M'
        FEMALE = 'Ж'

    inn = models.CharField(max_length=14, unique=True, verbose_name="СТИР", validators=[validate_inn])
    name = models.CharField(max_length=255, verbose_name="Имя пользователя")
    pinfl = models.CharField(max_length=14, blank=True, unique=True, verbose_name="ПИНФЛ")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    bank_name = models.CharField(max_length=255, verbose_name="Банк")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    date_birth = models.DateField(blank=True, verbose_name="Дата рождения")
    gender = models.CharField(max_length=1, choices=Genders.choices, blank=True, verbose_name="Пол")

    def clean(self):
        if self.phone:
            self.phone = self.phone.strip().replace(" ", "")  # Remove spaces

            if self.phone.startswith("998") and len(self.phone) == 12:
                self.phone = f"+{self.phone}"
            elif len(self.phone) == 9 and self.phone.isdigit():
                self.phone = f"+998{self.phone}"

    def save(self, *args, **kwargs):
        self.date_birth = self.parse_birth_date()
        self.gender = self.parse_gender()
        super().save(*args, **kwargs)

    def parse_birth_date(self):
        """https://lex.uz/docs/444922"""
        if self.pinfl:
            century_index = int(self.pinfl[0])
            day = int(self.pinfl[1:3])
            month = int(self.pinfl[3:5])
            year_offset = int(self.pinfl[5:7])

            if century_index in [1, 2]:
                year = 1800 + year_offset
            elif century_index in [3, 4]:
                year = 1900 + year_offset
            elif century_index in [5, 6]:
                year = 2000 + year_offset
            else:
                raise ValueError("Некорректный индекс века в ПИНФЛ")

            try:
                birthdate = datetime.date(year, month, day)
            except ValueError:
                raise ValueError("Некорректная дата рождения в ПИНФЛ")

            return birthdate.strftime("%Y-%m-%d")

    def parse_gender(self):
        if self.pinf:
            return self.Genders.MALE if int(self.pinfl[0]) % 2 else self.Genders.FEMALE

    def __str__(self):
        return self.inn
