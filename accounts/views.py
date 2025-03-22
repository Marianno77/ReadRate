from msilib.schema import ListView

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, UpdateView, ListView
from pyexpat.errors import messages

from accounts.forms import RegisterForm, LoginForm
from page.models import UserBookStatus, Review, UserFollowAuthor, Book, Author


# Create your views here.

class LoginAndRegister(TemplateView):
    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        context['register_form'] = RegisterForm()
        return context

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(data=request.POST)
        register_form = RegisterForm(request.POST)

        if 'login_submit' in request.POST:
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('book-list')
        elif 'register_submit' in request.POST:
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect('book-list')

        return render(request, self.template_name, {'login_form': login_form, 'register_form': register_form})


class UserPanel(DetailView, LoginRequiredMixin):
    model = User
    template_name = 'accounts/user.html'
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_status'] = UserBookStatus.objects.filter(user=self.object, is_read=True).order_by('-read_date')
        context['rating'] = Review.objects.filter(user=self.object)
        context['follows'] = UserFollowAuthor.objects.filter(user=self.object,follow=True).order_by('-follow_date')
        context['reviews'] = Review.objects.filter(user=self.object).exclude(Q(review_text='') | Q(review_text__exact=' '))
        return context

class EditUserData(UpdateView, LoginRequiredMixin):
    model = User
    template_name = 'accounts/edit_user.html'
    fields = ['username', 'first_name', 'last_name']

    def get_success_url(self):
        return reverse('accounts:user-panel', kwargs={'pk': self.request.user.pk})

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        username = form.cleaned_data['username']
        existing_user = User.objects.filter(username=username).exclude(pk=self.request.user.pk).first()

        if existing_user:
            messages.error(self.request,"Użytkownik o takiej nazwie już istnieje.")
            return self.form_invalid(form)

        return super().form_valid(form)


class AdminPanel(ListView, LoginRequiredMixin):
    model = Book
    template_name = 'accounts/admin-panel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(is_template=True).order_by('created_date')
        context['authors'] = Author.objects.filter(is_template=True).order_by('created_date')

        return context

