from rest_framework import serializers
from . import models
import requests as req



class UserProfileAPISerializer(serializers.ModelSerializer):
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

    number_of_books = serializers.SerializerMethodField()
    number_of_lists = serializers.SerializerMethodField()
    number_of_reviews = serializers.SerializerMethodField()
    number_of_books_in_library = serializers.SerializerMethodField()
    number_of_books_in_readlist = serializers.SerializerMethodField()
    number_of_followers = serializers.SerializerMethodField()
    number_of_liked_lists = serializers.SerializerMethodField()
    number_of_following = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = models.UserProfileAPI
        fields = ('bio', 'avatar', 'currently_reading', 'favorite_books', 'readlist_url', 'mylist_url',
                  'mybooks_url','library_url',  'reviews_url', 'likes_url', 'followers_url', 'following_url',
                  'number_of_books', 'number_of_lists', 'number_of_reviews', 'number_of_books_in_library',
                  'number_of_books_in_readlist', 'number_of_followers', 'number_of_following', 'number_of_liked_lists',
                  'is_following')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def get_number_of_books(self, object):
        return object.my_books.count()

    def get_number_of_reviews(self, object):
        return object.my_reviews.count()

    def get_number_of_lists(self, object):
        return object.my_lists.count()

    def get_number_of_books_in_library(self, object):
        return object.library.count()

    def get_number_of_books_in_readlist(self, object):
        return object.read_list.count()

    def get_number_of_followers(self, object):
        return object.followers.count()

    def get_number_of_liked_lists(self, object):
        return object.liked_lists.count()

    def get_number_of_following(self, object):
        return object.followings.count()

    def get_is_following(self,object):

        user = self.context['request'].user
        user_has_followed = False

        if not user.is_anonymous:
            try:
                user_has_followed = bool(object.followers.get(user=user.id))
            finally:
                return user_has_followed
        return user_has_followed


class UserProfileAPIListSerializer(serializers.ModelSerializer):

    number_of_books = serializers.SerializerMethodField()
    number_of_lists = serializers.SerializerMethodField()
    number_of_reviews = serializers.SerializerMethodField()

    class Meta:
        model = models.UserProfileAPI
        fields = ("id", "username", "avatar", "number_of_books", "number_of_reviews", "number_of_lists")

        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def get_number_of_books(self, object):
        return object.my_books.count()

    def get_number_of_reviews(self, object):
        return object.my_reviews.count()

    def get_number_of_lists(self, object):
        return object.my_lists.count()


class BookSerializer(serializers.ModelSerializer):

    vote_sum = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()

    class Meta:
        model = models.Book
        fields = ("isbn_10", "release_date", "publisher", "user_vote", "vote_sum")

    def get_vote_sum(self, object):

        votes = object.votes.values_list('value', flat=True)
        summation = 0
        for value in votes:
            summation += value
        return summation

    def get_user_vote(self, object):

        user = self.context['request'].user
        user_vote = 0

        if not user.is_anonymous:
            try:
                user_vote = object.votes.get(user=user.id).value
            finally:
                return user_vote
        return user_vote

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

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Review
        fields = "__all__"


class AuthorListSerializer(serializers.ModelSerializer):

    number_of_followers = serializers.SerializerMethodField()

    class Meta:
        model = models.Author
        fields = "__all__"

    def get_number_of_followers(self, object):
        return object.followers.count()


class AbstractBookListSerializer(serializers.ModelSerializer):

    number_of_ratings = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    number_of_fans = serializers.SerializerMethodField()
    number_of_reviews = serializers.SerializerMethodField()
    number_of_readings = serializers.SerializerMethodField()

    class Meta:
        model = models.AbstractBook
        fields = ('id', 'name', 'image', 'authors', 'number_of_ratings', 'avg_rating', 'number_of_fans',
                   'number_of_reviews', 'number_of_readings')

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

    def get_number_of_fans(self, object):
        return object.bookLiker.count()

    def get_number_of_reviews(self, object):
        return object.reviews.count()

    def get_number_of_readings(self, object):
        return object.reader.count()


class AbstractBookDetailSerializer(serializers.ModelSerializer):

    authors = AuthorListSerializer(read_only=True, many=True)
    child_books = BookSerializer(many=True, required=True)
    reviews = ReviewSerializer(many=True, required=False)
    number_of_ratings = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    number_of_fans = serializers.SerializerMethodField()
    number_of_reviews = serializers.SerializerMethodField()
    number_of_readings = serializers.SerializerMethodField()

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

    def get_number_of_fans(self, object):
        return object.bookLiker.count()

    def get_number_of_reviews(self, object):
        return object.reviews.count()

    def get_number_of_readings(self, object):
        return object.reader.count()


class AuthorDetailSerializer(serializers.ModelSerializer):

    books = AbstractBookListSerializer(many=True)

    class Meta:
        model = models.Author
        fields = "__all__"


class BookListDetailSerializer(serializers.ModelSerializer):

    books = AbstractBookListSerializer(many=True, required=False)
    number_of_books = serializers.SerializerMethodField()
    number_of_likes = serializers.SerializerMethodField()
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

    def get_number_of_likes(self, object):
        return object.listLiker.count()


class BookListListSerializer(serializers.ModelSerializer):

    user = UserProfileAPIListSerializer(read_only=True)
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


class RatingSerializer(serializers.ModelSerializer):

    user =  serializers.StringRelatedField(read_only=True)
    book =  serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Rating
        fields= "__all__"


class UpDownRatingSerializer(serializers.ModelSerializer):

    user =  serializers.StringRelatedField(read_only=True)
    book =  serializers.StringRelatedField(read_only=True)
    bookList = serializers.StringRelatedField(read_only=True)
    review = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.UpDownRating
        fields= "__all__"