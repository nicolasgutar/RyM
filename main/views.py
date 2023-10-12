
from django.shortcuts import render, redirect, get_object_or_404
from .models import Noticia
from .forms import PublicarNoticia
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

# Create your views here.

def about(request):
    return render(request, 'main/about.html')

def publicar(request):
    if request.method == 'GET':
        return render(request, 'main/pub.html', {'form':PublicarNoticia})
    else:
        Noticia.objects.create(tags = request.POST['tags'],
                               titulo = request.POST['titulo'],
                               resumen = request.POST['resumen'],
                               contenido = request.POST['contenido'])
        return redirect('/')
    
def tendencias(request):
    tags = ['Nacion','Industria', 'Economia', 'Deportes', 'Farandula','Política','Mundo','Opinion']
    applied_tags = []
    for tag in tags:
        if request.GET.get(tag):
            applied_tags.append(tag)
    
    noticias = Noticia.objects.all()

    if applied_tags == []:
        applied_tags = tags
    
    return render(request, "main/tendencias.html", {"noticias":noticias, "applied_tags":applied_tags})

def noticia(request, id):
    noticia = get_object_or_404(Noticia,id=id)
    return render(request, "main/noticia.html", {'noticia':noticia})

def iniciaSesion(request):
    if request.method == 'GET':
        return render(request, "main/iniciaSesion.html", {'form': AuthenticationForm})
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request, "main/iniciaSesion.html", {'form': AuthenticationForm,
                                                              'error': 'el usuario o la contraseña es incorrecto'})
        else:
            login(request, user)
            return redirect('/perfil')

def perfil(request):
    return render(request, 'main/perfil.html')

def registro(request):
    if request.method == 'GET':
        return render(request, "main/signup.html", {'form':UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username = request.POST['username'],
                                        password = request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('/perfil')
            except IntegrityError:
                return render(request, "main/signup.html", {'form':UserCreationForm,
                                                            'error':'el nombre de usuario ya existe'})

        return render(request, "main/signup.html", {'form':UserCreationForm,
                                                    'error': 'las contraseñas no coinciden'})
        print(request.POST)
        print('obt')

def signout(request):
    logout(request)
    return redirect('/')