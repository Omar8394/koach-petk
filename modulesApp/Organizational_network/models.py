from django.db import models
from ..App.models import ConfTablasConfiguracion, AppPublico
#from modulesApp.Capacitacion.models import componentesFormacion
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
class nodos_gruposIntegrantes(models.Model):
    id_nodoGrupo_Integrantes= models.SmallAutoField(primary_key=True)
    fk_public=models.ForeignKey(AppPublico, on_delete=models.DO_NOTHING, default=None, null=True)		
    fecha_incorporacion=models.DateField(blank=True, null=True)
    status_integrante=models.ForeignKey(ConfTablasConfiguracion,on_delete=models.DO_NOTHING,default=None, null=True,related_name="status_integrante")
    datos_adicionales=models.TextField()
    motivo_desincorporacion=models.ForeignKey(ConfTablasConfiguracion,on_delete=models.DO_NOTHING,default=None, null=True,related_name="motivo")
    descripcion_comentarios=models.TextField()
    fk_nodogrupo=models.ForeignKey(nodos_grupos,on_delete=models.DO_NOTHING,default=None, null=True)
class nodos_PlanFormacion(models.Model):
    idnodo_planformacion= models.SmallAutoField(primary_key=True)
    fk_gruponodo=models.ForeignKey(nodos_grupos, on_delete=models.DO_NOTHING, default=None, null=True)
    fk_componentesXestructura= models.ForeignKey('Capacitacion.capacitacion_componentesXestructura', on_delete=models.DO_NOTHING, default=None, null=True, related_name='forma')
    fecha_inicio=models.DateField(blank=True, null=True)
    orden_presentacion=models.SmallIntegerField(null=True)		
    fk_statusplan=models.ForeignKey(ConfTablasConfiguracion,on_delete=models.DO_NOTHING,default=None, null=True,related_name="status_plan")
	