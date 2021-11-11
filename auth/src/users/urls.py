from django.urls import path

from users.views import (
    UserDeleteView,
    UserEditView,
    UserListView,
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
)


app_name = 'users'

urlpatterns = [
    path(
        'login/',
        UserLoginView.as_view(),
        name='login',
    ),
    path(
        'logout/',
        UserLogoutView.as_view(),
        name='logout',
    ),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('<int:user_id>/edit/', UserEditView.as_view(), name='edit'),
    path('<int:user_id>/delete/', UserDeleteView.as_view(), name='delete'),
    path('', UserListView.as_view(), name='list'),
]
