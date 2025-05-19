from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
User = get_user_model()

from django import  forms

from django.forms.widgets import PasswordInput, TextInput
class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
         username = forms.CharField(widget=TextInput())
         password = forms.CharField(widget=PasswordInput())
