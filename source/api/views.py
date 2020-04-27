from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from webapp.parser import new_data
from api import serializers
from api.serializers import AnnouncementSerializer, UserSerializer, CarSerializer, ClientsInAnnounceSerializer
from webapp.models import Announcements, Car, ClientsInAnnounce


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcements.objects.all()
    serializer_class = AnnouncementSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def perform_create(self, serializer):
        serializer.save(photo=self.request.data.get('photo'))

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return super().get_permissions()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def perform_create(self, serializer):
        serializer.save(photo=self.request.data.get('photo'))


@api_view(['PATCH'])
def update(request, *args, **kwargs):
    if request.method == 'PATCH':
        user = User.objects.get(pk=kwargs['pk'])
        password = request.data['password']
        password_old = request.data['password_old']
        if not user.check_password(password_old):
            return Response({"error": "Old password dont match!"})
        user.set_password(password)
        user.save()
        return Response({"sucsess": "password changed!"})
    return Response({"error": "Metod false!"})


class CarListView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []

        return super().get_permissions()


class CarDetailView(APIView):
    def get(self, request, *args, **kwargs):
        car = Car.objects.get(pk=kwargs['pk'])
        serializer = CarSerializer(car, many=False)
        return Response({"car": serializer.data})

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return super().get_permissions()


class LogoutView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user.auth_token.delete()
        return Response({'status': 'ok'})


class ClientsInAnnounceView(APIView):
    def post(self, request, *args, **kwargs):
        announce = Announcements.objects.get(pk=request.data['announcement'])
        user = User.objects.get(pk=request.data['user'])

        try:
            ClientsInAnnounce.objects.get(announcement=announce, user=user)
            return Response({'status': 'error'})
            # raise TypeError('user already client')
        except ClientsInAnnounce.DoesNotExist:
            client = ClientsInAnnounce(
                announcement=announce,
                user=user,
                seats=request.data['seats'],
            )
            client.save()
            # print(validated_data['announcement'])
            announce.seats -= request.data['seats']
            if announce.seats == 0:
                announce.status = 'completed'
            announce.save()
            client = serializers.serialize('json', [client])
            return Response({"client": client})

    def delete(self, request, *args, **kwargs):
        announce = Announcements.objects.get(pk=request.data['announcement'])
        user = User.objects.get(pk=request.data['user'])
        client = ClientsInAnnounce.objects.get(announcement=announce, user=user)
        seat = client.seats
        client.delete()
        announce.seats += seat
        if announce.seats >= 1:
            announce.status = 'active'
        announce.save()
        client = serializers.serialize('json', [client])
        return Response({"status": "success"})


class SendNewPostsView(APIView):
    def get(self, request, *args, **kwargs):
        posts = []
        for post in new_data:
            posts.append(post)
        new_data.clear()
        return Response({"Announces": posts})
