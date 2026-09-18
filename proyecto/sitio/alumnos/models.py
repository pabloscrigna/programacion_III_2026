from django.db import models


class Alumno(models.Model):
    class Genero(models.TextChoices):
        MASCULINO = "M", "Masculino"
        FEMENINO = "F", "Femenino"
        OTRO = "O", "Otro"
        NO_ESPECIFICA = "N", "Prefiere de decir"

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    clave = models.IntegerField(default=0)
    genero = models.CharField(
        max_length=1, choices=Genero.choices, blank=True, null=True
    )

    def __str__(self):
        return f"nombre: {self.nombre} - apellido: {self.apellido}"


class Mensaje(models.Model):
    texto = models.CharField(max_length=20)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"texto: {self.texto}"
