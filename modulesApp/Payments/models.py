from django.db import models
from ..App.models import ConfTablasConfiguracion, AppPublico

# Create your models here.

class Pagos_regpagos(models.Model):
    idregpagos = models.SmallAutoField(primary_key=True)
    fkpublic = models.ForeignKey(AppPublico, on_delete=models.DO_NOTHING, db_column='fk_publico')
    fkmetodopago = models.ForeignKey(ConfTablasConfiguracion, on_delete=models.DO_NOTHING, related_name='fk_metodopago')
    fkconceptopago = models.ForeignKey(ConfTablasConfiguracion, on_delete=models.DO_NOTHING, related_name='fk_conceptopago') 
    fkStatusPago = models.ForeignKey(ConfTablasConfiguracion, on_delete=models.DO_NOTHING, related_name='fk_statuspago')
    fechaPago = models.DateField(db_column='fechapago', blank=True, null=True)  
    referencia = models.TextField(db_column='referencia', blank=True, null=True)
    confirmado = models.IntegerField(db_column='confirmado', blank=True, null=True)
    montopagado = models.DecimalField(max_digits=11, decimal_places=2, default=None, null=True)
    codigohash = models.TextField(db_column='codigohash', blank=True, null=True)
    beneficiario = models.TextField(db_column='beneficiario', blank=True, null=True)
     
    
class Event_eventos(models.Model):
    ideventos = models.SmallAutoField(primary_key=True)
    fktipoevento = models.ForeignKey(ConfTablasConfiguracion, on_delete=models.DO_NOTHING, db_column='fktipoevento')
    fechainicio = models.DateField(db_column='fechainicio', blank=True, null=True)
    lugar = models.TextField(db_column='lugar', blank=True, null=True)
    tipoevento = models.CharField(max_length=1, blank=True, null=True)
    fktipomedio =models.ForeignKey(ConfTablasConfiguracion, on_delete=models.DO_NOTHING, related_name='fk_tipomedio')
    fkmotivo = models.ForeignKey(ConfTablasConfiguracion, on_delete=models.DO_NOTHING, related_name='fk_motivo')
    temaprincipal = models.TextField(db_column='temaprincipal', blank=True, null=True)
    fechafinalevento = models.DateField(db_column='fechafinal', blank=True, null=True)


class Pagos_eventos(models.Model):
    idpagoseventos = models.SmallAutoField(primary_key=True)
    fk_idregpagos = models.ForeignKey(Pagos_regpagos, on_delete=models.DO_NOTHING, db_column='fk_idregpagos')
    fk_ideventos = models.ForeignKey(Event_eventos, on_delete=models.DO_NOTHING, db_column='fk_ideventos')