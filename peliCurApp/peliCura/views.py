from typing import Any, Dict
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import *
from peliCura.models import *
from django.core.paginator import Paginator
from django.http import Http404
from .forms import FormularioComentario
from django.db.models import Q

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

        # Asignar al template para poder seleccionar desde barra de navegación
        context['generoNavBar'] = Genero.manager.all().order_by('nombre')
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

        # Asignar al template para poder seleccionar desde barra de navegación
        context['generoNavBar'] = Genero.manager.all().order_by('nombre')
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
          

# Controlador de página de listado de Películas
class PeliculasListado(TemplateView):
   template_name = 'listado_peliculas.html'
   def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
      context = super().get_context_data(**kwargs)
      
      # Obtener todas las películas
      peliculas = Pelicula.manager.all().order_by('anio_realizacion', 'titulo')

      # Crear paginador
      paginador = Paginator(peliculas, 20)
      page_number = self.request.GET.get("page")
      context["page_obj"] = paginador.get_page(page_number)
      context["peliculas"] = peliculas

    # Asignar al template para poder seleccionar desde barra de navegación
      context['generoNavBar'] = Genero.manager.all().order_by('nombre')
      return context 

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

      # Asignar al template para poder seleccionar desde barra de navegación
      context['generoNavBar'] = Genero.manager.all().order_by('nombre')
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

      # Definir paginator y asignarle la página al template
      paginador = Paginator(peliculas, 25)
      page_number = self.request.GET.get("page")
      page_obj = paginador.get_page(page_number)
      context['page_obj'] = page_obj

      # Asignar al template para poder seleccionar desde barra de navegación
      context['generoNavBar'] = Genero.manager.all().order_by('nombre')
      return context 

# Controlador de página listado de Directores
class ListadoDirectores(TemplateView):
   template_name = "listado_directores.html"
   #template_name = "paginador_personas.html"
   def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
      context = super().get_context_data(**kwargs)
      
      # Obtener personas del modelo y asignarlas al template
      personas = Persona.manager.filter(director__isnull=False).distinct().order_by('apellido')
      context['personas'] = personas

      # Definir paginator y asignarle la página al template
      paginador = Paginator(personas, 25)
      page_number = self.request.GET.get("page")
      page_obj = paginador.get_page(page_number)
      context['page_obj'] = page_obj

      # Asignar al template para poder seleccionar desde barra de navegación
      context['generoNavBar'] = Genero.manager.all().order_by('nombre')
      #context['rol'] = "director"
      return context    

# Controlador de página listado de Actores
class ListadoActores(TemplateView):
   template_name = "listado_actores.html"
   def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
      context = super().get_context_data(**kwargs)
      
      # Obtener personas del modelo y asignarlas al template
      personas = Persona.manager.filter(actor__isnull=False).distinct().order_by('apellido')
      context['personas'] = personas

      # Definir paginator y asignarle la página al template
      paginador = Paginator(personas, 25)
      page_number = self.request.GET.get("page")
      page_obj = paginador.get_page(page_number)
      context['page_obj'] = page_obj

      # Asignar al template para poder seleccionar desde barra de navegación
      context['generoNavBar'] = Genero.manager.all().order_by('nombre')
      return context  
   
# Controlador para crear Películas
class CrearPelicula(CreateView):
   model = Pelicula
   fields = ['titulo', 'sinopsis', 'anio_realizacion', 'duracion', 'genero', 
             'director', 'actor', 'poster']   
   template_name = 'pelicula_form.html'
   success_url = reverse_lazy('detalle-pelicula-id')

   def form_valid(self, form):
     response = super().form_valid(form)
     self.object.save()
     return response
   
   def get_success_url(self):
        return reverse('detalle-pelicula-id', kwargs={'identificador': self.object.pk})

# Controlador para editar Películas
class EditarPelicula(UpdateView):
   model = Pelicula
   fields = ['titulo', 'sinopsis', 'anio_realizacion', 'duracion', 'genero', 
             'director', 'actor', 'poster']  
   template_name = "pelicula_form.html" 

   def form_valid(self, form):
     response = super().form_valid(form)
     self.object.save()
     return response
   
   def get_success_url(self):
        return reverse('detalle-pelicula-id', kwargs={'identificador': self.object.pk})

# Controlador para borrar Películas
class BorrarPelicula(DeleteView):
   model = Pelicula
   template_name = 'pelicula_confirm_delete.html'
   success_url = reverse_lazy('peliculas-listado')   
   
#Controlador para crear Personas
class CrearPersona(CreateView):
   model = Persona
   fields = ['nombre', 'apellido', 'nombre_artistico', 
             'nacionalidad', 'foto', 'fecha_nacimiento', 'biografia']   
   template_name = 'persona_form.html'
   success_url = reverse_lazy('detalle-director-id') # crear vista "detalle-persona-id"

   def form_valid(self, form):
     response = super().form_valid(form)
     self.object.save()
     return response
   
   def get_success_url(self):
        return reverse('detalle-director-id', kwargs={'identificador': self.object.pk})   

# Controlador para editar Personas
class EditarPersona(UpdateView):
   model = Persona
   fields = ['nombre', 'apellido', 'nombre_artistico', 
             'nacionalidad', 'foto', 'fecha_nacimiento', 'biografia']  
   template_name = "persona_form.html" 

   def form_valid(self, form):
     response = super().form_valid(form)
     self.object.save()
     return response
   
   def get_success_url(self):
        return reverse('detalle-director-id', kwargs={'identificador': self.object.pk})

# Controlador para borrar Personas
class BorrarPersona(DeleteView):
   model = Persona
   template_name = 'persona_confirm_delete.html'
   success_url = reverse_lazy('peliculas-listado')   
   

#Controlador para crear Géneros
class CrearGenero(CreateView):
   model = Genero
   fields = ['nombre']   
   template_name = 'genero_form.html'
   success_url = reverse_lazy('genero-listado-id') 

   def form_valid(self, form):
     response = super().form_valid(form)
     self.object.save()
     return response
   
   def get_success_url(self):
        return reverse('genero-listado-id', kwargs={'identificador': self.object.pk})  

# Controlador para borrar Género
class BorrarGenero(DeleteView):
   model = Genero
   template_name = 'genero_confirm_delete.html'
   success_url = reverse_lazy('main.page')   

# Controlador para auditar Comentarios
class AuditarComentario(TemplateView):
   template_name = "auditar_comentario.html"
   def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
      context = super().get_context_data(**kwargs)

      # Obtener los comentarios con el valor default ("Escrito") y asignarlo al template
      comentarios = Comentario.manager.filter(Q(estado = "E")).order_by('-fecha')
      context['comentarios'] = comentarios

      # Asignar al template para poder seleccionar desde barra de navegación
      context['generoNavBar'] = Genero.manager.all().order_by('nombre')
      return context

  # Obtener las actualizaciones de estado
   def post(self, request):
    comentario_id = request.POST.get('comentario_id')
    estado = request.POST.get('estado')

    # Actualizar el estado del objeto comentario
    comentario = Comentario.manager.get(id=comentario_id)
    comentario.auditar_comentario(estado)

    return redirect('auditar-comentario')   
