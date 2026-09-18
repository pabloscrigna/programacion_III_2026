from datetime import datetime

from django.shortcuts import render

from alumnos.models import Alumno


def inicio(request, id):
    print("id: ", id)
    notas = [5, 7, 10, 8]
    contexto = {
        "fecha_hora": datetime.now(),
        "nombre": "pablo",
        "id": int(id),
        "notas": notas,
    }

    alumnos = Alumno.objects.all()

    for alumno in alumnos:
        print(alumno.nombre)

    return render(request, "inicio-alumnos.html", contexto)
