from django.urls import reverse

from page.forms import SearchForm


def user_url(request):
    if request.user.is_authenticated:
        return {
            'user_url': reverse('accounts:user-panel',kwargs={'pk':request.user.pk})
        }
    return {}
