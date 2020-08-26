from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.conf import settings
from django import forms
from accounts.models import User

class SignupForm(UserCreationForm):
    
    email = forms.EmailField()
      
    class Meta:
        model = User #settings.AUTH_USER_MODEL
        fields = ('username', 'email', 'role', 'password1', 'password2')
