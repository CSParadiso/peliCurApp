from django.urls import path
from peliCura.views import *

urlpatterns = [
    # Página de inicio
    path('pelicurapp/', Index.as_view(), name="main-page"),
    # Páginas de detalles
    path('pelicurapp/pelicula/<int:identificador>/', PeliculaDetalle.as_view(), name="detalle-pelicula-id"),
    path('pelicurapp/pelicula/<str:titulo>/', PeliculaDetalle.as_view(), name="detalle-pelicula-titulo"),
    path('pelicurapp/genero/<int:identificador>/', GeneroListado.as_view(), name="genero-listado-id"),
    path('pelicurapp/genero/<str:nombre>/', GeneroListado.as_view(), name="genero-listado-nombre"),
    path('pelicurapp/director/<int:identificador>/', PersonaDetalle.as_view(), name="detalle-director-id"),
    path('pelicurapp/director/<str:apellido>/', PersonaDetalle.as_view(), name="detalle-director-nombre"),
    path('pelicurapp/actor/<int:identificador>/', PersonaDetalle.as_view(), name="detalle-actor-id"),
    path('pelicurapp/actor/<str:apellido>/', PersonaDetalle.as_view(), name="detalle-actor-nombre"),
    # Listados
    path('pelicurapp/peliculas/', PeliculasListado.as_view(), name="peliculas-listado"),
    path('pelicurapp/peliculas/<int:anio>/', PeliculasListadoAnio.as_view(), name="anio-listado"),
    path('pelicurapp/directores/', ListadoDirectores.as_view(), name="directores-listado"),
    path('pelicurapp/actores/', ListadoActores.as_view(), name="actores-listado"),
    # Crear    
    path('pelicurapp/add/pelicula/', CrearPelicula.as_view(), name="crear-pelicula"),
    path('pelicurapp/add/persona/', CrearPersona.as_view(), name="crear-persona"),
    path('pelicurapp/add/genero/', CrearGenero.as_view(), name="crear-genero"),
    # Actualizar    
    path('pelicurapp/pelicula/<int:pk>/update/', EditarPelicula.as_view(), name="editar-pelicula"),
    path('pelicurapp/director/<int:pk>/update/', EditarPersona.as_view(), name="editar-persona-director"),
    path('pelicurapp/actor/<int:pk>/update/', EditarPersona.as_view(), name="editar-persona-actor"),
    # Borrar
    path('pelicurapp/pelicula/<int:pk>/delete/', BorrarPelicula.as_view(), name="borrar-pelicula"),
    path('pelicurapp/director/<int:pk>/delete/', BorrarPersona.as_view(), name="borrar-persona-director"),
    path('pelicurapp/actor/<int:pk>/delete/', BorrarPersona.as_view(), name="borrar-persona-actor"),
    path('pelicurapp/genero/<int:pk>/delete/', BorrarGenero.as_view(), name="borrar-genero"),
    # Auditar comentario
    path('pelicurapp/auditar/', AuditarComentario.as_view(), name="auditar-comentario"),
]