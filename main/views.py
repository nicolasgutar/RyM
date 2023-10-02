from django.shortcuts import render, redirect, get_object_or_404
from .models import Noticia
from .forms import PublicarNoticia

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
    noticias = Noticia.objects.all()
    return render(request, "main/tendencias.html", {'noticias':noticias})

def noticia(request, id):
    noticia = get_object_or_404(Noticia,id=id)
    return render(request, "main/noticia.html", {'noticia':noticia})