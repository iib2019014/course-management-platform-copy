from django import forms
# from django.forms import 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import (
    Student,
)


# first create a User model object and then a Student model object,
    # then connect both of'em with OneToOne relation,

class UserRegistrationForm(UserCreationForm) :

    enrollment_no = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ('enrollment_no', 'username', 'password1', 'password2')