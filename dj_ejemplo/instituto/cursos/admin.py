from django.contrib import admin

from cursos.models import Curso


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre",)
