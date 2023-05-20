from django import forms 

class FormularioSimple(forms.Form):
    genero = forms.CharField(label="Nombre del género: ",
                              max_length=100)