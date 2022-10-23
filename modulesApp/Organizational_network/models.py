from django.db import models
from ..App.models import ConfTablasConfiguracion, AppPublico
# Create your models here.
class nodos_grupos(models.Model):
    if_gruponodo= models.SmallAutoField(primary_key=True)
    Descripcion= models.TextField()
    valor_elemento= models.TextField()
    fk_liderGrupo=models.ForeignKey(AppPublico, on_delete=models.DO_NOTHING, default=None, null=True)
    fecha_creacion=models.DateField(blank=True, null=True)
    status_grupo=models.ForeignKey(ConfTablasConfiguracion,on_delete=models.DO_NOTHING,default=None, null=True,related_name="fk_status_nodo")	
    ubicacion=models.ForeignKey(ConfTablasConfiguracion,on_delete=models.DO_NOTHING,default=None, null=True,related_name="pais")	
    fk_grupoNodo_padre = models.ForeignKey('self',on_delete=models.DO_NOTHING, default=None, null=True)
