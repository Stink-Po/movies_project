from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("email", "age")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs['class'] = "form-control"
        self.fields["email"].widget.attrs['class'] = "form-control"
        self.fields["age"].widget.attrs['class'] = "form-control"
        self.fields["password1"].widget.attrs['class'] = "form-control"
        self.fields["password2"].widget.attrs['class'] = "form-control"


class CustomUserChangeForom(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'password',
        }
))
