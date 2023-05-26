from typing import Any, Dict
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import *
from peliCura.models import *
from django.core.paginator import Paginator
from django.http import Http404
from .forms import FormularioComentario

# Create your views here.

# Controlador de página principal
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

# Controlador de página detalle de Película    
class PeliculaDetalle(TemplateView):
    template_name = 'pelicula_detalle.html'
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        # Determinar si la url contiene id(int) o titulo(str) de la pelicula
        try:
          identificador = self.kwargs['identificador']
        except:
          identificador = None
        try:
          titulo = self.kwargs['titulo'].capitalize()
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

        # Añadir al contexto el formulario del modelo
        context['formulario_comentario'] = FormularioComentario()
        return context

    # Lógica del formulario 
    def post(self, request, *args, **kwargs):
      formulario = FormularioComentario(request.POST)
      # Si el formulario es válido
      if formulario.is_valid(): 
          # Extraer la info del formulario
          pelicula_comentada = self.get_context_data()['pelicula']
          correo = formulario.cleaned_data['email']
          nombre = formulario.cleaned_data['nombre'] 
          valoracion = formulario.cleaned_data['valoracion']
          descripcion = formulario.cleaned_data['descripcion']

          # Crear el comentario con el manager 
          Comentario.manager.crear_comentario(pelicula_comentada, 
                                              correo, 
                                              nombre, 
                                              descripcion,
                                              valoracion,)
          
          # Retornar a la misma página
          return redirect('detalle-pelicula-id', pelicula_comentada.id)
      else:
          # Si la respuesta no es exitosa
          context = self.get_context_data(**kwargs)
          context['formulario_comentario'] = formulario
          return self.render_to_response(context)
          

# Controlador de página detalle de Persona  
class PersonaDetalle(TemplateView):
   template_name = "persona_detalle.html"
   def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
      context = super().get_context_data(**kwargs)
      
      # Determinar si la url contiene id(int) o apellido(str) de la persona
      try:
        identificador = self.kwargs['identificador']
      except:
        identificador = None
      try:
        apellido = self.kwargs['apellido'].capitalize()
      except:
        apellido = None

      # Tratar de obtener la persona indicada
      try:
         if identificador is None:
            persona = Persona.manager.all().get(apellido=apellido)
         else:
            persona = Persona.manager.all().get(id=identificador)
      # Si la persona no existe, lanzamos un error 404 clásico (por ahora)
      except Genero.DoesNotExist:
          raise Http404
      
      # Obtener del modelo y asignar al template las películas 
      # en las que actúa y las cuales dirige la persona
      context['dirigidas'] = persona.director.all()
      context['actuadas'] = persona.actor.all()
      
      # Asignar la correspondiente persona al template
      context['persona'] = persona
      return context 

# Controlador de página de listado de Géneros    
class GeneroListado(TemplateView):
   template_name = "genero_listado.html"
   def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
      context = super().get_context_data(**kwargs)

      # Determinar si la url contiene id(int) o nombre(str) del género
      try:
        identificador = self.kwargs['identificador']
      except:
        identificador = None
      try:
        nombre = self.kwargs['nombre'].capitalize()
      except:
        nombre = None

      # Tratar de obtener el género indicado
      try:
         if identificador is None:
          genero = Genero.manager.all().get(nombre=nombre)
         else:
          genero = Genero.manager.all().get(id=identificador)  
      # Si el género no existe, lanzamos un error 404 clásico (por ahora)
      except Genero.DoesNotExist:
          raise Http404
      
      # Obtener las películas del género
      peliculas = genero.pelicula_set.all()

      # Asignar el correspondiente género y sus películas al template
      context['peliculas'] = peliculas
      context['genero'] = genero
      return context 

# Controlador de página listado de Directores
class ListadoDirectores(TemplateView):
   template_name = "listado_directores.html"
   def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
      context = super().get_context_data(**kwargs)
      
      # Obtener personas del modelo y asignarlas al template
      personas = Persona.manager.filter(director__isnull=False).distinct().order_by('apellido')
      context['personas'] = personas
      return context    

# Controlador de página listado de Actores
class ListadoActores(TemplateView):
   template_name = "listado_actores.html"
   def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
      context = super().get_context_data(**kwargs)
      
      # Obtener personas del modelo y asignarlas al template
      personas = Persona.manager.filter(actor__isnull=False).distinct().order_by('apellido')
      context['personas'] = personas
      return context  