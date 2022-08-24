from django.conf import settings
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = settings.AUTH_USER_MODEL

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
        
class ResetPasswordForm(PasswordResetForm):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email o Usuario",
                "class": "form-control"
            }
        ))


class RecoveryMethodForm(ResetPasswordForm):
    typeMethod = forms.CharField(widget=forms.NumberInput)
    
class RecoveryMethodEmail(forms.Form):
    password1 = forms.CharField()
    password2 = forms.CharField()


class RecoveryMethodQuestion(forms.Form):
    secrettext = forms.CharField()


