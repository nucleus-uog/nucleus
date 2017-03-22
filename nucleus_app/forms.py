from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
import re

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
    """
    Creates a form that validates the registration of a user.
    """
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control mb-2"}), label="First Name")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control mb-2"}), label="Last Name")
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':"form-control mb-2"}), label="Student Email")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control mb-2"}), label="Password")
    confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control"}), label="Confirm Password")

    def clean_email(self):
        """Check that a email matches a Glasgow University student email."""
        email = self.cleaned_data.get('email')

        # Raise a ValidationError if the regex does not match.
        if not re.match(r'\d{7}[A-Za-z]@student.gla.ac.uk', email):
            raise forms.ValidationError("You must use your student email.")
        return email

    def clean_confirm(self):
        """Check that the password confirmation matches the password."""
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')

        # Check that are supplied a password confirmation, else bail out.
        if not confirm:
            raise forms.ValidationError("You must confirm your password.")
        # Check that the password confirmation matches the password, else bail out.
        if password != confirm:
            raise forms.ValidationError("Your passwords do not match.")
        return confirm

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')


class RepoForm(forms.Form):
    """Validates a repository url for a given student."""
    repository_url = forms.URLField(widget=forms.TextInput(attrs={'class':"form-control mb-2", 'id':"repoUrl"}), label="Repository")
    student_email = forms.EmailField(widget=forms.HiddenInput(attrs={'id': "studentEmail"}))

