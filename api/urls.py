from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import (BookListDetailAPIView, BookListListAPIView, AbstractBookListAPIView,
                    AbstractBookDetailAPIView, ReviewListAPIView, ReviewDetailAPIView,
                    UserProfileDetailAPIView, UserProfileMyListsAPIView, UserProfileReadListsAPIView,
                    UserProfileMyBooksAPIView, UserProfileLibraryAPIView,
                    UserProfileReviewsAPIView, UserProfileLikesAPIView, UserProfileFollowersAPIView, UserProfileListAPIView,
                    UserProfileFollowingAPIView, BookListAPIView, UserProfileFavouritesAPIView,
                    UserProfileCurrentlyReadingAPIView)
from rest_framework import routers

#router = routers.DefaultRouter()
# router.register('users', UserProfileViewSet)
# router.register('books', BookViewSet)
#router.register('detail', BookListDetailViewSet)



urlpatterns = [
    path('booklists/', BookListListAPIView.as_view(), name="booklist_list"),
    path('users/', UserProfileListAPIView.as_view(), name="users_list"),
    path('booklists/<int:pk>/', BookListDetailAPIView.as_view(), name="booklist_detail"),
    path('abstractbooks/', AbstractBookListAPIView.as_view(), name="abstractbook_list"),
    path('abstractbooks/<int:pk>/', AbstractBookDetailAPIView.as_view(), name="abstractbook_detail"),
    path('books/', BookListAPIView.as_view(), name="book_list"),
    path('reviews/', ReviewListAPIView.as_view(), name="review_list"),
    path('reviews/<int:pk>/', ReviewDetailAPIView.as_view(), name="review_detail"),
    path('users/<str:username>/', UserProfileDetailAPIView.as_view(), name="user_detail"),
    path('users/<str:username>/mylists', UserProfileMyListsAPIView.as_view(), name="user_mylists"),
    path('users/<str:username>/readlist', UserProfileReadListsAPIView.as_view(), name="user_readlist"),
    path('users/<str:username>/mybooks', UserProfileMyBooksAPIView.as_view(), name="user_mybooks"),
    path('users/<str:username>/library', UserProfileLibraryAPIView.as_view(), name="user_library"),
    path('users/<str:username>/reviews', UserProfileReviewsAPIView.as_view(), name="user_reviews"),
    path('users/<str:username>/likes', UserProfileLikesAPIView.as_view(), name="user_likes"),
    path('users/<str:username>/followers', UserProfileFollowersAPIView.as_view(), name="user_followers"),
    path('users/<str:username>/following', UserProfileFollowingAPIView.as_view(), name="user_following"),
    path('users/<str:username>/favourite_books', UserProfileFavouritesAPIView.as_view(), name="user_favourite_books"),
    path('users/<str:username>/currently_reading', UserProfileCurrentlyReadingAPIView.as_view(), name="user_current_reader"),

]
