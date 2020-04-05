from django.contrib.auth.models import User
from rest_framework import serializers

from accounts import models
from accounts.models import Profiles
from webapp.models import Announcements


class AnnouncementSerializer(serializers.ModelSerializer):  # Сериализатор для обявлений
    class Meta:
        model = Announcements
        fields = ('id', 'author', 'type', 'description', 'place_from', 'place_to', 'departure_time', 'seats', 'luggage',
                  'price', 'photo', 'status', 'clients')


class ProfileSerializer(serializers.ModelSerializer):  # Сериализатор для профиля
    class Meta:
        model = Profiles
        fields = ('id', 'user', 'type', 'mobile_phone', 'country', 'city', 'status', 'car', 'car_model', 'car_number',
                  'car_seats', 'notification', 'photo')
        extra_kwargs = {'user': {'read_only': True}}  # Юзер делаем только для чтения


class UserSerializer(serializers.ModelSerializer):  # Сериализатор для Юзера
    profile = ProfileSerializer(many=False)         # Добавляем сериализатор профиля и добавляем в fields

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}       # Пароль делаем для писания :-D

    def create(self, validated_data):                       # Создаем фунцию для создания, определяем метод POST
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        pof = validated_data['profile']
        profile = Profiles(
            user=user,
            type=pof['type'],
            mobile_phone=pof['mobile_phone'],
            country=pof['country'],
            city=pof['city'],
            status=pof['status'],
            car=pof['car'],
            car_model=pof['car_model'],
            car_number=pof['car_number'],
            car_seats=pof['car_seats'],
            notification=pof['notification'],
            photo=pof['photo']
        )
        profile.save()
        return user

    # def update(self, instance, validated_data):


