from django.urls import path, include

from knox.views import LogoutView

from .views import UserListAPI, UserDetailAPI, LoginAPI, RegisterAPI

from rest_framework import routers
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('users/', UserListAPI.as_view()),
    path('users/<str:username>/', UserDetailAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('register/', RegisterAPI.as_view()),
    ]
