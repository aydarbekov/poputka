from django.urls import path, include
from rest_framework import routers

from api import views
from api.views import update, CarListView, CarDetailView

router = routers.DefaultRouter()
router.register(r'announcements', views.AnnouncementViewSet)
router.register(r'users', views.UserViewSet)


app_name = 'api/v1'

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:pk>/change_password/', update, name='password_change'),
    path('cars/', CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail')
]