from django.urls import path
from django.contrib.auth.views import LogoutView
from accounts.views import LoginView, SignUp, UserDetailView, UserUpdateView, UserDeleteView, UserPasswordChangeView, \
    UserListView, UserSearchView, SearchResultsView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', SignUp.as_view(), name='create'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('profile/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('profile/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('profile/<int:pk>/change_password/', UserPasswordChangeView.as_view(), name='user_change_password'),
    path('profile/list/', UserListView.as_view(), name='user_list'),
    path('user/search/', UserSearchView.as_view(), name='user_search'),
    path('user/search/results/', SearchResultsView.as_view(), name='search_results'),
]