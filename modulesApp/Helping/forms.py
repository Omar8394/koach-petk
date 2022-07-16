from django import forms  
from .models import helpingImage
  
class helpingImageForm(forms.ModelForm):
  
    class Meta:
        model = helpingImage
        fields = ['imagen']