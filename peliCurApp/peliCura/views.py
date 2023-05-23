from typing import Any, Dict
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import *
from peliCura.models import *
from django.core.paginator import Paginator

# Create your views here.

class Index(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        peliculas = Pelicula.manager.all().order_by('-puntuacion') # Ordenadas por puntuacion descendente
        paginador = Paginator(peliculas, 18)
        page_number = self.request.GET.get("page")
        context["page_obj"] = paginador.get_page(page_number)
        context["peliculas"] = peliculas
        context['generos'] = Genero.manager.all().order_by('nombre')
        return context
    