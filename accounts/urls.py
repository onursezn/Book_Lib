from django.urls import path, include

from knox.views import LogoutView

from .views import UserListAPI, UserDetailAPI, LoginAPI, RegisterAPI


urlpatterns = [
    path('users/', UserListAPI.as_view()),
    path('users/<str:username>/', UserDetailAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', LogoutView.as_view()),
    path('register/', RegisterAPI.as_view()),
    ]
