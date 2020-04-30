from rest_framework import serializers
from . import models
from rest_framework.authtoken.models import Token
import requests as req



class UserProfileSerializer(serializers.ModelSerializer):
    mylist_url = serializers.HyperlinkedIdentityField(
        view_name='user_mylists',
        lookup_field='username'
    )
    readlist_url = serializers.HyperlinkedIdentityField(
        view_name='user_readlist',
        lookup_field='username'
    )
    mybooks_url = serializers.HyperlinkedIdentityField(
        view_name='user_mybooks',
        lookup_field='username'
    )
    likes_url = serializers.HyperlinkedIdentityField(
        view_name = 'user_likes',
        lookup_field = 'username'
    )
    reviews_url = serializers.HyperlinkedIdentityField(
        view_name = 'user_reviews',
        lookup_field = 'username'
    )
    library_url = serializers.HyperlinkedIdentityField(
        view_name = 'user_library',
        lookup_field = 'username'
    )
    followers_url = serializers.HyperlinkedIdentityField(
        view_name = 'user_followers',
        lookup_field = 'username'
    )
    following_url = serializers.HyperlinkedIdentityField(
        view_name = 'user_following',
        lookup_field = 'username'
    )

    class Meta:
        model = models.UserProfile
        fields = ('first_name','last_name', 'username', 'bio', 'avatar', 'currently_reading', 'favorite_books', 'readlist_url', 'mylist_url',
         'mybooks_url','library_url',  'reviews_url', 'likes_url', 'followers_url', 'following_url')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }


class UserProfileListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserProfile
        fields = ("id", "username", "avatar", "first_name", "last_name", "email", "password")

        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_users(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name = validated_data['last_name'],
            password=validated_data['password']
        )
        token = Token.objects.create(user=user)

        return user

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Book
        fields = ("isbn_10",)

    def create(self, validated_data):
        isbn = self.validated_data['isbn_10']
        url = "https://www.googleapis.com/books/v1/volumes?q=" + isbn
        print(url)
        h = {'X-API-Key': 'AIzaSyCHAmQ3pPfn3Uh56eA7wSZ8RQUl0yvuuQw'}
        resp = req.get(url, headers=h)
        print(resp)
        book_info = resp.json()['items'][0]
        book_information = {
        'name' : book_info['volumeInfo']['title'],
        'authors' : book_info['volumeInfo']['authors'],
        #'description' : book_info['volumeInfo']['description'],
        # image = book_info['volumeInfo']['authors']
        'isbn_10' : book_info['volumeInfo']['industryIdentifiers'][0]['identifier'],
        'isbn_13' : book_info['volumeInfo']['industryIdentifiers'][1]['identifier'],
        'release_date' : book_info['volumeInfo']['publishedDate']
        }

        book = models.Book.objects.create(
        # name = book_information['name'],
        #                                               authors = book_information['authors'],
        #                                               description = book_information['description'],
                                                      isbn_10 = book_information['isbn_10'],
                                                      isbn_13 = book_information['isbn_13'],
                                                      release_date = book_information['release_date'])

        author = models.Author.objects.get_or_create(name = book_information['authors'])
        # print(author)

        return book
        # if models.AbstractBook.objects.filter(name = book_information['name'])
            # b = Book(abstract_book=models.AbstractBook.objects.get(name=book_information['name'])








class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Review
        fields = "__all__"


class AbstractBookListSerializer(serializers.ModelSerializer):

    number_of_ratings = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = models.AbstractBook
        fields = ('id', 'name', 'image', 'authors', 'number_of_ratings', 'avg_rating')

    def get_number_of_ratings(self, object):
        return object.ratings.count()

    def get_avg_rating(self, object):
        count: float = object.ratings.count()
        values = object.ratings.values_list('stars', flat=True)
        summation = 0
        for value in values:
            summation += value
        try:
            a = summation/count
        except ZeroDivisionError:
            a = []
        return a


class AbstractBookDetailSerializer(serializers.ModelSerializer):

    child_books = BookSerializer(many=True, required=True)
    number_of_ratings = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, required=False)

    class Meta:
        model = models.AbstractBook
        fields = "__all__"

    def get_number_of_ratings(self, object):
        return object.ratings.count()

    def get_avg_rating(self, object):
        count = object.ratings.count()
        values = object.ratings.values_list('stars', flat=True)
        summation = 0
        for value in values:
            summation += value
        try:
            a = summation / count
        except ZeroDivisionError:
            a = []
        return a


class AuthorListSerializer(serializers.ModelSerializer):

    number_of_followers = serializers.SerializerMethodField()

    class Meta:
        model = models.Author
        fields = "__all__"

    def get_number_of_followers(self, object):
        return object.followers.count()


class AuthorDetailSerializer(serializers.ModelSerializer):

    books = AbstractBookListSerializer(many=True)

    class Meta:
        model = models.Author
        fields = "__all__"


class BookListDetailSerializer(serializers.ModelSerializer):

    books = AbstractBookListSerializer(many=True, required=False)
    number_of_books = serializers.SerializerMethodField()
    vote_sum = serializers.SerializerMethodField()

    class Meta:
        model = models.BookList
        fields = "__all__"

    def get_number_of_books(self, object):
        return object.books.count()

    def get_vote_sum(self, object):

        votes = object.votes.values_list('value', flat=True)
        summation = 0
        for value in votes:
            summation += value
        return summation


class BookListListSerializer(serializers.ModelSerializer):

    number_of_books = serializers.SerializerMethodField()
    vote_sum = serializers.SerializerMethodField()

    class Meta:
        model = models.BookList
        fields = "__all__"

    def get_number_of_books(self, object):
        return object.books.count()

    def get_vote_sum(self, object):

        votes = object.votes.values_list('value', flat=True)
        summation = 0
        for value in votes:
            summation += value
        return summation
