from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import (BookListViewSet, AbstractBookViewSet, ReviewListAPIView, ReviewDetailAPIView,
                    UserProfileViewSet, UserProfileMyListsAPIView, UserProfileReadListsAPIView,
                    UserProfileMyBooksAPIView, UserProfileLibraryAPIView, RatingCreateAPIView, RatingDetailsAPIView,
                    UserProfileReviewsAPIView, UserProfileLikesAPIView, UserProfileFollowersAPIView,
                    UserProfileFollowingAPIView, BookListAPIView, UserProfileFavouritesAPIView,
                    UserProfileCurrentlyReadingAPIView, CategoryViewSet, AuthorViewSet,
                    UpDownRatingCreateAPIView, UpDownRatingDetailsAPIView )
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserProfileViewSet)
router.register('booklists', BookListViewSet)
router.register('abstractbooks', AbstractBookViewSet)
router.register('authors', AuthorViewSet)
router.register('categories', CategoryViewSet)


urlpatterns = [
    path('books/', BookListAPIView.as_view(), name="book_list"),
    path('reviews/', ReviewListAPIView.as_view(), name="review_list"),
    path('reviews/<int:pk>/', ReviewDetailAPIView.as_view(), name="review_detail"),
    path('ratings/', RatingCreateAPIView.as_view(), name="rating_list"),
    path('ratings/<int:pk>/', RatingDetailsAPIView.as_view(), name="rating_detail"),
    path('updownratings/', UpDownRatingCreateAPIView.as_view(), name="up_down_rating_list"),
    path('updownratings/<int:pk>/', UpDownRatingDetailsAPIView.as_view(), name="up_down_rating_detail"),
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
    path('', include(router.urls)),
]
