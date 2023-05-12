"""
URL configuration for projecto_libreria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from libreria.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('libreria/horario/', VistaHora.as_view()),
    path('libreria/hora/<str:apellido>/<str:nombre>', HoraViewTemplate.as_view()), 
    path('libreria/genero/<str:genero>/', ListadoGenero.as_view()),
    path('libreria/autor/<str:autor>/', ListadoAutor.as_view()),
    path('libreria/autores',AutoresAll.as_view())
]
