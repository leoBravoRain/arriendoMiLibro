# -*- coding: utf-8 -*-
from django import forms
from libros.models import LibrosParaArrendar
from django.forms import ModelForm
from usuarios.models import Usuario
from arriendoMiLibro.variablesGlobales import maxLengthDefault


# Editar libro
class EditarLibro(ModelForm):

    class Meta:
        model = LibrosParaArrendar
        exclude = ['owner','fechaCreacion','estado','foto']
        widgets = {

            'titulo': forms.TextInput(attrs={'placeholder': 'Titulo de libro'}),
            'autor': forms.TextInput(attrs={'placeholder': 'Autor del libro'}),
            'resumen': forms.Textarea(attrs={'placeholder': 'Breve resumen del libro', "maxlength" : maxLengthDefault, "size": maxLengthDefault, "class": "img-responsive"}),
            'comentario': forms.Textarea(attrs={'placeholder': 'Comentario (idioma, estado del libro, etc)', "maxlength" : 10, "class": "img-responsive"}),

        }
        # help_texts = {
        #     'foto' : 'Foto del libro',
        # }


# Formulario para registrar a un owner
class AgregarLibro(ModelForm):

    class Meta:
        model = LibrosParaArrendar
        exclude = ['owner','fechaCreacion','estado']
        widgets = {

	        'titulo': forms.TextInput(attrs={'placeholder': 'Titulo de libro'}),
	        'autor': forms.TextInput(attrs={'placeholder': 'Autor del libro'}),
	        'resumen': forms.Textarea(attrs={'placeholder': 'Breve resumen del libro', "maxlength" : maxLengthDefault, "size": maxLengthDefault, "class": "img-responsive"}),
	        'comentario': forms.Textarea(attrs={'placeholder': 'Comentario (idioma, estado del libro, etc)', "maxlength" : 10, "class": "img-responsive"}),

        }
        help_texts = {
        	'foto' : 'Foto del libro',
        }




# Fomulario para cambiar estado de libro
class CambiarEstadoDeLibro(ModelForm):

	class Meta:

		model = LibrosParaArrendar
		fields = ["estado"]
