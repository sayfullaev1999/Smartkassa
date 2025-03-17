from django.db import models
from .validators import validate_14_digits
from .utils import extract_birthdate_and_gender
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True


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