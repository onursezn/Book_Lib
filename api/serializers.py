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
        fields = ('bio', 'image', 'currently_reading', 'favorite_books', 'readlist_url', 'mylist_url',
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
        fields = ("id", "username", "image", "number_of_books", "number_of_reviews", "number_of_lists")

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


class UserProfileAPIReviewSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(required=False, read_only=True)

    class Meta:
        model = models.UserProfileAPI
        fields = ( 'username', 'image' )


class BookSerializer(serializers.ModelSerializer):

    vote_sum = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()

    class Meta:
        model = models.Book
        fields = "__all__"

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


class BookListSerializer(serializers.ModelSerializer):

    vote_sum = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Book
        fields = ('id', 'image', 'vote_sum')

    def get_vote_sum(self, object):

        votes = object.votes.values_list('value', flat=True)
        summation = 0
        for value in votes:
            summation += value
        return summation


class AbstractBookForReviewSerializer(serializers.ModelSerializer):

    pop_child_book = BookListSerializer(read_only=True)

    class Meta:
        model = models.AbstractBook
        fields = ( 'id', 'name', 'pop_child_book')


class CommentSerializer(serializers.ModelSerializer):

    user = UserProfileAPIReviewSerializer()

    class Meta:
        model = models.Comment
        exclude = ("review", "booklist")


class ReviewListSerializer(serializers.ModelSerializer):

    user = UserProfileAPIReviewSerializer()
    abstract_book = AbstractBookForReviewSerializer()

    class Meta:
        model = models.Review
        fields = "__all__"


class ReviewDetailSerializer(serializers.ModelSerializer):

    user = UserProfileAPIReviewSerializer()
    abstract_book = AbstractBookForReviewSerializer()
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = models.Review
        fields = "__all__"


class AuthorListSerializer(serializers.ModelSerializer):

    number_of_followers = serializers.SerializerMethodField()

    class Meta:
        model = models.Author
        exclude = ("followers", )

    def get_number_of_followers(self, object):
        return object.followers.count()


class AbstractBookListSerializer(serializers.ModelSerializer):

    number_of_ratings = serializers.SerializerMethodField()
    avg_rating = serializers.IntegerField(read_only=True)
    number_of_fans = serializers.SerializerMethodField()
    number_of_reviews = serializers.SerializerMethodField()
    number_of_readings = serializers.SerializerMethodField()
    pop_child_book = BookListSerializer(read_only=True)
    authors = AuthorListSerializer(read_only=True, many=True)

    class Meta:
        model = models.AbstractBook
        fields = ('id', 'name', 'authors', 'number_of_ratings', 'avg_rating', 'number_of_fans',
                   'number_of_reviews', 'number_of_readings', 'pop_child_book')

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

    """def get_image(self, object):
        book = object.child_books.all().order_by('-total_vote').first()
        return book.image"""


class AbstractBookDetailSerializer(serializers.ModelSerializer):

    authors = AuthorListSerializer(read_only=True, many=True)
    child_books = BookSerializer(many=True, required=True)
    pop_child_book = BookListSerializer(read_only=True)
    reviews = ReviewListSerializer(many=True, required=False)
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
    comments = CommentSerializer(many=True, required=False)

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

    user = UserProfileAPIListSerializer(required=False)
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
        fields = "__all__"


class UpDownRatingSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    book = serializers.StringRelatedField(read_only=True)
    bookList = serializers.StringRelatedField(read_only=True)
    review = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.UpDownRating
        fields = "__all__"


class CategoryListSerializer(serializers.ModelSerializer):

    parent = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Category
        fields = ('id', 'name', 'parent', 'slug')


class CategoryDetailSerializer(serializers.ModelSerializer):

    books = AbstractBookListSerializer(many=True, required=False)

    class Meta:
        model = models.Category
        fields = ('id', 'parent', 'books')
