from django.db import models
from accounts.models import UserProfile
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class UserProfile(UserProfile):

    bio = models.TextField(max_length=500)
    avatar = models.ImageField(null=True, blank=True)


    library = models.ManyToManyField("AbstractBook", related_name='owner', blank=True)
    my_books = models.ManyToManyField("AbstractBook", related_name='reader', blank=True)
    read_list = models.ManyToManyField("AbstractBook", related_name='wisher', blank=True)
    currently_reading = models.ManyToManyField("AbstractBook", related_name='current_readers', blank=True)
    favorite_books = models.ManyToManyField("AbstractBook", related_name='bookLiker', blank=True)
    liked_lists = models.ManyToManyField("BookList", related_name='listLiker', blank=True)

    followers = models.ManyToManyField("self", blank=True,related_name='followings', symmetrical = False)
    # following = models.ManyToManyField("self", blank=True,related_name= 'followerss', symmetrical = False)
    #
    def __str__(self):
        """string representation of the user"""
        return self.username





class BookList(models.Model):
    image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=511, blank=True)
    user = models.ForeignKey(UserProfile, related_name='my_lists', on_delete=models.CASCADE, blank=True)

    REQUIRED_FIELDS = ['name', 'user']

    def __str__(self):
        return self.name


class Author(models.Model):

    avatar = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=255)
    bio = models.TextField(max_length=511, blank=True)
    followers = models.ManyToManyField(UserProfile,blank=True)

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name


class AbstractBook(models.Model):

    name = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='books', blank=True)
    description = models.TextField(max_length=511, blank=True)
    image = models.ImageField(null=True, blank=True)
    book_lists = models.ManyToManyField("BookList", related_name='books', blank=True)
    #genre = models.CharField(default='', max_length=63)

    REQUIRED_FIELDS = ['name', 'authors']

    def __str__(self):
        return self.name


class Book(models.Model):
    isbn_10 = models.CharField(max_length=10, blank=True)
    isbn_13 = models.CharField(max_length=13, blank=True)
    release_date = models.DateField()
    abstract_book = models.ForeignKey(AbstractBook, blank=True, null=True, related_name='child_books', on_delete=models.CASCADE)

    #REQUIRED_FIELDS = ['name', 'isbn_13']

    def __str__(self):
        return self.isbn_10


class Review(models.Model):
    review = models.TextField(max_length=1023)
    abstract_book = models.ForeignKey(AbstractBook, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        index_together = (('user', 'abstract_book'),)
        unique_together = (('user', 'abstract_book'),)

    def __str__(self):
        return self.user.username


class Rating(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(AbstractBook, on_delete=models.CASCADE, related_name="ratings")

    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        unique_together = (('user', 'book'),)
        index_together = (('user', 'book'),)

    def __str__(self):
        return str(self.stars)


class UpDownRating(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    bookList = models.ForeignKey(BookList, on_delete=models.CASCADE, related_name="votes", blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="votes", blank=True, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="votes", blank=True, null=True)

    value = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(1)])

    class Meta:
        unique_together = (('user', 'book'), ('user', 'bookList'), ('user', 'review'))
        index_together = (('user', 'book'), ('user', 'bookList'), ('user', 'review'))

    def __str__(self):
        return str(self.value)
