from django.conf import settings
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.http import JsonResponse
from phonenumber_field.phonenumber import to_python, PhoneNumber
from rest_framework import serializers
from rest_framework.response import Response
from accounts import models
from accounts.models import Profiles
from webapp.models import Announcements, Car, CarModel, ClientsInAnnounce


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
        try:
            photo = pof['photo']
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
        except:
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
            )
        profile.save()
        return user

    def update(self, instance, validated_data):
        user = instance
        if user.username != validated_data['username']:
            user.username = validated_data['username']
        if user.first_name != validated_data['first_name']:
            user.first_name = validated_data['first_name']
        if user.last_name != validated_data['last_name']:
            user.last_name = validated_data['last_name']
        if user.email != validated_data['email']:
            user.email = validated_data['email']
        user.save()
        pof = validated_data['profile']
        if user.profile.type != pof['type']:
            user.profile.type = pof['type']
        if str(user.profile.mobile_phone) != pof['mobile_phone']:  # Сразу переопределить не получилось
            user.profile.mobile_phone = None
            user.profile.mobile_phone = pof['mobile_phone']
        if user.profile.country != pof['country']:
            user.profile.country = pof['country']
        if user.profile.city != pof['city']:
            user.profile.city = pof['city']
        if user.profile.status != pof['status']:
            user.profile.status = pof['status']
        if user.profile.car != pof['car']:
            user.profile.car = pof['car']
        if user.profile.car_model != pof['car_model']:
            user.profile.car_model = pof['car_model']
        if user.profile.car_number != pof['car_number']:
            user.profile.car_number = pof['car_number']
        if user.profile.car_seats != pof['car_seats']:
            user.profile.car_seats = pof['car_seats']
        if user.profile.notification != pof['notification']:
            user.profile.notification = pof['notification']
        try:
            photo = pof['photo']
            user.profile.photo = photo
        except:
            user.profile.photo = None
        user.profile.save()
        return user


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=32)
    password_old = serializers.CharField(max_length=32)


class CarModelSerializer(serializers.ModelSerializer):  # Сериализатор для моделей
    class Meta:
        model = CarModel
        fields = ('id', 'mark', 'model')


class CarSerializer(serializers.ModelSerializer):  # Сериализатор для Юзера
    model = CarModelSerializer(many=True)         # Добавляем сериализатор профиля и добавляем в fields

    class Meta:
        model = Car
        fields = ('id', 'mark', 'model')


class ClientsInAnnounceSerializer(serializers.ModelSerializer):  # Сериализатор для клиентов
    class Meta:
        model = ClientsInAnnounce
        fields = ('id', 'announcement', 'user', 'seats')
