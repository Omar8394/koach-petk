from django.db import models
from ..App.models import ConfTablasConfiguracion, AppPublico
 
class fichas(models.Model):
    
    id_ficha = models.AutoField(primary_key=True)
    nombre_ficha = models.TextField()
    mostrar = models.SmallIntegerField()
    ordenamiento = models.SmallIntegerField(default=0)

    class Meta:

        ordering = ['ordenamiento']
    
class fichas_bloques(models.Model):
    
    id_bloquexficha = models.AutoField(primary_key=True)
    descrip_bloque = models.TextField()
    fk_idficha = models.ForeignKey(fichas, on_delete=models.CASCADE, default=None, null=True)
    ordenamiento = models.SmallIntegerField(default=0)
    
    class Meta:

        ordering = ['ordenamiento']
        
class atributosxfichaxbloque(models.Model):
    
    id_atribxfichaxbloq = models.AutoField(primary_key=True)
    nombre_atrib = models.CharField(max_length=50, null=True, default="")
    fk_ficha_bloque = models.ForeignKey(fichas_bloques, on_delete=models.CASCADE, default=None, null=True)
    fk_tipodato = models.ForeignKey(ConfTablasConfiguracion, on_delete=models.DO_NOTHING, default=None, null=True)
    fk_atribxfichaxbloq_padre = models.ForeignKey('self', on_delete=models.CASCADE, db_column='fk_tabla_padre', default=None, null=True)
    listaValores = models.TextField(null=True, default=None)
    rangos = models.TextField(null=True, default=None)
    status = models.SmallIntegerField(default=1)
    orden_presentacion = models.SmallIntegerField(default=0)

    class Meta:

        ordering = ['orden_presentacion']

class public_fichas_datos(models.Model):
    
    id_publicFichasDatos = models.AutoField(primary_key=True)
    id_public  = models.ForeignKey(AppPublico, on_delete=models.DO_NOTHING, default=None, null=True)
    id_atributo_fichaBloque = models.ForeignKey(atributosxfichaxbloque, on_delete=models.DO_NOTHING, default=None, null=True)
    valor = models.TextField(null=True, default=None)