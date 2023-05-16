from typing import Any, Dict
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse
from datetime import datetime
from django.core.paginator import Paginator
from libreria.models import *


# Create your views here.

class VistaHora(View):
    def get(self, request):
        ahora = datetime.now()
        return HttpResponse(f'''
        <html>
          <head>
          </head>
            <body>
              La hora es { ahora }
            </body>
        </html>
        ''')

class HoraViewTemplate(TemplateView):
    template_name = 'hora.html'
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
      context = super().get_context_data(**kwargs)
      context['ahora'] = datetime.now()
      context['nombre'] = self.kwargs['nombre']
      context['apellido'] = self.kwargs['apellido']
      return context
    
class ListadoGenero(TemplateView):
    template_name = "listado_libros.html"
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        genero = self.kwargs['genero']
        libros = Libro.objects.filter(tipo_libro = genero)
        paginador = Paginator(libros, 12)
        numero_pagina = self.request.GET.get('page')
        context['page_obj'] = paginador.get_page(numero_pagina)
        return context 

class ListadoAutor(TemplateView):
    template_name = "listado_libros.html"
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        autorcito = self.kwargs['autor']
        libros = Libro.objects.filter(autor = Autor.objects.get(nombre = autorcito))
        paginador = Paginator(libros, 12)
        numero_pagina = self.request.GET.get('page')
        context['page_obj'] = paginador.get_page(numero_pagina)
        return context 

class AutoresAll(TemplateView):
    template_name='autores_all.html'
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)