from datetime import timezone

from django.http import JsonResponse, HttpResponseRedirect
from django.template.defaultfilters import title
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from unicodedata import category

from .forms import UserBookStatusForm, UserFollowAuthorForm, BookAddForm, SearchForm
from .models import Book, Review, UserBookStatus, Author, UserFollowAuthor
from django.db.models import Avg, Q, Count
from django.urls import reverse, reverse_lazy
from django import forms

from pyexpat.errors import messages

# Create your views here.

class BookListView(ListView):
    model = Book
    template_name = 'page/book_list.html'
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        # queryset = Book.objects.all()
        context = super().get_context_data(**kwargs)

        all_books = Book.objects.all()
        sorted_books = Book.objects.filter(is_template=False).annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:4]
        horror_books = Book.objects.filter(category='Horror', is_template=False).annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:4]
        fantasy_books = Book.objects.filter(category='Fantastyka', is_template=False).annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:4]
        best_authors = Author.objects.filter(is_template=False).annotate(follow_count=Count('author_link', filter=Q(author_link__follow=True))).order_by('-follow_count')[:4]
        category = Book.objects.all()[:1]

        context['sorted_books'] = sorted_books
        context['horror_books'] = horror_books
        context['fantasy_books'] = fantasy_books
        context['all_books'] = all_books
        context['best_authors'] = best_authors
        context['category'] = category

        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'page/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        context['authors'] = Author.objects.filter(is_template=True)

        form = BookAddForm(instance=book)
        context['form_add'] = form

        if self.request.user.is_authenticated:
            user_status, created = UserBookStatus.objects.get_or_create(user=self.request.user, book = book)
            form = UserBookStatusForm(instance=user_status)
            context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        book = self.get_object()

        if not request.user.is_authenticated:
            return self.get(request, *args, **kwargs)

        if 'form_add_submit' in request.POST:
            form_add = BookAddForm(request.POST, instance=book)
            if form_add.is_valid():
                form_add.save()
                return redirect('accounts:admin-panel')

        if 'form_status_submit' in request.POST:
            user_status, created = UserBookStatus.objects.get_or_create(user=request.user, book=book)
            form = UserBookStatusForm(request.POST, instance=user_status)
            status = UserBookStatus.objects.filter(user=self.request.user,book=book)
            if form.is_valid():
                '''
                if status:
                    if status.is_read != True:
                        status.read_date = timezone.now()
                    status.save()
                '''
                form.save()
                return redirect('book-detail', pk=book.pk)

        return self.get(request, *args, **kwargs)

class ReviewCreateView(CreateView):
    model = Review
    template_name = 'page/add_review.html'
    fields = ['review_text', 'rating']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.book_id = self.kwargs['book_id']
        book = get_object_or_404(Book, pk=self.kwargs['book_id'])
        existing = Review.objects.filter(user=self.request.user, book=book)
        if existing:
            form.add_error(None,'Już dodałeś recenzję do tej książki')
            return self.form_invalid(form)

        status = UserBookStatus.objects.filter(user=self.request.user,book=book).first()
        if status:
            if status.is_read != True:
                status.is_read = True
                status.read_date = timezone.now()
            status.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('book-detail', kwargs={'pk': self.kwargs['book_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = get_object_or_404(Book, pk=self.kwargs['book_id'])
        return context

class AuthorCreateView(CreateView):
    model = Author
    template_name = 'page/add_author.html'
    fields = ['first_name','second_name','last_name','description','birth_date','image']
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['birth_date'].widget = forms.DateTimeInput(attrs={'type': 'date'})
        form.fields['first_name'].label = 'Imię'
        form.fields['second_name'].label = 'Drugie imię'
        form.fields['last_name'].label = 'Nazwisko'
        form.fields['description'].label = 'Opis'
        form.fields['birth_date'].label = 'Data urodzenia'
        form.fields['image'].label = 'Zdjęcie'
        return form

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        second_name = form.cleaned_data['second_name']
        last_name = form.cleaned_data['last_name']

        existing = Author.objects.filter(first_name=first_name)

        if existing:
            existing = Author.objects.filter(second_name=second_name)
            if existing:
                existing = Author.objects.filter(last_name=last_name)
                if existing:
                    form.add_error(None, 'Taki autor już istnieje.')
                    return self.form_invalid(form)

        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e.message)
            return self.form_invalid(form)

class BookCreateView(CreateView):
    model = Book
    template_name = 'page/add_book.html'
    fields = ['author', 'title', 'subtitle', 'description', 'category', 'cover_image']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['author'].queryset = Author.objects.filter(is_template=False)

        form.fields['author'].label = 'Autor'
        form.fields['title'].label = 'Tytuł'
        form.fields['subtitle'].label = 'Podtytuł'
        form.fields['description'].label = 'Opis'
        form.fields['category'].label = 'Kategoria'
        form.fields['cover_image'].label = 'Okładka'
        return form

    def form_valid(self, form):
        author = form.cleaned_data['author']
        title = form.cleaned_data['title']
        subtitle = form.cleaned_data['subtitle']

        existing = Book.objects.filter(author=author)

        if existing:
            existing = Book.objects.filter(title=title)
            if existing:
                existing = Book.objects.filter(subtitle=subtitle)
                if existing:
                    form.add_error(None, 'Taka książka już istnieje.')
                    return self.form_invalid(form)

        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e.message)
            return self.form_invalid(form)

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'page/author_detail.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['books'] = Book.objects.filter(author=self.object, is_template=False).annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
        average_rating = Review.objects.filter(book__author=self.object).aggregate(Avg('rating'))['rating__avg']
        context['average_rating'] = round(average_rating, 1) if average_rating else 0
        context['all_authors'] = Author.objects.all()

        form = BookAddForm(instance=self.object)
        context['form_add'] = form

        if self.request.user.is_authenticated:
            author = self.object
            user_status, created = UserFollowAuthor.objects.get_or_create(user=self.request.user, author=author)
            form = UserFollowAuthorForm(instance=user_status)
            context['form'] = form

        return context

    def post(self, request, *args, **kwargs):
        author = self.get_object()

        if not request.user.is_authenticated:
            return self.get(request, *args, **kwargs)

        if 'form_add_submit' in request.POST:
            form_add = BookAddForm(request.POST, instance=author)
            if form_add.is_valid():
                form_add.save()
                return redirect('accounts:admin-panel')

        if 'form_status_submit' in request.POST:
            user_status, created = UserFollowAuthor.objects.get_or_create(user=self.request.user, author=author)
            form = UserFollowAuthorForm(request.POST, instance=user_status)

            if form.is_valid():
                form.save()
                return redirect('author-detail', pk=author.pk)

        return self.get(request, *args, **kwargs)

class CategoryBooks(ListView):
    model = Book
    template_name = 'page/category_book.html'
    context_object_name = 'books'

    CATEGORY_MAP = {v: k for k, v in dict(Book.CATEGORY_CHOICES).items()}

    def render_to_response(self, context, **response_kwargs):
        return super().render_to_response(context, **response_kwargs)

    def get_queryset(self):
        category_key = self.kwargs.get('category_key')
        if category_key:
            return Book.objects.filter(category=category_key, is_template=False)
        return Book.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_category'] = self.kwargs.get('category_key', 'Nieznana kategoria')
        return context

class AuthorListView(ListView):
    model = Author
    template_name = 'author_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        best_authors = Author.objects.filter(is_template=False).annotate(follow_count=Count('author_link', filter=Q(author_link__follow=True))).order_by('-follow_count')
        context['authors'] = best_authors

        return context

class AllBookView(ListView):
    model = bool
    template_name = 'page/category_book.html'
    context_object_name = 'books'

    def get_queryset(self):
        book = Book.objects.filter(is_template=False).annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
        return book

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['selected_category'] = 'Wszystkie książki'
        return context



class EditReviewView(UpdateView, LoginRequiredMixin):
    model = Review
    template_name = 'page/add_review.html'
    fields = ['review_text', 'rating']

    def get_object(self, queryset=None):
        return get_object_or_404(Review, pk=self.kwargs['pk'], book_id=self.kwargs['book_id'])

    def get_success_url(self):
        return reverse('book-detail', kwargs={'pk': self.kwargs['book_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = get_object_or_404(Book, pk=self.kwargs['book_id'])
        context['edit'] = True
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.book_id = self.kwargs['book_id']
        book = get_object_or_404(Book, pk=self.kwargs['book_id'])
        status = UserBookStatus.objects.filter(user=self.request.user, book=book).first()
        if status:
            status.is_read = True
            status.save()

        return super().form_valid(form)


class SearchView(ListView):
    model = Book
    template_name = 'page/category_book.html'
    context_object_name = 'books'

    def get_queryset(self):
        query = self.request.GET.get('query', '')

        if query and len(query) >= 3:
            return Book.objects.filter(
                Q(is_template=False),
                Q(author__first_name__icontains=query) |
                Q(author__second_name__icontains=query) |
                Q(author__last_name__icontains=query) |
                Q(title__icontains=query) |
                Q(subtitle__icontains=query)
            )
        return Book.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query']= self.request.GET.get('query', '')
        return context

class DeleteReview(DeleteView):
    model = Review

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', reverse_lazy('book-list'))

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

class DeleteBook(DeleteView):
    model = Book

    def get_success_url(self):
        return reverse_lazy('accounts:admin-panel')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

class DeleteAuthor(DeleteView):
    model = Author

    def get_success_url(self):
        return reverse_lazy('accounts:admin-panel')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())