from email.policy import default
from pyexpat import model
from select import select
from statistics import mode
import turtle
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.forms.utils import to_current_timezone

# Create your models here.

class ConfTablasConfiguracion(models.Model):
    id_tabla = models.SmallAutoField(primary_key=True)
    desc_elemento = models.CharField(max_length=70, blank=True, null=True)
    fk_tabla_padre = models.ForeignKey('self', on_delete=models.DO_NOTHING, db_column='fk_tabla_padre')
    tipo_elemento = models.CharField(max_length=1, blank=True, null=True)
    permite_cambios = models.IntegerField()
    valor_elemento = models.TextField(blank=True, null=True)
    mostrar_en_combos = models.IntegerField(db_column='Mostrar_en_combos', blank=True, null=True)  # Field name made lowercase.
    maneja_lista = models.IntegerField(db_column='Maneja_lista', blank=True, null=True)  # Field name made lowercase.
    datos_adicional = models.TextField(db_column='Datos_adicional', blank=True, null=True)  # Field name made lowercase.
    tipo_dato = models.SmallIntegerField(db_column='Tipo_dato', blank=True, null=True)  # Field name made lowercase.


class AppPublico(models.Model):
    idpublico = models.SmallAutoField(primary_key=True)
    nombre = models.TextField()
    apellido = models.TextField()
    correo_principal = models.TextField()
    pais = models.IntegerField(blank=True, null=True)
    telefono_principal = models.TextField()
    direccion = models.TextField()

    def __str__(self):
        return self.nombre +" " +self.apellido



class ConfMisfavoritos(models.Model):
    idmisfavoritos = models.AutoField(primary_key=True)
    idpublic = models.IntegerField()
    direccion_url = models.TextField()
    descripcion_url = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion_url


class ConfSettings(models.Model):
    idconfig_setting = models.SmallAutoField(primary_key=True)
    fk_setting_padre = models.ForeignKey('self', on_delete=models.DO_NOTHING, db_column='fk_setting_padre')
    fk_atributo_setting = models.SmallIntegerField()
    titulo_setting = models.TextField(db_column='Titulo_setting')  # Field name made lowercase.
    descripcion_setting = models.TextField(db_column='Descripcion_setting')  # Field name made lowercase.
    fecha_activo = models.DateField(db_column='Fecha_activo', blank=True, null=True)  # Field name made lowercase.
    status_setting = models.IntegerField(db_column='Status_setting')  # Field name made lowercase.
    rangovalor_setting = models.TextField(db_column='RangoValor_setting')  # Field name made lowercase.
    valor_setting = models.TextField()
    fk_tipo_dato_setting = models.ForeignKey(ConfTablasConfiguracion, on_delete=models.DO_NOTHING, db_column='fk_Tipo_dato_setting')  # Field name made lowercase.
    permite_borrar = models.IntegerField(db_column='Permite_Borrar')  # Field name made lowercase.

    



    