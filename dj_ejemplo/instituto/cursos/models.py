from django.db import models

# Create your models here.


class Curso(models.Model):
    class Turno(models.TextChoices):
        MANANA = "M", "Mañana"
        TARDE = "T", "Tarde"
        NOCHE = "N", "Noche"

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    turno = models.CharField(max_length=1, choices=Turno.choices, default=Turno.MANANA)

    def __str__(self):
        return self.nombre
