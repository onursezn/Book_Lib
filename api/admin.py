from django.contrib import admin
from .models import UserProfile, Book, Review, Rating, BookList, Author, AbstractBook, UpDownRating

admin.site.register(UserProfile)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(BookList)
admin.site.register(Author)
admin.site.register(AbstractBook)
admin.site.register(UpDownRating)
