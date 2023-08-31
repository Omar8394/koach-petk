
from distutils.command.upload import upload
from django.db import models
from ckeditor.fields import RichTextField
import os
from django.conf import settings
from ..Capacitacion.models import Estructuraprograma,componentesFormacion
from ..App.models import ConfTablasConfiguracion, AppPublico
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
class Entrenamiento_Post(models.Model): 
      id_post = models.SmallAutoField(primary_key=True)
      fk_escuela = models.ForeignKey(Estructuraprograma, on_delete=models.DO_NOTHING, default=None, null=True,related_name="escuela")
      fk_modulo = models.ForeignKey(Estructuraprograma, on_delete=models.DO_NOTHING, default=None, null=True,related_name="modulo")
      fk_topico = models.ForeignKey(componentesFormacion, on_delete=models.DO_NOTHING, default=None, null=True)
      link_post = models.TextField(blank=True, null=True)
      orden=models.SmallIntegerField(null=True)
class Entrenamiento_Post_Envio(models.Model): 
      id_PostEnvio	 = models.SmallAutoField(primary_key=True)
      fk_post = models.ForeignKey(Entrenamiento_Post, on_delete=models.DO_NOTHING, default=None, null=True)
      tipo_receptor = models.TextField(blank=True, null=True)
      tiempo_recordatorio = models.SmallIntegerField(null=True)
      tipo_recordatorio = models.ForeignKey(ConfTablasConfiguracion, on_delete=models.DO_NOTHING, default=None, null=True)
class Entrenamiento_Post_Envio_personas(models.Model): 
      id_post_envio_personas = models.SmallAutoField(primary_key=True)  
      fk_PostEnvio= models.ForeignKey(Entrenamiento_Post_Envio, on_delete=models.DO_NOTHING, default=None, null=True)      
      fk_public=models.ForeignKey(AppPublico, on_delete=models.DO_NOTHING, default=None, null=True)      
      fecha_inicio_envio=models.DateField(blank=True, null=True)
      fk_frecuencia=models.ForeignKey(ConfTablasConfiguracion, on_delete=models.DO_NOTHING, default=None, null=True)
      fecha_visto=models.DateField(blank=True, null=True)
      MAYBECHOICE = ( ('0', 'Sin enviar'), ('1', 'Enviado'), ('2', 'Reenviado'), )
      marca = models.CharField(max_length=1, choices=MAYBECHOICE)
      