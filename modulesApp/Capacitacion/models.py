from django.db import models
from ..App.models import ConfTablasConfiguracion, AppPublico
from ..Organizational_network.models import nodos_grupos
# Create your models here.
class Estructuraprograma(models.Model):
    id_estructura = models.SmallAutoField(primary_key=True)
    descripcion = models.TextField()
    Titulo = models.TextField(null=True)
    valor_elemento = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    peso_creditos = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    orden_presentacion = models.SmallIntegerField(null=True)
    fk_categoria = models.ForeignKey(ConfTablasConfiguracion, on_delete=models.DO_NOTHING, default=None, null=True)
    fk_estructura_padre = models.ForeignKey('self',on_delete=models.DO_NOTHING, default=None, null=True)
    def __str__(self):
        return self.descripcion
class Capacitacion_componentesFormacion(models.Model):
    id_componetesformacion=models.SmallAutoField(primary_key=True)
    titulo=models.TextField(null=True)
    descripcion=models.TextField()
    codigo_componente=models.TextField(blank=True, null=True)
    url=models.TextField(blank=True, null=True)
    Fecha_activo=models.DateField(blank=True, null=True)
    creditos_peso=models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    orden_presentacion=models.SmallIntegerField(null=True)
    status_componente=models.IntegerField(blank=True, null=True)
    Condicion=models.IntegerField(blank=True, null=True)
    ritmo=models.IntegerField(blank=True, null=True)
    tipo_ritmo=models.ForeignKey(ConfTablasConfiguracion, on_delete=models.DO_NOTHING, default=None, null=True)
    tiene_certificad= models.BooleanField(null=True)
    def __str__(self):
        return self.titulo

class capacitacion_componentesXestructura(models.Model):
    id_componenteXestructura=models.SmallAutoField(primary_key=True)
    fk_componetesformacion=models.ForeignKey(Capacitacion_componentesFormacion, on_delete=models.DO_NOTHING, default=None, null=True)
    fk_estructuraprogramas=models.ForeignKey(Estructuraprograma, on_delete=models.DO_NOTHING, default=None, null=True)
class capacitacion_ComponentesActividades(models.Model):
    id_componenteActividades=models.SmallAutoField(primary_key=True)
    fk_componenteformacion=models.ForeignKey(Capacitacion_componentesFormacion,on_delete=models.DO_NOTHING, default=None, null=True)
    titulo=models.TextField(null=True)
    descripcion=models.TextField()
    fk_tipocomponente=models.ForeignKey(ConfTablasConfiguracion, on_delete=models.DO_NOTHING,related_name="tipo_componente")
    fecha_disponibilidad=models.DateField(blank=True, null=True)
    fk_statuscomponente=models.ForeignKey(ConfTablasConfiguracion,on_delete=models.DO_NOTHING,default=None, null=True,related_name="fk_status")
    url=models.TextField(blank=True, null=True)
    orden_presentacion =models.SmallIntegerField(null=True)
    valor_elemento=models.TextField(blank=True, null=True)
    peso_creditos=models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    def __str__(self):
        return self.titulo
class capacitacion_Actividad_leccion(models.Model):		
      id_actividadleccion=models.SmallAutoField(primary_key=True)
      fk_componenteActividad=models.ForeignKey(capacitacion_ComponentesActividades, on_delete=models.DO_NOTHING, default=None, null=True)
      titulo=models.TextField(null=True)
      descripcion=models.TextField()
      url= models.TextField(blank=True, null=True)
      orden_presentacion=models.SmallIntegerField(null=True)
      peso_creditos=models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
      valor_elemento=models.TextField(blank=True, null=True)
      fecha_disponibilidad=models.DateField(blank=True, null=True)
      fk_statusleccion=models.ForeignKey(ConfTablasConfiguracion,on_delete=models.DO_NOTHING,default=None, null=True,related_name="fk_status_le")
class capacitacion_LeccionPaginas(models.Model):
      id_leccionPaginas=models.SmallAutoField(primary_key=True)
      fk_actividadLeccion=models.ForeignKey(capacitacion_Actividad_leccion, on_delete=models.DO_NOTHING, default=None, null=True)
      titulo=models.TextField(null=True)
      contenido=models.TextField(null=True)
      orden_presentacion=models.SmallIntegerField(null=True)
      fk_statusPagina=models.ForeignKey(ConfTablasConfiguracion,on_delete=models.DO_NOTHING,default=None, null=True,related_name="fk_status_pa")
      fk_tipoContenido=models.ForeignKey(ConfTablasConfiguracion,on_delete=models.DO_NOTHING,default=None, null=True,related_name="tipo_contenido")
      id_recursos=models.TextField(null=True)
class capacitacion_Recursos(models.Model):
      id_recurso=models.SmallAutoField(primary_key=True)
      fk_tipoRecurso=models.ForeignKey(ConfTablasConfiguracion,on_delete=models.DO_NOTHING,default=None, null=True,related_name="tipo_recurso")
      path_rutas=models.TextField(null=True)
class capacitacion_Tag(models.Model):
      id_tag = models.SmallAutoField(primary_key=True)
      desc_tag = models.TextField(null=True)
class capacitacion_TagRecurso(models.Model):
      id_tag_recurso = models.AutoField(primary_key=True)
      fk_tag = models.ForeignKey(capacitacion_Tag,on_delete=models.CASCADE,  default=None, null=True)
      fk_recurso = models.ForeignKey(capacitacion_Recursos,on_delete=models.CASCADE,  default=None, null=True)
class capacitacion_componentesPrerequisitos(models.Model):
      id_componentePrerequisitos= models.AutoField(primary_key=True)
      fk_componenteActividades=models.ForeignKey(capacitacion_ComponentesActividades,on_delete=models.CASCADE,  default=None, null=True)
      fk_prerequisito=models.ForeignKey(capacitacion_ComponentesActividades,on_delete=models.CASCADE,  default=None, null=True, related_name="requisito")
class capacitacion_Actividad_tareas	(models.Model):
      id_capacitacion_actividadTareas= models.AutoField(primary_key=True)
      titulo=models.TextField(null=True)
      Descripcion_tarea=models.TextField(null=True)
      path_recurso=models.TextField(null=True)
      fk_status=models.ForeignKey(ConfTablasConfiguracion,on_delete=models.DO_NOTHING,default=None, null=True,related_name="fk_status_homework")	
      tiempo_entrega=models.IntegerField(blank=True, null=True)
      fk_tipoTiempoEntrega=models.ForeignKey(ConfTablasConfiguracion, on_delete=models.DO_NOTHING, default=None, null=True,related_name="fk_time")
      fk_componenteActividad=models.ForeignKey(capacitacion_ComponentesActividades, on_delete=models.DO_NOTHING, default=None, null=True)
class capacitacion_Actividad_Sesiones(models.Model):
      id_capacitacionActividadSesiones= models.AutoField(primary_key=True)
      titulo=models.TextField(null=True)
      Descripción = models.TextField(null=True)
      MAYBECHOICE = ( ('0', 'Presencial'), ('1', 'Online'), ('2', 'Mixta'), )
      modalidad = models.CharField(max_length=1, choices=MAYBECHOICE)
      fk_status=models.ForeignKey(ConfTablasConfiguracion,on_delete=models.DO_NOTHING,default=None, null=True,related_name="fk_status_sesiones")	
      fk_componenteActividad=models.ForeignKey(capacitacion_ComponentesActividades, on_delete=models.DO_NOTHING, default=None, null=True,related_name="fk_atvidad")
class capacitacion_ActSesiones_programar(models.Model):
      id_capacitacionActSesiones_programar= models.AutoField(primary_key=True)
      id_capacitacionActividadSesiones=models.OneToOneField(capacitacion_Actividad_Sesiones, on_delete=models.DO_NOTHING, default=None, null=True)
      director_ponente=models.ForeignKey(AppPublico, on_delete=models.DO_NOTHING, default=None, null=True)
      fk_grupoNodo=models.ForeignKey(nodos_grupos, on_delete=models.DO_NOTHING, default=None, null=True)
      status_sesion=models.ForeignKey(ConfTablasConfiguracion,on_delete=models.DO_NOTHING,default=None, null=True,related_name="status_sesiones")
      fecha_inicio=models.DateField(blank=True, null=True)
      datos_sesion = models.TextField(null=True)
      fecha_finalizacion=models.DateField(blank=True, null=True)	
      