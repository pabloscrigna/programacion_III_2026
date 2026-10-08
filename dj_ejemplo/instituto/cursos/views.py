from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404


from cursos.models import Curso
from cursos.forms import CursoForm


def lista_cursos(request):

    cursos = Curso.objects.all()

    return render(request, "lista_cursos.html", {"cursos": cursos})


def detalle_curso(request, id):
    print("Vista  detalles de un curso")
    curso = get_object_or_404(Curso, pk=id)
    return render(request, "curso_detalle.html", {"curso": curso})


# GET -- POST
def crear_curso(request):

    if request.method == "POST":
        form = CursoForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            # nombre = form.cleaned_data["nombre"]
            # descripcion = form.cleaned_data["descripcion"]
            # precio = form.cleaned_data["precio"]
            # activo = form.cleaned_data["activo"]
            # curso = Curso(
            #     nombre=nombre, descripcion=descripcion, precio=precio, activo=activo
            # )
            # curso.save()
            curso = form.save()
            print(f"el {curso.id} se dio de alta")
            return redirect("cursos:lista")

    form = CursoForm()
    return render(request, "crear_curso.html", {"tag": "Crear", "form": form})


@login_required
def editar_curso(request, id):
    curso = get_object_or_404(Curso, pk=id)

    if request.method == "POST":
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            print("El curso se actualizo de manera exitosa")

        return redirect("cursos:lista")

    form = CursoForm(instance=curso)
    return render(request, "crear_curso.html", {"tag": "Editar", "form": form})


def registro(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect("cursos:lista")

    form = UserCreationForm()
    return render(request, "registration/registro.html", {"form": form})
