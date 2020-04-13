from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from webapp.models import Car, CarModel

DRIVER_STATUS_CHOICES = (
    ('free', 'Свободен'),
    ('busy', 'Занят'),
)

PROFILE_TYPE_CHOICES = (
    ('client', 'Клиент'),
    ('driver', 'Водитель'),
)


class Profiles(models.Model):
    user = models.OneToOneField('auth.User', related_name='profile', on_delete=models.CASCADE, verbose_name='Профиль')
    type = models.CharField(max_length=20, choices=PROFILE_TYPE_CHOICES, verbose_name='Тип')
    mobile_phone = PhoneNumberField(max_length=20, verbose_name='Мобильный телефон')
    country = models.CharField(max_length=30, null=True, blank=True, verbose_name='Страна')
    city = models.CharField(max_length=30, null=True, blank=True, verbose_name='Город')
    status = models.CharField(max_length=20, null=True, blank=True, choices=DRIVER_STATUS_CHOICES, verbose_name='Статус')
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True, related_name='profile', verbose_name='Марка авто')
    car_model = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='profile', verbose_name='Модель авто')
    car_number = models.CharField(max_length=50, null=True, blank=True, verbose_name='Номер авто')
    car_seats = models.IntegerField(null=True, blank=True, verbose_name='Количество мест')
    notification = models.BooleanField(default=True, verbose_name='Уведомления')
    photo = models.ImageField(upload_to='users_photo', null=True, blank=True, verbose_name='Фото')

    def __str__(self):
        return self.user.first_name
