import os
from django.db import models
from accounts.models import UserProfile
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from partial_date import PartialDateField
from PIL import Image as Img
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from .utils import unique_slug_generator
# Create your models here.

class UserProfileAPI(models.Model):

    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='userprofileapi')
    username = models.CharField(max_length=255, default='')
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='users')

    library = models.ManyToManyField("AbstractBook", related_name='owner', blank=True)
    my_books = models.ManyToManyField("AbstractBook", related_name='reader', blank=True)
    read_list = models.ManyToManyField("AbstractBook", related_name='wisher', blank=True)
    currently_reading = models.ManyToManyField("AbstractBook", related_name='current_readers', blank=True)
    favorite_books = models.ManyToManyField("AbstractBook", related_name='bookLiker', blank=True)
    liked_lists = models.ManyToManyField("BookList", related_name='listLiker', blank=True)

    followers = models.ManyToManyField("self", blank=True, related_name='followings', symmetrical = False)


    def __str__(self):
        """string representation of the user"""
        return self.username

    def save(self, *args, **kwargs):
        image_save(self, UserProfileAPI, 200, 200, *args, **kwargs)


@receiver(post_save, sender=UserProfile)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        UserProfileAPI.objects.create(user=instance, username=instance.username)


@receiver(post_delete, sender=UserProfile)
def auto_delete_UserImage_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

class BookList(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='booklists')
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=511, blank=True)
    user = models.ForeignKey(UserProfileAPI, related_name='my_lists', on_delete=models.CASCADE, blank=True)

    REQUIRED_FIELDS = ['name', 'user']

    def __str__(self):
        return self.name

#     def save(self, *args, **kwargs):
#         image_save(self, UserProfileAPI, 200, 200, *args, **kwargs)
#
#
# @receiver(post_delete, sender=BookList)
# def auto_delete_BookListImage_on_delete(sender, instance, **kwargs):
#     """
#     Deletes file from filesystem
#     when corresponding `MediaFile` object is deleted.
#     """
#     if instance.image:
#         if os.path.isfile(instance.image.path):
#             os.remove(instance.image.path)


class Author(models.Model):

    image = models.ImageField(null=True, blank=True, upload_to='authors')
    name = models.CharField(max_length=255)
    bio = models.TextField(max_length=511, blank=True)
    followers = models.ManyToManyField(UserProfileAPI, blank=True)

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        image_save(self, Author, 200, 200, *args, **kwargs)


@receiver(post_delete, sender=Author)
def auto_delete_AuthorImage_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class AbstractBook(models.Model):

    name = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='books')
    book_lists = models.ManyToManyField("BookList", related_name='books', blank=True)
    category = models.ManyToManyField('Category', related_name='books')
    pop_child_book = models.OneToOneField('Book', related_name='pop_of_parent', on_delete=models.PROTECT, null=True, blank=True)
    #genre = models.CharField(default='', max_length=63)

    REQUIRED_FIELDS = ['name', 'authors']

    def __str__(self):
        return self.name


class Book(models.Model):
    isbn_10 = models.CharField(max_length=10, blank=True)
    isbn_13 = models.CharField(max_length=13)
    name = models.CharField(max_length=255)
    release_date = PartialDateField(blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name='sub_books')
    translator = models.CharField(max_length=255, blank=True, null=True)
    page_number = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=1023, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='books')
    abstract_book = models.ForeignKey(AbstractBook, blank=True, null=True, related_name='child_books', on_delete=models.CASCADE)

    #REQUIRED_FIELDS = ['name', 'isbn_13']

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.isbn_13

    def save(self, *args, **kwargs):
        image_save(self, Book, 260, 400, *args, **kwargs)


@receiver(post_delete, sender=Book)
def auto_delete_Book_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class Review(models.Model):
    review = models.TextField(max_length=1023)
    abstract_book = models.ForeignKey(AbstractBook, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(UserProfileAPI, on_delete=models.CASCADE, related_name='my_reviews')

    class Meta:
        index_together = (('user', 'abstract_book'),)
        unique_together = (('user', 'abstract_book'),)

    def __str__(self):
        return self.user.username


class Rating(models.Model):
    user = models.ForeignKey(UserProfileAPI, on_delete=models.CASCADE, related_name="my_ratings")
    book = models.ForeignKey(AbstractBook, on_delete=models.CASCADE, related_name="ratings")

    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        unique_together = (('user', 'book'),)
        index_together = (('user', 'book'),)

    def __str__(self):
        return str(self.stars)


class UpDownRating(models.Model):

    class Votes(models.IntegerChoices):
        UP = 1
        DOWN = -1

    user = models.ForeignKey(UserProfileAPI, on_delete=models.CASCADE)
    bookList = models.ForeignKey(BookList, on_delete=models.CASCADE, related_name="votes", blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="votes", blank=True, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="votes", blank=True, null=True)

    value = models.IntegerField(choices=Votes.choices)

    class Meta:
        unique_together = (('user', 'book'), ('user', 'bookList'), ('user', 'review'))
        index_together = (('user', 'book'), ('user', 'bookList'), ('user', 'review'))

    def __str__(self):
        return str(self.value)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, default='', unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


@receiver(pre_save, sender=Category)
def generate_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


def image_save(obj, model, im_width, im_height, *args, **kwargs):
    # Opening the uploaded image
    width = im_width
    height = im_height
    size = (width, height)
    isSame = False
    if(obj.image):
        try:
            this = model.objects.get(id=obj.id)
            if this.image == obj.image:
                print('same')
                isSame = True
        except:
            pass

        im = Img.open(obj.image)
        (imw, imh) = im.size

        # resize the image if a bigger one was posted
        if (imw > width) or (imh > height):
            scale = 1
            if (imw/width)>(imh/height):
                scale = imw/width
            else:
                scale = imh/height
            im = im.resize((int(imw/scale), int(imh/scale)))
            (imw, imh) = im.size

        if (imw < width) or (imh < height):
            im.thumbnail(size, Img.ANTIALIAS)
            (imw, imh) = im.size

        im.load()
        background = Img.new("RGB", size, (255, 255, 255, 0))
        # background.resize((width, height))
        offset = (int(round(((width - imw) / 2), 0)), int(round(((height - imh) / 2), 0)))
        background.paste(im, offset)
        im = background

        output = BytesIO()

        # after modifications, save it to the output
        im.save(output, format='JPEG', quality=100)
        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        obj.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % obj.image.name.split('.')[0], 'image/jpeg',
                                        sys.getsizeof(output), None)

    try:
        this = model.objects.get(id=obj.id)
        if this.image == obj.image or isSame:
            obj.image = this.image
        else:
            this.image.delete(save=False)
    except:
        pass  # when new photo then we do nothing, normal case

    super(model, obj).save(*args, **kwargs)
