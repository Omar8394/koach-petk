from django import forms  
from .models import helpingImage, helpingPdf
from django.core.exceptions import ValidationError

class helpingImageForm(forms.ModelForm):
  
    class Meta:
        
        model = helpingImage
        fields = ['imagen']

    def clean_imagen(self):

        data = self.cleaned_data['imagen']

        if (data.size/1000) > 3000 or not (data.content_type == 'image/jpeg' or data.content_type == 'image/png'):

            raise ValidationError("You have an error!")

        return data

        
class helpingPdfForm(forms.ModelForm):
  
    class Meta:
        
        model = helpingPdf
        fields = ['pdf']

    def clean_pdf(self):

        data = self.cleaned_data['pdf']
        
        if not data.content_type == 'application/pdf':

            raise ValidationError("You have an error!")

        return data