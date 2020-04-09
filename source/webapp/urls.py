from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import SignUp, UserDetailView
from webapp.views import IndexView, AnnounceCreateView, AnnounceDetailView, AnnounceUpdateView, AnnounceDeleteView, \
    PassengersList, DriversList, ClientAddView, ClientDeleteView, ReviewCreateView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('passengers/', PassengersList.as_view(), name="passengers_list"),
    path('drivers/', DriversList.as_view(), name="drivers_list"),
    path('announce/create/', AnnounceCreateView.as_view(), name='announce_create'),
    path('announce/detail/<int:pk>/', AnnounceDetailView.as_view(), name='announce_detail'),
    path('announce/update/<int:pk>/', AnnounceUpdateView.as_view(), name='announce_update'),
    path('announcements/delete/<int:pk>/', AnnounceDeleteView.as_view(), name='announce_delete'),
    path('client/add/', ClientAddView.as_view(), name='client_add'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('review/add/<int:pk>/', ReviewCreateView.as_view(), name='review_create')
]