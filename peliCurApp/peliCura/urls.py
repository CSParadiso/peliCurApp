from django.urls import path
from peliCura.views import *

urlpatterns = [
    path('pelicurapp/', Index.as_view(), name="main-page"),
    path('pelicurapp/pelicula/<int:identificador>', PeliculaDetalle.as_view(), name="detalle-pelicula-id"),
    path('pelicurapp/pelicula/<str:titulo>', PeliculaDetalle.as_view(), name="detalle-pelicula-titulo"),
    #path('pelicurapp/peliculas', PeliculasListado.as_view(), name="peliculas-listado")
    path('pelicurapp/genero/<int:identificador>', GeneroListado.as_view(), name="genero-listado-id"),
    path('pelicurapp/genero/<str:nombre>', GeneroListado.as_view(), name="genero-listado-nombre"),
    path('pelicurapp/directores', ListadoDirectores.as_view(), name="directores-listado"),
    #path('pelicurapp/actores', ActoresListado.as_view(), name="actores-listado")
    path('pelicurapp/director/<int:identificador>', PersonaDetalle.as_view(), name="detalle-director-id"),
    path('pelicurapp/director/<str:apellido>', PersonaDetalle.as_view(), name="detalle-director-nombre"),
    path('pelicurapp/actor/<int:identificador>', PersonaDetalle.as_view(), name="detalle-actor-id"),
    path('pelicurapp/actor/<str:apellido>', PersonaDetalle.as_view(), name="detalle-actor-nombre"),
]