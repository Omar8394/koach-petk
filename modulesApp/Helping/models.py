from django.db import models
    
class tutoriales(models.Model):
    
    idtutorial = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=15)
    descripcion = models.TextField()
    url = models.TextField()
    tipo = models.SmallIntegerField()
    ordenamiento = models.SmallIntegerField()

    class Meta:

        ordering = ['-idtutorial']
        
class paginas(models.Model):
    
    idpagina = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50, null=True)
    fk_tutorial = models.ForeignKey(tutoriales, on_delete=models.CASCADE, default=None, null=True)
    contenido = models.TextField()
    url = models.TextField()
    ordenamiento = models.SmallIntegerField(default=0)

    class Meta:

        ordering = ['ordenamiento']


class helpingImage(models.Model):

    imagen = models.ImageField(upload_to='images/')
    

class helpingPdf(models.Model):
    
    pdf = models.FileField(upload_to='pdfs/')
