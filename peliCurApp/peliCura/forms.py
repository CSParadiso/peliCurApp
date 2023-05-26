from django import forms
from django.forms import ModelForm 
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Comentario

# Creamos un formulario acorde al modelo Comentario
class FormularioComentario(ModelForm):
    # Establecer meta información del modelo del formulario
    class Meta:
       model = Comentario 
       fields = ["email", "nombre", "valoracion", "descripcion"]
       
       # Establecer limitaciones a los widgtes
       widgets = {
           "valoracion": forms.NumberInput(attrs={"min": 1,
                                                  "max": 5, 
                                                  "title": "Valore la película con un puntaje entre 1 y 5"}), 
           "descripcion": forms.Textarea(attrs={"rows": 4}),
       }

       # Validar el campo donde se ingresan las valoraciones
       validators = {
           "valoracion": [
               MinValueValidator(1),
               MaxValueValidator(5),
           ]
       }

       # Establecer mensajes de error
       error_messages = {
           "valoracion": {
               "min_value": "El puntaje debe ser igual o mayor a 1",
               "max_value": "El puntaje debe ser igual o menor a 5",
           }
       }

      