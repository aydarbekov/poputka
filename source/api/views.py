from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import AnnouncementSerializer, UserSerializer, CarSerializer
from webapp.models import Announcements, Car


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcements.objects.all()
    serializer_class = AnnouncementSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def perform_create(self, serializer):
        serializer.save(photo=self.request.data.get('photo'))


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


class CarDetailView(APIView):
    def get(self, request, *args, **kwargs):
        car = Car.objects.get(pk=kwargs['pk'])
        serializer = CarSerializer(car, many=False)
        return Response({"car": serializer.data})