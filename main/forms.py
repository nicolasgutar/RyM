from django import forms
from .models import Noticia

"""
class PublicarNoticia(forms.Form ):
    autor = forms.CharField(label = "autor de la noticia",max_length=30)
    tags = forms.CharField(max_length=50)
    titulo = forms.TextField(max_length=200, default="noticia")
    resumen = forms.TextField(max_length=300)
    fecha = forms.DateField(auto_now=True)
    contenido = forms.TextField(max_length=2000,null=True)
"""

class PublicarNoticia(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['tags', 'titulo', 'resumen', 'contenido']

