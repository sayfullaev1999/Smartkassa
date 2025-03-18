from django.db import models
from django.core.exceptions import ValidationError
from .validators import validate_inn

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True

class Client(BaseModel):
    inn = models.CharField(
        max_length=14, unique=True, verbose_name="СТИР", validators=[validate_inn]
    )
    name = models.CharField(max_length=255, verbose_name="Имя пользователя")
    pinfl = models.CharField(
        max_length=14, blank=True, unique=True, verbose_name="ПИНФЛ"
    )
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    bank_name = models.CharField(max_length=255, verbose_name="Банк")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    date_birth = models.DateField(blank=True, verbose_name="Дата рождения")
    gender = models.CharField(max_length=10, blank=True, verbose_name="Пол")

    def clean(self):
        if self.phone:
            self.phone = self.phone.strip().replace(" ", "")  # Remove spaces

            if self.phone.startswith("998") and len(self.phone) == 12:
                self.phone = f"+{self.phone}"
            elif len(self.phone) == 9 and self.phone.isdigit():
                self.phone = f"+998{self.phone}"
            elif self.phone.startswith("+998") and len(self.phone) == 13:
                pass
            else:
                raise ValidationError("Телефон должен быть в формате +998XXXXXXXXX")

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.pinfl:
            self.date_birth = self.parse_birth_date()
            self.gender = self.parse_gender()
        super().save(*args, **kwargs)

    def parse_birth_date(self):
        if not self.pinfl or len(self.pinfl) != 14 or not self.pinfl.isdigit():
            return None
        day = int(self.pinfl[1:3])
        month = int(self.pinfl[3:5])
        year_suffix = int(self.pinfl[5:7])
        year = 1900 + year_suffix if year_suffix > 30 else 2000 + year_suffix
        return f"{year}-{month:02d}-{day:02d}"

    def parse_gender(self):
        if not self.pinfl or len(self.pinfl) != 14 or not self.pinfl.isdigit():
            return None
        return "Мужской" if int(self.pinfl[-1]) % 2 else "Женский"

    def __str__(self):
        return self.name if self.name else "Без имени"
