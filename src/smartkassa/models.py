from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils import parse_birth_date
from .validators import validate_inn


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        abstract = True


class Client(BaseModel):
    inn = models.CharField(verbose_name=_("TIN"), max_length=14, unique=True, validators=[validate_inn])
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    pinfl = models.CharField(verbose_name=_("PINFL"), max_length=14, blank=True, null=True)
    phone = models.CharField(verbose_name=_("Phone"), max_length=13, null=True, blank=True)
    bank_name = models.CharField(verbose_name=_("Bank"), max_length=255)
    address = models.CharField(verbose_name=_("Address"), max_length=255)
    balance = models.DecimalField(verbose_name=_("Balance"), max_digits=20, decimal_places=2, default=0)
    date_birth = models.DateField(verbose_name=_("Date of birth"), null=True, blank=True)

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    def clean(self):
        if self.phone:
            self.phone = self.phone.strip().replace(" ", "")

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
        ("bank", _("Bank")),
        ("smartkassa", _("Smart Kassa")),
        ("personal", _("Personal")),
    ]

    name = models.CharField(verbose_name=_("Name"), max_length=255)
    is_active = models.BooleanField(verbose_name=_("Active"), blank=True, default=True)
    kkm_serial_number = models.CharField(
        verbose_name=_("KKM"), max_length=255, unique=True, help_text=_("Cash register machine")
    )
    fm_serial_number = models.CharField(
        verbose_name=_("FM"), max_length=255, blank=True, null=True, help_text=_("Fiscal memory")
    )
    owner_type = models.CharField(verbose_name=_("Owner type"), max_length=10, choices=OWNER_CHOICES)
    client = models.ForeignKey(
        verbose_name=_("Client"), to=Client, on_delete=models.CASCADE, related_name="devices", blank=True
    )

    class Meta:
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")

    def __str__(self):
        return f"{self.name} ({self.kkm_serial_number})"


class BalanceTransaction(BaseModel):
    client = models.ForeignKey(
        verbose_name=_("Client"), to=Client, on_delete=models.CASCADE, related_name="transactions"
    )
    amount = models.DecimalField(verbose_name=_("Amount"), max_digits=20, decimal_places=2)
    comment = models.CharField(verbose_name=_("Comment"), max_length=255)

    class Meta:
        verbose_name = _("Balance transaction")
        verbose_name_plural = _("Balance transactions")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client} - {self.amount}"


class Service(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Название услуги")
    description = models.TextField(blank=True, null=True, verbose_name="Описание услуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    is_active = models.BooleanField(default=True, verbose_name="Активность")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return f"{self.name} - {self.price} сум"
