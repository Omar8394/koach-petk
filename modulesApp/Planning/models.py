from django.db import models
from ..App.models import ConfTablasConfiguracion
 
class fichas(models.Model):
    
    id_ficha = models.AutoField(primary_key=True)
    nombre_ficha = models.TextField()
    mostrar = models.SmallIntegerField()
    
class fichas_bloques(models.Model):
    
    id_bloquexficha = models.AutoField(primary_key=True)
    descrip_bloque = models.TextField()
    fk_idficha = models.ForeignKey(fichas, on_delete=models.CASCADE, default=None, null=True)
        
class atributosxfichaxbloque(models.Model):
    
    id_atribxfichaxbloq = models.AutoField(primary_key=True)
    nombre_atrib = models.CharField(max_length=50, null=True)
    fk_ficha_bloque = models.ForeignKey(fichas_bloques, on_delete=models.CASCADE, default=None, null=True)
    fk_tipodato = models.ForeignKey(ConfTablasConfiguracion, on_delete=models.DO_NOTHING, default=None, null=True)
    fk_atribxfichaxbloq_padre = models.ForeignKey('self', on_delete=models.DO_NOTHING, db_column='fk_tabla_padre')
    listaValores = models.TextField()
    rangos = models.TextField()
    status = models.SmallIntegerField(default=1)
    orden_presentacion = models.SmallIntegerField(default=0)
