# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from arriendoMiLibro.variablesGlobales import maxLengthDefault
from django.conf import settings
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_delete

# Create your models here.

# Ciudad del dueño (que es donde va a arrendar el libro)
class Ciudad(models.Model):

	nombre = models.CharField(max_length = maxLengthDefault)

	# Definir que cuando se llame al objeto se retorne su nombre
	def __str__(self):
		return self.nombre
		
# Se crea usaurio dueño de libros
class Usuario(models.Model):

	user = models.OneToOneField(settings.AUTH_USER_MODEL, default = "1")

	nombre = models.CharField(max_length = maxLengthDefault)
	email = models.CharField(max_length = maxLengthDefault)
	numeroContacto = models.CharField(max_length = maxLengthDefault)
	password = models.CharField(max_length = maxLengthDefault)
	foto = models.ImageField(upload_to= 'imagenes/owners', null = True)
	ciudad = models.ForeignKey(Ciudad, on_delete = models.SET_NULL, blank=True, null=True)

	fechaCreacion = models.DateTimeField(auto_now=False,auto_now_add=False)
	

	# Definir que cuando se llame al objeto se retorne su nombre
	def __str__(self):
		return self.nombre

@receiver(pre_delete, sender=Usuario)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.foto.delete(False)
