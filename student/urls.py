from django.urls import path

from .views import (
    renderRegisterView,
    renderLoginView,
    renderLogoutView,
)



urlpatterns = [
    path('register', renderRegisterView, name='register'),
    path('login', renderLoginView, name='login'),
    path('logout', renderLogoutView, name='logout'),
]