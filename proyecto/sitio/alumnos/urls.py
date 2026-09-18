from django.urls import path

from alumnos.views import inicio

urlpatterns = [
    path("inicio/<str:id>", inicio),
]
