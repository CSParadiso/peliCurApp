from typing import Any, Dict
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import *
from peliCura.models import *
from django.core.paginator import Paginator
from django.http import Http404

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
    
class DetallePelicula(TemplateView):
    template_name = 'detalle_pelicula.html'
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        # Determinar si la url contiene id(int) o titulo(str) de la pelicula
        try:
          identificador = self.kwargs['identificador']
        except:
          identificador = None
        try:
          titulo = self.kwargs['titulo']
        except:
          titulo = None
        
        # Tratar de obtener la película indicada
        try:
          if identificador is None:
            pelicula = Pelicula.manager.all().get(titulo=titulo)
          else:
            pelicula = Pelicula.manager.all().get(id=identificador)
        # Si la pel[icula no existe, lanzamos un error 404 clásico (por ahora)
        except Pelicula.DoesNotExist:
           raise Http404
           
        # Obtener los géneros, directores y actores de la pelicula y asignarlos al template
        context['generos'] = pelicula.genero.all()
        context['directores'] = pelicula.director.all()
        context['actores'] = pelicula.actor.all()

        # Asignar la correspondiente película al template
        context['pelicula'] = pelicula
        return context
    
class GeneroListado(TemplateView):
   template_name = "listado_genero.html"
   def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
      context = super().get_context_data(**kwargs)

      # Tratar de obtener el género indicado
      try:
         genero = Genero.manager.all().get(nombre=self.kwargs['nombre'].capitalize())
      # Si la pel[icula no existe, lanzamos un error 404 clásico (por ahora)
      except Genero.DoesNotExist:
          raise Http404
      
      # Obtener las películas del género
      peliculas = genero.pelicula_set.all()

      # Asignar el correspondiente género y sus películas al template
      context['peliculas'] = peliculas
      context['genero'] = genero
      return context 
