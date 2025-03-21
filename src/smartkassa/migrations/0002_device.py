# Generated by Django 5.1.7 on 2025-03-20 11:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartkassa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Активен')),
                ('kkm_serial_number', models.CharField(help_text='Контрольно-кассовая машина', max_length=255, unique=True, verbose_name='ККМ')),
                ('fm_serial_number', models.CharField(blank=True, help_text='Фиксальный память', max_length=255, null=True, verbose_name='ФМ')),
                ('owner_type', models.CharField(choices=[('bank', 'Банк'), ('smartkassa', 'Смарт-касса'), ('personal', 'Личное')], max_length=10, verbose_name='Тип владельца')),
                ('client', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='smartkassa.client', verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Устройства',
                'verbose_name_plural': 'Устройствы',
            },
        ),
    ]
