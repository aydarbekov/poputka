from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import SignUp, UserDetailView
from webapp.views import IndexView, AnnounceCreateView, AnnounceDetailView, AnnounceUpdateView, AnnounceDeleteView, \
    PassengersList, DriversList, ClientAddView, ClientDeleteView, ReviewCreateView
from rest_framework import routers
router = routers.DefaultRouter()
app_name = 'webapp'
# router.register(r'users', views.UserViewSet)
# router.register(r'^ajax/categ/$', 'proj.list.views.feeds_subcat')
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('passengers/', PassengersList.as_view(), name="passengers_list"),
    path('drivers/', DriversList.as_view(), name="drivers_list"),
    path('announcements/create/', AnnounceCreateView.as_view(), name='announce_create'),
    path('announcements/detail/<int:pk>/', AnnounceDetailView.as_view(), name='announce_detail'),
    path('announcements/update/<int:pk>/', AnnounceUpdateView.as_view(), name='announce_update'),
    path('announcements/delete/<int:pk>/', AnnounceDeleteView.as_view(), name='announce_delete'),
    path('client/add/', ClientAddView.as_view(), name='client_add'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('review/add/<int:pk>/', ReviewCreateView.as_view(), name='review_create')
]