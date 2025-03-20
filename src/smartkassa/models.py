from django.db import models

from .utils import parse_birth_date
from .validators import validate_inn


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True


class Client(BaseModel):
    inn = models.CharField(max_length=14, unique=True, verbose_name="СТИР", validators=[validate_inn])
    name = models.CharField(max_length=255, verbose_name="Имя пользователя")
    pinfl = models.CharField(max_length=14, blank=True, null=True, verbose_name="ПИНФЛ")
    phone = models.CharField(max_length=13, verbose_name="Телефон", null=True, blank=True)
    bank_name = models.CharField(max_length=255, verbose_name="Банк")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    date_birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def clean(self):
        if self.phone:
            self.phone = self.phone.strip().replace(" ", "")  # Remove spaces

            if self.phone.startswith("998") and len(self.phone) == 12:
                self.phone = f"+{self.phone}"
            elif len(self.phone) == 9 and self.phone.isdigit():
                self.phone = f"+998{self.phone}"

    def save(self, *args, **kwargs):
        self.date_birth = parse_birth_date(self.pinfl)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.inn


class Device(BaseModel):
    OWNER_CHOICES = [
        ("bank", "Банк"),
        ("smartkassa", "Смарт-касса"),
        ("personal", "Личное"),
    ]

    name = models.CharField(max_length=255, verbose_name="Название")
    is_active = models.BooleanField(verbose_name="Активен", blank=True, default=True)
    kkm_serial_number = models.CharField(max_length=255, unique=True, verbose_name="ККМ", help_text="Контрольно-кассовая машина")
    fm_serial_number = models.CharField(max_length=255, verbose_name="ФМ", blank=True, null=True, help_text="Фиксальный память")
    owner_type = models.CharField(max_length=10, choices=OWNER_CHOICES, verbose_name="Тип владельца")
    client = models.ForeignKey(to=Client, verbose_name="Клиент", on_delete=models.CASCADE, related_name="devices", blank=True)

    class Meta:
        verbose_name = "Устройства"
        verbose_name_plural = "Устройствы"

    def __str__(self):
        return f"{self.name} ({self.kkm_serial_number})"
