from django.contrib import admin
from .models import UserProfileAPI, Book, Review, Rating, BookList, Author, AbstractBook, UpDownRating, Category

admin.site.register(UserProfileAPI)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(BookList)
admin.site.register(Author)
admin.site.register(AbstractBook)
admin.site.register(UpDownRating)
admin.site.register(Category)
