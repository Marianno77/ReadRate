from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Nazwa użytkownika')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Adres e-mail', required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username):
            raise forms.ValidationError("Użytkownik o takiej nazwie już istnieje.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise forms.ValidationError("Użytkownik o takim adresie e-mail już istnieje.")
        return email