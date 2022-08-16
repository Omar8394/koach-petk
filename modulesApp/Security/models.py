from django.db import models
from django.contrib.auth.models import AbstractUser
from modulesApp.App.models import ConfTablasConfiguracion
# Create your models here.
class User(AbstractUser):
    fk_rol_usuario = models.ForeignKey(ConfTablasConfiguracion, on_delete=models.CASCADE,
                                       related_name='rol_usuario', null=True, default=None)
    fk_pregunta_secreta = models.ForeignKey(ConfTablasConfiguracion, on_delete=models.DO_NOTHING, related_name='pregunta', null=True, default=None)
    intentos_fallidos = models.IntegerField(default=3)  # Field name made lowercase.
    fecha_ult_cambio = models.DateField(blank=True, null=True)
    respuesta_secreta = models.TextField(blank=True, null=True)
    fk_status_cuenta = models.ForeignKey(ConfTablasConfiguracion, on_delete=models.DO_NOTHING, related_name='estado_cuenta', null=True)
    dias_cambio = models.IntegerField(default=90)
    url_imagen = models.CharField(max_length=100, default=None, blank=True, null=True)
    
    def __str__(self):
        return self.username
    
class CodigoVerificacion(models.Model):
    id_verificacion = models.AutoField(primary_key=True)
    activation_key = models.TextField(blank=True)
    key_expires = models.DateTimeField()
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    tipo_verificacion = models.ForeignKey(ConfTablasConfiguracion, on_delete=models.DO_NOTHING, related_name='tipo_verificacion')
