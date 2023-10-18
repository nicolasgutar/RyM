
from django.shortcuts import render, redirect, get_object_or_404
from .models import Noticia, CustomUser
from .forms import PublicarNoticia, RegistrarUsuario
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.db.models import Case, When, Value, IntegerField
from django.contrib.auth.decorators import login_required

# Create your views here.

def about(request):
    return render(request, 'main/about.html')


@login_required
def publicar(request):
    if request.method == 'GET':
        return render(request, 'main/pub.html', {'form':PublicarNoticia})
    else:
        Noticia.objects.create(tags = request.POST['tags'],
                               titulo = request.POST['titulo'],
                               resumen = request.POST['resumen'],
                               contenido = request.POST['contenido'],
                               user = request.user,
                               autor = request.user)
        return redirect('/')
    
def tendencias(request):

    tags = ['Nacion','Industria', 'Economia', 'Deportes', 'Farandula','Política','Mundo','Opinion']
    applied_tags = []
    for tag in tags:
        if request.GET.get(tag):
            applied_tags.append(tag)
    
    noticias = Noticia.objects.all().order_by('fecha').reverse()

    if applied_tags == []:
        applied_tags = tags
    
    if request.method == 'GET':
        return render(request, "main/tendencias.html", {"noticias":noticias, "applied_tags":applied_tags})
    elif request.method == 'POST':
        operacion = request.POST.get('operacion')
        print('aaaaaa',operacion)
        noticia_id = request.POST.get('noticia_id')
        if operacion == 'save':
            #print(noticia_id)
            noticia = Noticia.objects.get(id=noticia_id)
            #print(noticia)
            print('esta entrando por save')
            request.user.saved_news.add(noticia)
            #print(request.user.saved_news)
            return redirect('/')
        elif operacion == 'unsave':
            noticia = Noticia.objects.get(id=noticia_id)
            print('esta entrando por unsave')
            request.user.saved_news.remove(noticia)
            return redirect('/')

@login_required
def tusnoticias(request):
    tags = ['Nacion','Industria', 'Economia', 'Deportes', 'Farandula','Política','Mundo','Opinion']
    applied_tags = []
    for tag in tags:
        if request.GET.get(tag):
            applied_tags.append(tag)
    
    noticias = Noticia.objects.all().order_by('fecha').reverse()

    if applied_tags == []:
        applied_tags = tags

    preferences = set(request.user.preferences)

    noticias = noticias.annotate(
        custom_order= Case(
            When(tags__in=preferences, then=Value(1)),
            default=Value(0),
            output_field=IntegerField()
        )
    ).order_by('custom_order')

    if request.method == 'GET':
        return render(request, "main/tendencias.html", {"noticias":noticias, "applied_tags":applied_tags})
    elif request.method == 'POST':
        operacion = request.POST.get('operacion')
        print('aaaaaa',operacion)
        noticia_id = request.POST.get('noticia_id')
        if operacion == 'save':
            #print(noticia_id)
            noticia = Noticia.objects.get(id=noticia_id)
            #print(noticia)
            print('esta entrando por save')
            request.user.saved_news.add(noticia)
            #print(request.user.saved_news)
            return redirect('/perfil')
        elif operacion == 'unsave':
            noticia = Noticia.objects.get(id=noticia_id)
            print('esta entrando por unsave')
            request.user.saved_news.remove(noticia)
            return redirect('/perfil')



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
    user = request.user
    print(type(user.preferences))
    return render(request, 'main/perfil.html', {'usuario':user})

def registro(request):
    if request.method == 'GET':
        return render(request, "main/signup.html", {'form':RegistrarUsuario})
    else:
        if request.POST['password'] == request.POST['password2']:
            try:
                print(request.POST['preferences'])
                user = CustomUser.objects.create_user(username = request.POST['username'],
                                        password = request.POST['password'],
                                        password2 = 'secret',
                                        preferences = request.POST['preferences'])
                user.save()
                login(request,user)
                return redirect('/perfil')
            except IntegrityError:
                return render(request, "main/signup.html", {'form':UserCreationForm,
                                                            'error':'el nombre de usuario ya existe'})
        else:
            return render(request, "main/signup.html", {'form':UserCreationForm,
                                                    'error': 'las contraseñas no coinciden'})
        print(request.POST)
        print('obt')

def signout(request):
    logout(request)
    return redirect('/')
