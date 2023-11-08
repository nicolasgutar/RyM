from django import forms
from .models import Noticia
from .models import CustomUser
from django.core.exceptions import ValidationError

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
            'titulo': forms.TextInput(attrs={'placeholder':'Ingrese el título de su noticia'}),
            'resumen': forms.Textarea(attrs={'placeholder':'Ingrese el resumen de su noticia'}),
            'contenido': forms.Textarea(attrs={'placeholder':'Ingrese el contenido de su noticia'})
        }
        labels = {
            'tags':'Tag'
        }

class RegistrarUsuario(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','profile_pic', 'password','password2','preferences']
        widgets = {
            #'preferences': forms.CheckboxInput(attrs={'class': 'custon-box'})
            'username': forms.TextInput(attrs={'placeholder':'Ingrese su usuario'}),
            'password': forms.PasswordInput(attrs={'placeholder':'Ingrese su contraseña. Almenos 6 caracteres, 1 de ellos no numerico'}),
            'password2': forms.PasswordInput(attrs={'placeholder':'Ingrese nuevamente su contraseña para validar'}),
        }

        labels = {
            'username': 'Usuario*',
            'password': 'Contraseña*',
            'password2': 'Confirmar Contraseña*',
            'preferences': 'preferencias',
            'profile_pic': 'foto de perfil'
        }

        
    preferences = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=CustomUser.TAGS
    )
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username.isalnum():
            raise ValidationError("Username should be alphanumeric.")
        return username
        
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise ValidationError("La contraseña debe tener almenos 6 caracteres.")
        if password.isdigit():
            raise ValidationError("La contraseña no debe ser completamente numérica.")
        return password
        


class EditarPreferencias(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['preferences']
        
        labels = {
            'preferences': 'preferencias',
        }