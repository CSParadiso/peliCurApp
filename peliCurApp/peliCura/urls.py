from django.urls import path
from peliCura.views import *

urlpatterns = [
    path('pelicurapp/', Index.as_view(), name="main-page"),
    path('pelicurapp/pelicula/<int:identificador>', DetallePelicula.as_view(), name="detalle-pelicula-id"),
    path('pelicurapp/pelicula/<str:titulo>', DetallePelicula.as_view(), name="detalle-pelicula-titulo"),
    path('pelicurapp/genero/<str:nombre>', GeneroListado.as_view(), name="genero-listado"),
    #path('pelicurapp/director/<str:apellido>', DetallePersona.as_view(), name="detalle-director"),
    #path('pelicurapp/actor/<str:apellido>', DetallePersona.as_view(), name="detalle-actor"),
]