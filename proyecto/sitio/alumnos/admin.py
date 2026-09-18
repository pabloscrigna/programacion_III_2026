from django.contrib import admin

# Register your models here.
from alumnos.models import Alumno, Mensaje

# admin.site.register(Alumno)
admin.site.register(Mensaje)


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ("apellido", "nombre")
    list_filter = ("genero",)
    search_fields = ("apellido", "nombre")
    list_per_page = 3
    ordering = ("-apellido",)
