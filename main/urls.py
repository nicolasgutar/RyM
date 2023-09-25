from django.urls import path
from . import views

urlpatterns = [
    path('',views.tendencias),
    path('about/',views.about),
    path("noticia/<int:id>",views.noticia),
    path("publicar",views.publicar),
]