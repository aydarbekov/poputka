# Generated by Django 2.2 on 2020-03-27 11:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20200326_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcements',
            name='clients',
            field=models.ManyToManyField(blank=True, null=True, related_name='clients', to=settings.AUTH_USER_MODEL, verbose_name='Клиенты'),
        ),
    ]
