from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import SignUp, UserDetailView
from webapp.views import IndexView, AnnounceCreateView, AnnounceDetailView, AnnounceUpdateView, AnnounceDeleteView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('announce/create/', AnnounceCreateView.as_view(), name='announce_create'),
    path('announce/detail/<int:pk>/', AnnounceDetailView.as_view(), name='announce_detail'),
    path('announce/update/<int:pk>/', AnnounceUpdateView.as_view(), name='announce_update'),
    path('announcements/delete/<int:pk>/', AnnounceDeleteView.as_view(), name='announce_delete'),
]