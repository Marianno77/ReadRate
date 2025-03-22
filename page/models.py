from django.core.exceptions import ValidationError
from django.db.models import Count, BooleanField
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse

# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='author_images/',blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    is_template = models.BooleanField(default=True)

    def follow_count(self):
        follows = self.author_link.all()
        count = 0;
        for follow in follows:
            if follow.follow == True:
                count += 1
        return count

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})

    def get_most_common_category(self):
        most_common = (
            Book.objects.filter(author=self, is_template=False)
            .values('category')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        if most_common.exists():
            most_common_category = most_common.first()
            return most_common_category['category']
        else:
            return 'Brak kategorii'


    def __str__(self):
        full_name = f"{self.first_name} {self.second_name or ''} {self.last_name}"
        return " ".join(full_name.split())


class Book(models.Model):
    CATEGORY_CHOICES = [
        ('Fantastyka', 'Fantastyka'),
        ('Science Fiction', 'Science Fiction'),
        ('Romans', 'Romans'),
        ('Thriller', 'Thriller'),
        ('Tajemnica', 'Tajemnica'),
        ('Kryminał', 'Kryminał'),
        ('Horror', 'Horror'),
        ('Biografia', 'Biografia'),
        ('Historia', 'Historia'),
        ('Manga', 'Manga'),
        ('Religia', 'Religia'),
        ('Komiks', 'Komiks'),
        ('Przygoda', 'Przygoda'),
        ('Psychologia', 'Psychologia'),
        ('Komedia', 'Komedia'),
        ('Dramat', 'Dramat'),
        ('Filozofia', 'Filozofia'),
        ('Naukowe', 'Naukowe'),
    ]

    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    cover_image = models.ImageField(upload_to='book_covers/',blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    is_template = models.BooleanField(default=True)

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum([review.rating for review in reviews]) / len(reviews)
        return 0

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.pk})

    def __str__(self):
        name = f"{self.title} {self.subtitle or ''}"
        return " ".join(name.split())

class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField(blank=True,null=True)
    rating = models.PositiveSmallIntegerField(default=1,choices=[(i,i) for i in range(1,6)])
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username}: {self.book.title} -- {self.book.subtitle}'

class UserBookStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user','book')

    def __str__(self):
        return f"{self.user.username} - {self.book.subtitle} - {'Przeczytana' if self.is_read else 'Nieprzeczytana'}"

class UserFollowAuthor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, related_name='author_link', on_delete=models.CASCADE)
    follow = models.BooleanField(default=False)
    follow_date = models.DateTimeField(default=timezone.now )

    class Meta:
        unique_together = ('user','author')

    def __str__(self):
        return f"{self.user.username} - {self.author}"