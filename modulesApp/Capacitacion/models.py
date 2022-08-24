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