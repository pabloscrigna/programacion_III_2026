from django import forms

from cursos.models import Curso


# class CursoForm(forms.Form):
#     nombre = forms.CharField(max_length=100)
#     descripcion = forms.CharField(widget=forms.Textarea)
#     precio = forms.DecimalField()
#     activo = forms.BooleanField(initial=True)


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ["nombre", "descripcion", "precio", "activo", "turno"]
