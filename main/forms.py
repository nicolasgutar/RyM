from django import forms
from .models import Noticia
from .models import CustomUser

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
        widgets = {
            'titulo': forms.Textarea(attrs={'placeholder':'ingrese el titulo de su noticcia'}),
            'resumen': forms.Textarea(attrs={'placeholder':'ingrese el resumen de su noticcia'}),
            'contenido': forms.Textarea(attrs={'placeholder':'ingrese el contenido de su noticcia'})
        }

class RegistrarUsuario(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password','password2','preferences']
