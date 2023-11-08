
from django.shortcuts import render, redirect, get_object_or_404
from .models import Noticia, CustomUser
from .forms import PublicarNoticia, RegistrarUsuario, EditarPreferencias
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.db.models import Case, When, Value, IntegerField
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
                                                              'error': 'El usuario o la contraseña es incorrecto.'})
        else:
            login(request, user)
            return redirect('/perfil')

def perfil(request):
    user = request.user
    print(type(user.preferences))
    return render(request, 'main/perfil.html', {'usuario':user})

def registro(request):
    if request.method == 'POST':
        form = RegistrarUsuario(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']

            if password == password2:
                try:
                    user = CustomUser(username=username, profile_pic = form.cleaned_data['profile_pic'], preferences=form.cleaned_data['preferences'])
                    user.set_password(password)
                    user.save()
                    login(request, user)
                    messages.success(request, 'Usuario creado exitosamente.')
                    return redirect('/perfil')
                except IntegrityError:
                    messages.error(request, 'El nombre de usuario ya existe.')
            else:
                messages.error(request, 'Las contraseñas no coinciden.')
        else:
            # Form is not valid; messages should be displayed on the form
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in field "{field}": {error}')

    else:
        form = RegistrarUsuario()

    return render(request, "main/signup.html", {'form': form})

def editar(request):
    user = request.user
    if request.method == 'GET':
        return render(request, 'main/editar.html', {'form':EditarPreferencias})
    else:
        form = EditarPreferencias(request.POST)
        if form.is_valid():
            user.preferences = form.cleaned_data['preferences']
            user.save()
            return redirect('/perfil')
        user.preferences = []
        user.save()
        return redirect('/perfil')
        

def signout(request):
    logout(request)
    return redirect('/')
