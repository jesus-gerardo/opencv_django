from django.db import models

# Create your models here.
class personas(models.Model):
    id = models.AutoField(primary_key=True) 
    registro = models.CharField(max_length = 255, null=True)
    fecha_registro = models.DateField(auto_now_add=True)
    foto = models.FileField(upload_to="imagenes", max_length=150)

class datos_personas(models.Model):
    persona = models.ForeignKey(personas, on_delete=models.CASCADE)
    temperatura = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=5, decimal_places=2)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    presion = models.DecimalField(max_digits=5, decimal_places=2, null=True)  
    fecha_registro = models.DateField(auto_now_add=True)

class personas_imagenes(models.Model):
    persona = models.ForeignKey(personas, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to="fotos", max_length=100)