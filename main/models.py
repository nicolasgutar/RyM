from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from multiselectfield import MultiSelectField

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
    titulo = models.TextField(max_length=200)
    resumen = models.TextField(max_length=600)
    fecha = models.DateField(auto_now=True)
    #a implementar cuando se aprenda de usuarios
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE,null=True,blank=True)
    url = models.CharField(max_length=200, null=True, blank = True)
    contenido = models.TextField(max_length=4000,null=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ["fecha"]

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=12, unique=True)
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
    preferences = MultiSelectField(max_length= 50, choices = TAGS)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="pfp")
    saved_news = models.ManyToManyField(Noticia, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    password2 = models.CharField(max_length=20, null=True)

    objects = CustomUserManager()

    def get_by_natural_key(self):
        return self.username

    # Add other fields and methods as needed

    USERNAME_FIELD = 'username'