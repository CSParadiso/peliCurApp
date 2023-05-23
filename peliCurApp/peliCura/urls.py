from django.urls import path
from peliCura.views import *

urlpatterns = [
    path('pelicurapp/', Index.as_view(), name="mainPage"),
]