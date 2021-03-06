# Generated by Django 2.2 on 2020-03-28 05:37

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200327_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiles',
            name='city',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='country',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Страна'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='mobile_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=20, null=True, region=None, verbose_name='Мобильный телефон'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='type',
            field=models.CharField(blank=True, choices=[('client', 'Клиент'), ('driver', 'Водитель')], max_length=20, null=True, verbose_name='Тип'),
        ),
    ]
