from django import forms
from .models import UserBookStatus, UserFollowAuthor, Book, Author


class UserBookStatusForm(forms.ModelForm):
    class Meta:
        model = UserBookStatus
        fields = ['is_read']
        labels = {
            'is_read': 'Przeczytane'
        }
        widgets = {
            'is_read': forms.CheckboxInput(attrs={"onchange": "this.form.submit();"}),
        }

class UserFollowAuthorForm(forms.ModelForm):
    class Meta:
        model = UserFollowAuthor
        fields = ['follow']
        labels = {
            'follow': 'Obserwuj:'
        }

        widgets = {
            'follow': forms.CheckboxInput(attrs={'onchange': 'this.form.submit();'})
        }

class BookAddForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['is_template']
        labels = {
            'is_template': 'Szablon:'
        }
        widgets = {
            'is_template': forms.CheckboxInput(attrs={"onchange": "this.form.submit();"}),
        }

class AuthorAddForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['is_template']
        labels = {
            'is_template': 'Szablon:'
        }
        widgets = {
            'is_template': forms.CheckboxInput(attrs={"onchange": "this.form.submit();"}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Szukaj'})
    )