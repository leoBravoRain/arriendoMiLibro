# -*- coding: utf-8 -*-
from django import forms
from usuarios.models import Usuario
from django.forms import ModelForm

# formulario para login de owner
class LoginOwner(forms.Form):

    email = forms.EmailField(required= True,widget=forms.TextInput(attrs={'placeholder': 'Correo@electronico.com'}) )
    password = forms.CharField(required= True,widget=forms.PasswordInput(attrs={'placeholder': 'Clave'}))


# Formulario para registrar a un owner
class RegistrarOwner(ModelForm):

    class Meta:
        model = Usuario
        exclude = ['user','fechaCreacion']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre completo'}),
            'email': forms.TextInput(attrs={'placeholder': 'email@gmail.com'}),
            'numeroContacto': forms.TextInput(attrs={'placeholder': '+569987654321'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Clave'}),

        }
        help_texts = {
        
                    'foto': 'Foto de perfil',
                    'ciudad': 'Ciudad en donde arrendarás libros',

                }
    

