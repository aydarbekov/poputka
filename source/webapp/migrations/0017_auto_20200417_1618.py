# Generated by Django 2.2 on 2020-04-17 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0016_review_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcements',
            name='car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='announcement', to='webapp.Car', verbose_name='Марка авто'),
        ),
        migrations.AddField(
            model_name='announcements',
            name='car_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='announcement', to='webapp.CarModel', verbose_name='Модель авто'),
        ),
        migrations.AlterField(
            model_name='announcements',
            name='place_from',
            field=models.CharField(choices=[('Bishkek', 'Бишкек'), ('Chui', 'Чуй'), ('Talas', 'Талас'), ('Naryn', 'Нарын'), ('Issykkul', 'Иссыкуль'), ('Osh', 'Ош'), ('Jalal-Abad', 'Ж-Абад'), ('Batken', 'Баткен')], max_length=100, verbose_name='Откуда'),
        ),
        migrations.AlterField(
            model_name='announcements',
            name='place_to',
            field=models.CharField(choices=[('Bishkek', 'Бишкек'), ('Chui', 'Чуй'), ('Talas', 'Талас'), ('Naryn', 'Нарын'), ('Issykkul', 'Иссыкуль'), ('Osh', 'Ош'), ('Jalal-Abad', 'Ж-Абад'), ('Batken', 'Баткен')], max_length=100, verbose_name='Куда'),
        ),
    ]
