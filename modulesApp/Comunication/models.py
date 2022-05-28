
from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.


class Comunication_MsjPredeterminado(models.Model):
    id_MSJ = models.SmallAutoField(primary_key=True)
    titulo = models.TextField(blank=True, null=True)
    texto = models.TextField()
    url_link = models.TextField()
    req_respuesta = models.BooleanField()
    tipo_msj = models.TextField()
    

    def __str__(self):
        return self.titulo

class Boletin_Info(models.Model):
    id_boletin = models.SmallAutoField(primary_key=True)
    titulo = models.TextField(blank=True, null=True)
    contenido = RichTextField(blank=True, null=True)
    fech_inicio = models.DateField(blank=True, null=True)
    fech_fin = models.DateField(blank=True, null=True)
    path_recurso = models.TextField(blank=True, null=True)
    requiere_accion = models.BooleanField()
    url_accion = models.TextField()
    status = models.BooleanField(max_length=3)
    
    def __str__(self):
        return self.titulo