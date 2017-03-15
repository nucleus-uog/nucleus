from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = User
        fields = ("email", "repository_url")

class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)

    class Meta:
        model = User
        fields = ("repository_url",)


class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control mb-2", 'id':"fNameInput"}), label="First Name")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control mb-2", 'id':"lNameInput"}), label="Last Name")
    email = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control mb-2", 'id':"emailInput"}), label="Student Email")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control mb-2", 'id':"passInput"}), label="Password")
    confirmPW = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control", 'id':"confirmPassInput"}), label="Confirm Password")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
