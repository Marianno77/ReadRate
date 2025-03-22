from django.contrib import admin
from .models import Book, Review, Author, UserBookStatus, UserFollowAuthor

# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(UserBookStatus)
admin.site.register(UserFollowAuthor)
