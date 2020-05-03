from django.urls import path, include
from .views import UserListAPI, UserDetailAPI, LoginAPI, RegisterAPI, PasswordChangeAPI
from knox import views as knox_views

urlpatterns = [
    path('logout/', knox_views.LogoutView.as_view(), name = "knox_logout"),
    path('users/', UserListAPI.as_view(), name = "users-list"),
    path('users/<str:username>/', UserDetailAPI.as_view(), name = "users-detail"),
    path('login/', LoginAPI.as_view(), name = "login"),
    path('register/', RegisterAPI.as_view(), name = "register"),
    path('password-change/', PasswordChangeAPI.as_view(), name = "password-change"),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    ]

#from django_rest_passwordreset import urls