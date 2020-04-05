from django.urls import path, include
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'announcements', views.AnnouncementViewSet)
router.register(r'users', views.UserViewSet)


app_name = 'api/v1'

urlpatterns = [
    path('', include(router.urls)),

]