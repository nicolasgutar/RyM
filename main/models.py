from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Noticia(models.Model):
    TAGS = (
        ('Nacion','Nacion'),
        ("Industria","Industria"),
        ("Economia","Economia"),
        ("Deportes","Deportes"),
        ("Farandula","Farandula"),
        ("Política","Política"),
        ("Mundo","Mundo"),
        ("Opinion","Opinion"),
    )

    autor = models.CharField(max_length=30)
    tags = models.CharField(max_length=50, choices = TAGS)
    titulo = models.TextField(max_length=200, default="noticia")
    resumen = models.TextField(max_length=300)
    fecha = models.DateField(auto_now=True)
    #a implementar cuando se aprenda de usuarios
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    url = models.CharField(max_length=50, null=True, blank = True)
    contenido = models.TextField(max_length=2000,null=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ["fecha"]
