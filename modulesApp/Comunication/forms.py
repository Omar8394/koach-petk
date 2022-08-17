from ast import Pass
from dataclasses import field
from pyexpat import model
from django import forms
from .models import Boletin_Info

class BoletinForm(forms.ModelForm):
    titulo =widget={'titulo':forms.Textarea(
            attrs={
                "placeholder" : "Add a description",                
                "class": "form-control", 
                # 'maxlength':30
            }
        )}
    contenido = widget={'contenido':forms.Textarea(
            attrs={
                "placeholder" : "Add a description",                
                "class": "form-control", 
            }
        )}

    class Meta:
        model = Boletin_Info
        fields = ('titulo', 'contenido', 'path_recurso')

        Widget = {
            # 'titulo': forms.TextInput(attrs={'class':'form-control'}),
            # 'contenido': forms.Textarea(attrs={'class':'form-control'}),
            'path_recurso': forms.Textarea(attrs={'class':'form-control'}),

        }