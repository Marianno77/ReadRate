from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import LoginAndRegister, UserPanel, EditUserData, AdminPanel

app_name = 'accounts'

urlpatterns = [
    path('accounts/',LoginAndRegister.as_view(),name='login-register'),
    path('accounts/user/<int:pk>/',UserPanel.as_view(),name='user-panel'),
    path('logout/',LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/user/edit',EditUserData.as_view(),name='edit-user'),
    path('accounts/user/admin-panel/',AdminPanel.as_view(),name='admin-panel')
]