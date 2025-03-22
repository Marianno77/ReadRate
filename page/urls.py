from django.urls import path
from django.views.generic import TemplateView

from .views import BookListView, BookDetailView, ReviewCreateView, AuthorCreateView, BookCreateView, AuthorDetailView, \
    CategoryBooks, AuthorListView, AllBookView, EditReviewView, SearchView, DeleteReview, DeleteBook, DeleteAuthor
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',BookListView.as_view(), name='book-list'),
    path('books/book-number/<int:pk>/',BookDetailView.as_view(), name='book-detail'),
    path('authors/author-number/<int:pk>/',AuthorDetailView.as_view(), name='author-detail'),
    path('books/<int:book_id>/add-review',ReviewCreateView.as_view(), name='add-review'),
    path('author/add-author',AuthorCreateView.as_view(), name='add-author'),
    path('book/add-book',BookCreateView.as_view(), name='add-book'),
    path('books/category=<str:category_key>/', CategoryBooks.as_view(), name='category-book'),
    path('about/',TemplateView.as_view(template_name='page/about.html'), name='about'),
    path('contact/',TemplateView.as_view(template_name='page/contact.html'), name='contact'),
    path('authors/',AuthorListView.as_view(),name='author-list'),
    path('books/all-books/',AllBookView.as_view(),name='all-book'),
    path('books/<int:book_id>/edit-review/<int:pk>/',EditReviewView.as_view(),name='edit-review'),
    path('books/search',SearchView.as_view(),name='search'),
    path('books/book-number/<int:pk>/review-delete/',DeleteReview.as_view(),name='delete-review'),
    path('books/book-number/<int:pk>/book-delete/', DeleteBook.as_view(), name='delete-book'),
    path('authors/author-number/<int:pk>/author-delete/', DeleteAuthor.as_view(), name='delete-author'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)