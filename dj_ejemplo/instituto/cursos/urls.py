from django.urls import path

from cursos.views import lista_cursos, crear_curso, detalle_curso, editar_curso


app_name = "cursos"

urlpatterns = [
    path("", lista_cursos, name="lista"),
    path("<int:id>/", detalle_curso, name="detalle"),
    path("<int:id>/editar/", editar_curso, name="editar"),
    path("nuevo/", crear_curso, name="crear"),
]
