from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import SignUp, UserDetailView, UserUpdateView, UserDeleteView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', SignUp.as_view(), name='create'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('profile/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('profile/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]