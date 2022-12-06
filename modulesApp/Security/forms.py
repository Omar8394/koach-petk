from django.conf import settings
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth import get_user_model
from modulesApp.App.models import ConfTablasConfiguracion, AppPublico

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

class editProfiles(forms.ModelForm):
    nombre = forms.CharField(label='Nombre',
                             widget=forms.TextInput(
                                 attrs={
                                     "placeholder": "Agrega tu nombre",
                                     "class": "form-control form-control-line",
                                     'maxlength': 15,

                                 }
                             ))

    apellido = forms.CharField(label='Apellido',
                               widget=forms.TextInput(
                                   attrs={
                                       "placeholder": "Agrega tu apellido",
                                       "class": "form-control form-control-line",
                                       'maxlength': 100,
                                       "name": "Last Name"
                                   }
                               ))
    pais = forms.ModelChoiceField(queryset=ConfTablasConfiguracion.obtenerHijos("countries_iso"), empty_label="Selecciona tu pais?",label='Pais:',
    widget=forms.Select(
        attrs={        
            "placeholder" : "Selecciona un pais",        
            "class": "form-control",
        }
    )) 

    direccion = forms.CharField(label='Direccion',
                                widget=forms.TextInput(
                                    attrs={
                                        "placeholder": "Agrega una direccion",
                                        "class": "form-control form-control-line",
                                        'maxlength': 200
                                    }
                                ))

    telefono_principal = forms.CharField(label='Telefono Principal', required=False,
                                widget=forms.NumberInput(
                                    attrs={
                                        "placeholder": "Agrega un telefono",
                                        "class": "form-control form-control-line",
                                        'maxlength': 100
                                    }
                                ))

    correo_principal = forms.CharField(label='Correo Alternativo', required=False,
                              widget=forms.EmailInput(
                                  attrs={
                                      "placeholder": "Agregue un correo alternativo",
                                      "class": "form-control form-control-line",
                                      'maxlength': 100
                                  }
                              ))
    class Meta:
        model = AppPublico
        exclude=('telegram_id','user_id')

