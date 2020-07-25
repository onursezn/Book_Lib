from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import filters
from rest_framework import serializers as restSerializers
from knox.auth import TokenAuthentication
from rest_framework.decorators import action
from django.db.models import Avg
from django.forms.models import model_to_dict

from . import serializers
from . import models
from . import mixins
from . import permissions


class UserProfileViewSet(mixins.ListDetailSerializerMixin, viewsets.ModelViewSet):
#     """Handle creating and updating profiles"""

    list_serializer_class = serializers.UserProfileAPIListSerializer
    detail_serializer_class = serializers.UserProfileAPISerializer
    queryset = models.UserProfileAPI.objects.all()
    lookup_field = 'username'
    authentication_classes = (TokenAuthentication, )
    permission_classes_by_action = {
        'create': [IsAdminUser],
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'update': [permissions.IsOwnProfileOrReadOnly],
        'partial_update': [permissions.IsOwnProfileOrReadOnly],
        'destroy': [permissions.IsOwnProfileOrReadOnly],
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    @action(detail=True, methods=['PUT'])
    def follow(self, request, username=None):

        try:
            followed = models.UserProfileAPI.objects.get(username=username)
            user = request.user.userprofileapi
            followed.followers.add(user)
            followed.save()
            response = {'message': 'User is followed'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'User cannot be followed'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['PUT'])
    def unfollow(self, request, username=None):
        try:
            followed = models.UserProfileAPI.objects.get(username=username)
            user = request.user.userprofileapi
            followed.followers.remove(user)
            followed.save()
            response = {'message': 'User is unfollowed'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'User cannot be unfollowed'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserProfileListAPIView(generics.ListAPIView):     # search/filter nedeniyle ihtiyacımız olursa diye silmedim

    queryset = models.UserProfileAPI.objects.all()
    serializer_class = serializers.UserProfileAPIListSerializer
    authentication_classes = (TokenAuthentication, )

    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    search_fields = ['first_name', 'email', 'username']


class UserProfileMyListsAPIView(generics.ListAPIView):

    queryset = models.BookList.objects.all()
    serializer_class = serializers.BookListListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfileAPI.objects.get(username=user_name)
        booklist = models.BookList.objects.filter(user=user.id)
        return booklist


class UserProfileReadListsAPIView(generics.ListAPIView):

    queryset = models.AbstractBook.objects.all()
    serializer_class = serializers.AbstractBookListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfileAPI.objects.get(username=user_name)
        books = models.AbstractBook.objects.filter(wisher=user.id)
        return books


class UserProfileMyBooksAPIView(generics.ListAPIView):

    queryset = models.AbstractBook.objects.all()
    serializer_class = serializers.AbstractBookListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfileAPI.objects.get(username=user_name)
        books = models.AbstractBook.objects.filter(reader=user.id)
        return books


class UserProfileLibraryAPIView(generics.ListAPIView):

    queryset = models.AbstractBook.objects.all()
    serializer_class = serializers.AbstractBookListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfileAPI.objects.get(username=user_name)
        books = models.AbstractBook.objects.filter(owner=user.id)
        return books


class UserProfileReviewsAPIView(generics.ListAPIView):

    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfileAPI.objects.get(username=user_name)
        reviews = models.Review.objects.filter(user=user.id)
        return reviews


class UserProfileLikesAPIView(generics.ListAPIView):

    queryset = models.BookList.objects.all()
    serializer_class = serializers.BookListListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfileAPI.objects.get(username=user_name)
        book_lists = models.BookList.objects.filter(listLiker=user.id)
        return book_lists


class UserProfileFollowersAPIView(generics.ListAPIView):

    queryset = models.UserProfileAPI.objects.all()
    serializer_class = serializers.UserProfileAPIListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfileAPI.objects.get(username=user_name)
        followers = models.UserProfileAPI.objects.filter(followings=user.id)
        return followers


class UserProfileFollowingAPIView(generics.ListAPIView):

    queryset = models.UserProfileAPI.objects.all()
    serializer_class = serializers.UserProfileAPIListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfileAPI.objects.get(username=user_name)
        following = models.UserProfileAPI.objects.filter(followers=user.id)
        return following


class UserProfileFavouritesAPIView(generics.ListAPIView):

    queryset = models.AbstractBook.objects.all()
    serializer_class = serializers.AbstractBookListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfileAPI.objects.get(username=user_name)
        favourites = models.AbstractBook.objects.filter(bookLiker=user.id)
        return favourites


class UserProfileCurrentlyReadingAPIView(generics.ListAPIView):

    queryset = models.AbstractBook.objects.all()
    serializer_class = serializers.AbstractBookListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user_name = self.kwargs['username']
        user = models.UserProfileAPI.objects.get(username=user_name)
        currently_reading = models.AbstractBook.objects.filter(current_readers=user.id)
        return currently_reading


class BookListViewSet(mixins.ListDetailSerializerMixin, viewsets.ModelViewSet):

    queryset = models.BookList.objects.all()
    list_serializer_class = serializers.BookListListSerializer
    detail_serializer_class = serializers.BookListDetailSerializer
    permission_classes_by_action = {
        'create': [permissions.IsAuthenticatedOrReadOnly],
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'update': [permissions.IsOwnerOrReadOnly],
        'partial_update': [permissions.IsOwnerOrReadOnly],
        'destroy': [permissions.IsOwnerOrReadOnly],
    }

    def perform_create(self, serializer):

        request_user = self.request.user.userprofileapi
        if request_user.my_lists.filter(name=self.request.data["name"]).exists():
            raise restSerializers.ValidationError("You have a list with the same name!")

        serializer.save(user=request_user)

    @action(detail=True, methods=['PUT'])
    def like_list(self, request, pk=None):

        try:
            list = models.BookList.objects.get(id=pk)
            user = request.user.userprofileapi
            list.listLiker.add(user)
            list.save()
            response = {'message': 'You liked the list'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'List cannot be liked'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def unlike_list(self, request, pk=None):
        try:
            list = models.BookList.objects.get(id=pk)
            user = request.user.userprofileapi
            list.listLiker.remove(user)
            list.save()
            response = {'message': 'You unliked the list'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'List cannot be unliked'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class AbstractBookViewSet(mixins.ListDetailSerializerMixin, viewsets.ModelViewSet):

    queryset = models.AbstractBook.objects.annotate(avg_rating=Avg('ratings__stars'))
    list_serializer_class = serializers.AbstractBookListSerializer
    detail_serializer_class = serializers.AbstractBookDetailSerializer
    permission_classes_by_action = {
        'create': [IsAdminUser],
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'update': [IsAdminUser],
        'partial_update': [IsAdminUser],
        'destroy': [IsAdminUser],
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    @action(detail=True, methods=['PUT'])
    def add_to_booklist(self, request, pk=None):
        if 'booklist' in request.data:

            try:
                booklist = models.BookList.objects.get(id=request.data['booklist'])
                book = models.AbstractBook.objects.get(id=pk)
                book.book_lists.add(booklist)
                book.save()
                response = {'message': 'You added book to the list'}
                return Response(response, status=status.HTTP_200_OK)
            except:
                response = {'message': 'Book cannot be added'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:

            response = {'message': 'You need to provide a list'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def remove_from_booklist(self, request, pk=None):
        if 'booklist' in request.data:

            try:
                booklist = models.BookList.objects.get(id=request.data['booklist'])
                book = models.AbstractBook.objects.get(id=pk)
                book.book_lists.remove(booklist)
                book.save()
                response = {'message': 'You removed book from the list'}
                return Response(response, status=status.HTTP_200_OK)
            except:
                response = {'message': 'Book cannot be removed'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:

            response = {'message': 'You need to provide a list'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def add_to_my_books(self, request, pk=None):

        try:
            book = models.AbstractBook.objects.get(id=pk)
            user = request.user.userprofileapi
            book.reader.add(user)
            book.save()
            response = {'message': 'You added book to your books'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'Book cannot be added'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def remove_from_my_books(self, request, pk=None):

        try:
            book = models.AbstractBook.objects.get(id=pk)
            user = request.user.userprofileapi
            book.reader.remove(user)
            book.save()
            response = {'message': 'You removed book from your books'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'Book cannot be removed'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def add_to_favorite_books(self, request, pk=None):

        try:
            book = models.AbstractBook.objects.get(id=pk)
            user = request.user.userprofileapi
            book.bookLiker.add(user)
            book.save()
            response = {'message': 'You added book to your favorites'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'Book cannot be added'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def remove_from_favorite_books(self, request, pk=None):

        try:
            book = models.AbstractBook.objects.get(id=pk)
            user = request.user.userprofileapi
            book.bookLiker.remove(user)
            book.save()
            response = {'message': 'You removed book from your favorites'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'Book cannot be removed'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def add_to_library(self, request, pk=None):

        try:
            book = models.AbstractBook.objects.get(id=pk)
            user = request.user.userprofileapi
            book.owner.add(user)
            book.save()
            response = {'message': 'You added book to your library'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'Book cannot be added'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def remove_from_library(self, request, pk=None):

        try:
            book = models.AbstractBook.objects.get(id=pk)
            user = request.user.userprofileapi
            book.owner.remove(user)
            book.save()
            response = {'message': 'You removed book from your library'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'Book cannot be removed'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def add_to_currently_reading(self, request, pk=None):

        try:
            book = models.AbstractBook.objects.get(id=pk)
            user = request.user.userprofileapi
            book.current_readers.add(user)
            book.save()
            response = {'message': 'You added book to your current readings'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'Book cannot be added'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def remove_from_currently_reading(self, request, pk=None):

        try:
            book = models.AbstractBook.objects.get(id=pk)
            user = request.user.userprofileapi
            book.current_readers.remove(user)
            book.save()
            response = {'message': 'You removed book from your current readings'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'Book cannot be removed'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def add_to_read_list(self, request, pk=None):

        try:
            book = models.AbstractBook.objects.get(id=pk)
            user = request.user.userprofileapi
            book.wisher.add(user)
            book.save()
            response = {'message': 'You added book to your read list'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'Book cannot be added'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def remove_from_read_list(self, request, pk=None):

        try:
            book = models.AbstractBook.objects.get(id=pk)
            user = request.user.userprofileapi
            book.wisher.remove(user)
            book.save()
            response = {'message': 'You removed book from your read list'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'Book cannot be removed'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class BookListAPIView(generics.ListCreateAPIView):

    serializer_class = serializers.BookSerializer
    queryset = models.Book.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
          "book": 'serializers.BookSerializer(user, context=self.get_serializer_context()).data',
        })


class ReviewListAPIView(generics.ListCreateAPIView):

    serializer_class = serializers.ReviewListSerializer
    queryset = models.Review.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):

        request_user = self.request.user.userprofileapi
        kwarg_abstractbook = self.request.data["abstract_book"]
        abstractbook = models.AbstractBook.objects.get(pk=kwarg_abstractbook)
        print(abstractbook.id)
        print(request_user.username)
        if abstractbook.reviews.filter(user=request_user).exists():
            raise restSerializers.ValidationError("You have already reviewed this book!")

        serializer.save(user=request_user, abstract_book=abstractbook)

    def create(self, request, *args, **kwargs):

        request_user = request.user.userprofileapi
        kwarg_abstractbook = request.data["abstract_book"]
        abstractbook = models.AbstractBook.objects.get(pk=kwarg_abstractbook)

        data = {
            'user': model_to_dict(request_user),
            'abstract_book': model_to_dict(abstractbook),
            'review': request.data["review"]
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = serializers.ReviewDetailSerializer
    queryset = models.Review.objects.all()
    permission_classes = [permissions.IsOwnerOrReadOnly]


class CommentCreateAPIView(generics.ListCreateAPIView):

    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        request_user = request.user.userprofileapi
        data = {
            'user': model_to_dict(request_user),
            'comment': request.data['comment'],
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        request_user = self.request.user.userprofileapi
        if self.request.data["booklist"]:
            booklist = models.BookList.objects.get(pk=self.request.data["booklist"])
            serializer.save(user=request_user, booklist=booklist)
            return
        elif self.request.data["review"]:
            review = models.Review.objects.get(pk=self.request.data["review"])
            serializer.save(user=request_user, rewiew=review)
            return

        raise restSerializers.ValidationError("You can comment only for reviews or books")


class CommentDestroyAPIView(generics.DestroyAPIView):

    serializer_class = serializers.CommentSerializer
    queryset = models.Comment
    permission_classes = [permissions.IsOwnerOrReadOnly]


class AuthorViewSet(mixins.ListDetailSerializerMixin, viewsets.ModelViewSet):

    list_serializer_class = serializers.AuthorListSerializer
    detail_serializer_class = serializers.AuthorDetailSerializer
    queryset = models.Author.objects.all()
    permission_classes_by_action = {
        'create': [IsAdminUser],
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'update': [IsAdminUser],
        'partial_update': [IsAdminUser],
        'destroy': [IsAdminUser],
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    @action(detail=True, methods=['PUT'])
    def follow(self, request, pk=None):

        try:
            author = models.Author.objects.get(id=pk)
            user = request.user.userprofileapi
            author.followers.add(user)
            author.save()
            response = {'message': 'You followed the author'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'Author cannot be followed'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def unfollow(self, request, pk=None):

        try:
            author = models.Author.objects.get(id=pk)
            user = request.user.userprofileapi
            author.followers.remove(user)
            author.save()
            response = {'message': 'You unfollowed the author'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'Author cannot be unfollowed'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingCreateAPIView(generics.CreateAPIView):

    serializer_class = serializers.RatingSerializer
    queryset = models.Rating.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        request_user = self.request.user.userprofileapi
        kwarg_abstractbook = self.request.data["abstract_book"]
        abstractbook = models.AbstractBook.objects.get(pk=kwarg_abstractbook)

        if abstractbook.ratings.filter(user=request_user).exists():
            raise restSerializers.ValidationError("You have already rate this book!")

        serializer.save(user=request_user, book=abstractbook)


class RatingDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = serializers.RatingSerializer
    queryset = models.Rating.objects.all()
    permission_classes = [permissions.IsOwnerOrReadOnly]


class UpDownRatingCreateAPIView(generics.CreateAPIView):

    serializer_class = serializers.UpDownRatingSerializer
    queryset = models.UpDownRating.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        request_user = self.request.user.userprofileapi

        if "booklist" in self.request.data:
            kwarg_booklist = self.request.data["booklist"]
            booklist = models.BookList.objects.get(pk=kwarg_booklist)

            if booklist.votes.filter(user=request_user).exists():
                raise restSerializers.ValidationError("You have already voted this booklist!")

            serializer.save(user=request_user, bookList=booklist)

        elif "book" in self.request.data:
            kwarg_book = self.request.data["book"]
            book = models.Book.objects.get(pk=kwarg_book)

            if book.votes.filter(user=request_user).exists():
                raise restSerializers.ValidationError("You have already voted this book!")

            serializer.save(user=request_user, book=book)

        elif "review" in self.request.data:
            kwarg_review = self.request.data["review"]
            review = models.Book.objects.get(pk=kwarg_review)

            if review.votes.filter(user=request_user).exists():
                raise restSerializers.ValidationError("You have already voted this review!")

            serializer.save(user=request_user, review=review)

        return


class UpDownRatingDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = serializers.UpDownRatingSerializer
    queryset = models.UpDownRating.objects.all()
    permission_classes = [permissions.IsOwnerOrReadOnly]


class CategoryViewSet(mixins.ListDetailSerializerMixin, viewsets.ModelViewSet):

    lookup_field = 'slug'
    list_serializer_class = serializers.CategoryListSerializer
    detail_serializer_class = serializers.CategoryDetailSerializer
    permission_classes_by_action = {
        'create': [IsAdminUser],
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'update': [IsAdminUser],
        'partial_update': [IsAdminUser],
        'destroy': [IsAdminUser],
    }
    queryset = models.Category.objects.all()

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
