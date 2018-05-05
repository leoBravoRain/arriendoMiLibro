# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from usuarios.models import Usuario
from arriendoMiLibro.variablesGlobales import maxLengthDefault
from arriendoMiLibro.funcionesGlobales import imageAutorotate

# Constantes
estadosDelLibro = (("disponible","Disponible"), ("quierenArrendarlo", "Quieren arrendarlo"), ("arrendado","Arrendado"))

# Create your models here.

# Libros para arrendar
class LibrosParaArrendar(models.Model):

	owner = models.ForeignKey(Usuario, on_delete=models.CASCADE)

	fechaCreacion = models.DateTimeField(auto_now=False,auto_now_add=False)
	
	titulo = models.CharField(max_length = maxLengthDefault)
	autor = models.CharField(max_length = maxLengthDefault)
	resumen = models.CharField(max_length = maxLengthDefault)
	foto = models.ImageField(upload_to= 'imagenes/libros')
	comentario = models.CharField(max_length = maxLengthDefault, null = True)

	# Estado de libro para saber si esta disponible para arrendar, alguien queire arrendarlo o arrendado
	estado = models.CharField(max_length = maxLengthDefault, choices = estadosDelLibro, default = estadosDelLibro[0][0])

	# Definir que cuando se llame al objeto se retorne su nombre
	def __str__(self):
		return self.titulo


	# Se sobreescribe el metodo save para rotar imagen
	def save(self):

		# Se sobreescribe metodo anterior
		super(LibrosParaArrendar, self).save()

		# Se aplica resize de la imagen
		imageAutorotate(self.foto)

# Arriendo de libro
class ArriendoDeLibro(models.Model):

	libro = models.ForeignKey(LibrosParaArrendar)
	arrendatario = models.ForeignKey(Usuario)
	finalizado = models.BooleanField(default = False)

	fechaCreacion = models.DateTimeField(auto_now=False,auto_now_add=False)
	fechaInicioArriendo = models.DateTimeField(auto_now=False,auto_now_add=False, null = True)
	fechaFinalArriendo = models.DateTimeField(auto_now=False,auto_now_add=False, null = True)

	# Definir que cuando se llame al objeto se retorne su nombre
	def __str__(self):
		return self.arrendatario.nombre