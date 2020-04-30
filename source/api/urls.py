from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api import views
from api.views import update, CarListView, CarDetailView, LogoutView, ClientsInAnnounceView

router = routers.DefaultRouter()
router.register(r'announcements', views.AnnouncementViewSet)
router.register(r'users', views.UserViewSet)

app_name = 'api/v1'

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:pk>/change_password/', update, name='password_change'),
    path('cars/', CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('logout/', LogoutView.as_view(), name='api_token_delete'),
    path('clients/', ClientsInAnnounceView.as_view(), name='client_create'),
    # path('new_posts/', SendNewPostsView.as_view(), name='post_send')
]