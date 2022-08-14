
from distutils.command.upload import upload
from django.db import models
from ckeditor.fields import RichTextField
import os
from django.conf import settings

from ckeditor_uploader.fields import RichTextUploadingField


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
    titulo = RichTextField(blank=True, null=True, config_name='Specialtitulo')
    contenido = RichTextField(blank=True, null=True)
    fech_inicio = models.DateField(blank=True, null=True)
    fech_fin = models.DateField(blank=True, null=True)
    path_recurso = RichTextUploadingField(blank=True, null=True, config_name='Special')
    requiere_accion = models.BooleanField()
    url_accion = models.TextField()
    status = models.BooleanField(max_length=3)


    def delete(self, *args, **kwargs):
        
        cadena = self.path_recurso
    
        posicion=0

        while posicion != -1:
            posicion=cadena.find('src',posicion)
            if posicion != -1:
            
                cadena1=cadena[posicion+6:]
                pos_last=cadena1.index('"')
                cadena2=cadena1[:pos_last]
            

                if os.path.isfile(cadena2):
            
                    os.remove(cadena2)

                posicion+=1 

            
        super(Boletin_Info, self).delete(*args, **kwargs)


    
    def __str__(self):
        return self.titulo