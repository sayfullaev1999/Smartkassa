from django.db import models

from .utils import parse_birth_date
from .validators import validate_inn


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True


class Client(BaseModel):
    inn = models.CharField(verbose_name="СТИР", max_length=14, unique=True, validators=[validate_inn])
    name = models.CharField(verbose_name="Имя пользователя", max_length=255)
    pinfl = models.CharField(verbose_name="ПИНФЛ", max_length=14, blank=True, null=True)
    phone = models.CharField(verbose_name="Телефон", max_length=13, null=True, blank=True)
    bank_name = models.CharField(verbose_name="Банк", max_length=255)
    address = models.CharField(verbose_name="Адрес", max_length=255)
    balance = models.DecimalField(verbose_name="Баланс", max_digits=20, decimal_places=2, default=0)
    date_birth = models.DateField(verbose_name="Дата рождения", null=True, blank=True)

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

    name = models.CharField(verbose_name="Название", max_length=255)
    is_active = models.BooleanField(verbose_name="Активен", blank=True, default=True)
    kkm_serial_number = models.CharField(
        verbose_name="ККМ", max_length=255, unique=True, help_text="Контрольно-кассовая машина"
    )
    fm_serial_number = models.CharField(
        verbose_name="ФМ", max_length=255, blank=True, null=True, help_text="Фиксальный память"
    )
    owner_type = models.CharField(verbose_name="Тип владельца", max_length=10, choices=OWNER_CHOICES)
    client = models.ForeignKey(
        verbose_name="Клиент", to=Client, on_delete=models.CASCADE, related_name="devices", blank=True
    )

    class Meta:
        verbose_name = "Устройства"
        verbose_name_plural = "Устройствы"

    def __str__(self):
        return f"{self.name} ({self.kkm_serial_number})"


class BalanceTransaction(BaseModel):
    client = models.ForeignKey(verbose_name="Клиент", to=Client, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(verbose_name="Сумма", max_digits=20, decimal_places=2)
    comment = models.CharField(verbose_name="Комментарий", max_length=255)

    class Meta:
        verbose_name = "Транзакция по счету клиента"
        verbose_name_plural = "Транзакции по счету клиентов"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client} - {self.amount}"
