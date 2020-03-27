from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

DRIVER_STATUS_CHOICES = (
    ('free', 'Свободен'),
    ('busy', 'Занят'),
)

PROFILE_TYPE_CHOICES = (
    ('client', 'Клиент'),
    ('driver', 'Водитель'),
)


class Profiles(models.Model):
    user = models.ForeignKey('auth.User', related_name='client', on_delete=models.CASCADE, verbose_name='Профиль')
    type = models.CharField(max_length=20, choices=PROFILE_TYPE_CHOICES, verbose_name='Тип')
    mobile_phone = PhoneNumberField(max_length=20, verbose_name='Мобильный телефон')
    country = models.CharField(max_length=30, verbose_name='Страна')
    city = models.CharField(max_length=30, verbose_name='Город')
    status = models.CharField(max_length=20, null=True, blank=True, choices=DRIVER_STATUS_CHOICES, verbose_name='Статус')
    car_model = models.CharField(max_length=50, null=True, blank=True, verbose_name='Модель авто')
    car_number = models.CharField(max_length=50, null=True, blank=True, verbose_name='Номер авто')
    car_seats = models.IntegerField(null=True, blank=True, verbose_name='Количество мест')
    notification = models.BooleanField(default=True, verbose_name='Уведомления')
    photo = models.ImageField(upload_to='users_photo', null=True, blank=True, verbose_name='Фото')

    def __str__(self):
        return self.user.first_name
