from django.db import models

ANNOUNCEMENT_STATUS_CHOICES = (
    ('active', 'Активный'),
    ('completed', 'Завершенный'),
)

ANNOUNCEMENT_TYPE_CHOICES = (
    ('client', 'Клиент'),
    ('driver', 'Водитель'),
)

REGION_CHOICES = (
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
    type = models.CharField(max_length=50, choices=ANNOUNCEMENT_TYPE_CHOICES, verbose_name='Тип')
    description = models.CharField(max_length=50, null=True, blank=True, verbose_name='Описание')
    place_from = models.CharField(max_length=100, choices=REGION_CHOICES, verbose_name='Откуда')
    place_to = models.CharField(max_length=100, choices=REGION_CHOICES, verbose_name='Куда')
    departure_time = models.DateTimeField(verbose_name='Когда')
    seats = models.IntegerField(verbose_name='Количество мест')
    luggage = models.CharField(null=True, blank=True, max_length=100, verbose_name='Багаж')
    # car_model = models.CharField(max_length=50, null=True, blank=True, verbose_name='Модель авто')
    # car_number = models.CharField(max_length=50, null=True, blank=True, verbose_name='Номер авто')
    price = models.IntegerField(null=True, blank=True, verbose_name='Цена')
    photo = models.ImageField(upload_to='ads_photo', null=True, blank=True, verbose_name='Фото')
    status = models.CharField(max_length=50, choices=ANNOUNCEMENT_STATUS_CHOICES, verbose_name='Статус')
    clients = models.ManyToManyField('auth.User', through='ClientsInAnnounce', related_name='clients', verbose_name='Клиенты')

    def __str__(self):
        return str(self.author) + f'{self.place_from} - {self.place_to}'


class ClientsInAnnounce(models.Model):
    announcement = models.ForeignKey('Announcements', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    seats = models.IntegerField()


class Car(models.Model):
    mark = models.CharField(null=True, blank=True, max_length=100, verbose_name='Марка авто')

    def __str__(self):
        return self.mark


class CarModel(models.Model):
    mark = models.ForeignKey('Car', related_name='model', max_length=100, on_delete=models.CASCADE, verbose_name='Марка авто')
    model = models.CharField(max_length=100, verbose_name='Модель авто')

    def __str__(self):
        return f'{self.mark} - {self.model}'


class Review(models.Model):
    user = models.ForeignKey('auth.User', related_name='user_review', on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(max_length=500, verbose_name='Отзыв')

    def __str__(self):
        return self.text