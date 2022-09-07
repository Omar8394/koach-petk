from django.db import models
from ..App.models import ConfTablasConfiguracion
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