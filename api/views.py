from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication, TokenAuthentication


from . import serializers
from . import models




class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     """Handle creating and updating profiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    lookup_field = 'username'
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ['name', 'email', 'username']

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfile.objects.filter(username=user_name)
        return user


class UserProfileListAPIView(generics.ListCreateAPIView):

    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileListSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = [AllowAny]

    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    search_fields = ['first_name', 'email', 'username']
    # ordering = ['first_name']


class UserProfileMyListsAPIView(generics.ListCreateAPIView):

    queryset = models.BookList.objects.all()
    serializer_class = serializers.BookListListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfile.objects.get(username=user_name)
        booklist = models.BookList.objects.filter(user=user.id)
        return booklist


class UserProfileReadListsAPIView(generics.ListCreateAPIView):

    queryset = models.AbstractBook.objects.all()
    serializer_class = serializers.AbstractBookListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfile.objects.get(username=user_name)
        books = models.AbstractBook.objects.filter(wisher=user.id)
        return books

class UserProfileMyBooksAPIView(generics.ListCreateAPIView):

    queryset = models.AbstractBook.objects.all()
    serializer_class = serializers.AbstractBookListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfile.objects.get(username=user_name)
        books = models.AbstractBook.objects.filter(reader=user.id)
        return books
class UserProfileLibraryAPIView(generics.ListCreateAPIView):

    queryset = models.AbstractBook.objects.all()
    serializer_class = serializers.AbstractBookListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfile.objects.get(username=user_name)
        books = models.AbstractBook.objects.filter(owner=user.id)
        return books
class UserProfileReviewsAPIView(generics.ListCreateAPIView):

    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfile.objects.get(username=user_name)
        reviews = models.Review.objects.filter(user=user.id)
        return reviews


class UserProfileLikesAPIView(generics.ListCreateAPIView):

    queryset = models.BookList.objects.all()
    serializer_class = serializers.BookListListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfile.objects.get(username=user_name)
        book_lists = models.BookList.objects.filter(listLiker=user.id)
        return book_lists


class UserProfileFollowersAPIView(generics.ListCreateAPIView):

    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfile.objects.get(username=user_name)
        followers = models.UserProfile.objects.filter(followings=user.id)
        return followers

class UserProfileFollowingAPIView(generics.ListCreateAPIView):

    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfile.objects.get(username=user_name)
        following = models.UserProfile.objects.filter(followers=user.id)
        return following

class UserProfileFavouritesAPIView(generics.ListCreateAPIView):

    queryset = models.AbstractBook.objects.all()
    serializer_class = serializers.AbstractBookListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfile.objects.get(username=user_name)
        favourites = models.AbstractBook.objects.filter(bookLiker=user.id)
        return favourites
class UserProfileCurrentlyReadingAPIView(generics.ListCreateAPIView):

    queryset = models.AbstractBook.objects.all()
    serializer_class = serializers.AbstractBookListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfile.objects.get(username=user_name)
        currently_reading = models.AbstractBook.objects.filter(current_readers=user.id)
        return currently_reading

class BookListListAPIView(generics.ListCreateAPIView):

    queryset = models.BookList.objects.all()
    serializer_class = serializers.BookListListSerializer


class BookListDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = serializers.BookListDetailSerializer
    queryset = models.BookList.objects.all()

    def get_queryset(self):
        booklist_pk = self.kwargs['pk']
        booklist = models.BookList.objects.filter(pk=booklist_pk)
        return booklist


class AbstractBookListAPIView(generics.ListCreateAPIView):

    queryset = models.AbstractBook.objects.all()
    serializer_class = serializers.AbstractBookListSerializer


class AbstractBookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = serializers.AbstractBookDetailSerializer
    queryset = models.AbstractBook.objects.all()

    def get_queryset(self):
        book_id = self.kwargs['pk']
        return models.AbstractBook.objects.filter(pk=book_id)


class BookListAPIView(generics.ListCreateAPIView):

    serializer_class = serializers.BookSerializer
    queryset = models.Book.objects.all()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
          "book": 'serializers.BookSerializer(user, context=self.get_serializer_context()).data',
        })


class ReviewListAPIView(generics.ListCreateAPIView):

    serializer_class = serializers.ReviewSerializer
    queryset = models.Review.objects.all()


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = serializers.ReviewSerializer
    queryset = models.Review.objects.all()

    def get_queryset(self):
        review_id = self.kwargs['pk']
        return models.Review.objects.filter(pk=review_id)

# Create your views here.
