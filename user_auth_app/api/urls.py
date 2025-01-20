# urls.py

from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, UserListView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserListView.as_view(), name='user-list'),  # Benutzerliste View
]
