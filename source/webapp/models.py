from django.db import models

ANNOUNCEMENT_STATUS_CHOICES = (
    ('active', 'Активный'),
    ('completed', 'Завершенный'),
)

ANNOUNEMENT_TYPE_CHOICES = (
    ('client', 'Клиент'),
    ('driver', 'Водитель'),
)
OBLASTI_CHOICES = (
    ('Bishkek', 'Бишкек'),
    ('Chui', 'Чуй'),
    ('Talas', 'Талас'),
    ('Naryn', 'Нарын'),
    ('Issykkul', 'Иссыкуль'),
    ('Osh', 'Ош'),
    ('Jalal-Abad', 'Жалал-Абад'),
    ('Batken', 'Баткен')
)


class Announcements(models.Model):
    author = models.ForeignKey('auth.User', related_name='announcement', on_delete=models.CASCADE, verbose_name='Автор')
    type = models.CharField(max_length=50, choices=ANNOUNEMENT_TYPE_CHOICES, verbose_name='Тип')
    description = models.CharField(max_length=50, null=True, blank=True, verbose_name='Описание')
    place_from = models.CharField(max_length=100, choices=OBLASTI_CHOICES, verbose_name='Откуда')
    place_to = models.CharField(max_length=100, choices=OBLASTI_CHOICES,  verbose_name='Куда')
    departure_time = models.DateTimeField(verbose_name='Когда')
    seats = models.IntegerField(verbose_name='Количество мест')
    luggage = models.CharField(null=True, blank=True, max_length=100, verbose_name='Багаж')
    car_model = models.CharField(max_length=50, null=True, blank=True, verbose_name='Модель авто')
    car_number = models.CharField(max_length=50, null=True, blank=True, verbose_name='Номер авто')
    price = models.IntegerField(null=True, blank=True, verbose_name='Цена')
    photo = models.ImageField(upload_to='ads_photo', null=True, blank=True, verbose_name='Фото')
    clients = models.ManyToManyField('auth.User', null=True, blank=True, related_name='experts',
                                     verbose_name='Область аккредитации')
    status = models.CharField(max_length=50, choices=ANNOUNCEMENT_STATUS_CHOICES, verbose_name='Статус')

    def __str__(self):
        return self.description
