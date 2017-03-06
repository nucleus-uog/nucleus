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
        # del self.fields['username']

    class Meta:
        model = User
        fields = ("repository_url",)

	
class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'GUID'}), label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}), label="")
    confirmPW = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}), label="")
	
    class Meta:
        model = User
        fields = ('username', 'password')

