# Generated by Django 2.2 on 2020-03-27 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20200327_1127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcements',
            name='car_model',
        ),
        migrations.RemoveField(
            model_name='announcements',
            name='car_number',
        ),
    ]