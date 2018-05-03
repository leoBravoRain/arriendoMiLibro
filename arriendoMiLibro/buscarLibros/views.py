# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from libros.models import LibrosParaArrendar, estadosDelLibro, ArriendoDeLibro
from django.db.models import Q
from django.http import JsonResponse
from django.core import serializers
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils import timezone
from usuarios.models import Usuario
from arriendoMiLibro.variablesGlobales import precioArriendo, maximoLibrosPorRequest, mErrorIntenteNuevamente

# Variables generales

cualquierTitulo = "cualquierTitulo"
cualquierCiudad = "cualquierCiudad"
camposParaSerializarLibrosGeneral = ["titulo",'foto']
camposParaSerializarDetallesDeLibros = ["titulo","autor","resumen","foto","comentario"]
camposParaSerializarUsuario = ["nombre","foto"]
camposParaSerializarUsuarioDetalles = ["nombre", "foto"]
quierenArrendarlo = estadosDelLibro[1][0]
disponible = estadosDelLibro[0][0]

# Template
buscarLibrosTemplate = "buscarLibros/buscarLibros/buscarLibros.html"
verDetallesDeLibroTemplate = "buscarLibros/verDetallesDeLibro/verDetallesDeLibro.html"
arrendarLibroTemplate = "buscarLibros/arrendarLibro/arrendarLibro.html"
verDetallesDeOwnerTemplate = "buscarLibros/verDetallesDeOwnerTemplate/verDetallesDeOwnerTemplate.html"

# Mensajes
mArriendoExitoso = "¡ Tu arriendo ha sido exitoso ! Recuerda ponerte en contacto con el dueño para coordinar la entrega y el pago del libro."
mOwnerEsUsuario = "Ups, usted no se puede arrendar su libro a usted mismo."

# Create your views here.

# Vista para ver detalles de owner
@login_required
def verDetallesOwner_view(request, idOwner):

	# Se obtiene el template
	template = verDetallesDeOwnerTemplate 

	# Se obtiene el owner
	owner = Usuario.objects.get(id__exact = idOwner)

	# Se obtiene el contexto
	context = {"usuario" : owner}

	# Se retorna respeusta
	return render(request, template, context)


# Vista para confirmar el arriendo de un libro
@login_required
def confirmarArriendoDeLibro_view(request, idLibro):

	# Se obtiene el libro
	libro = LibrosParaArrendar.objects.get(id__exact = idLibro)

	# se obtiene el usuario logueado
	usuario = Usuario.objects.get(email__exact = request.user)
	
	# Se comprueba que usuario no sea dueño del libro
	if usuario != libro.owner:

		# Se chequea si el libro esta disponible
		if libro.estado == disponible:

			# Se almacena evento en DB
			ArriendoDeLibro(libro = libro, arrendatario = usuario , fechaCreacion = timezone.now()).save()

			# Se cambia estado de libro a quierenArrendarlo
			libro.estado = quierenArrendarlo

			# Se almacena cambio dn DB
			libro.save()

			# Se agrega mensaje de confirmacion de arriendo
			messages.add_message(request, messages.SUCCESS, mArriendoExitoso)

			# Se reenvia a detalles de libro
			return redirect(reverse('buscarLibros:verDetallesOwner', kwargs = {"idOwner": libro.owner.id}))

		# Si no esta disponible
		else:

			# Se agrega mensaje de error
			messages.add_message(request, messages.WARNING, mErrorIntenteNuevamente)

			# Se reenvia a detalles de libro
			return redirect(reverse('inicio:inicio'))

	# si es el mismo
	else:

		# Se agrega mensaje de confirmacion de arriendo
		messages.add_message(request, messages.WARNING, mOwnerEsUsuario)

		# Se reenvia a detalles de libro
		return redirect(reverse('buscarLibros:verDetallesDeLibro', kwargs = {"idLibro": idLibro}))		


# Vista para arrendar libro
@login_required
def arrendarLibro_view(request, idLibro):

	# Se obtiene los detalles
	template = arrendarLibroTemplate

	# Context
	context = {"idLibro": idLibro, "precioArriendo": precioArriendo}

	# Se retorna respuesta
	return render(request, template, context)


# Vista para ver detalles de libro
def verDetallesDeLibro_view(request, idLibro):

	# Si reques is ajax
	if request.is_ajax():

		# Se obtiene el libro
		libro = LibrosParaArrendar.objects.filter(id__exact = idLibro)

		# Se serializa al owner del libro
		owner = Usuario.objects.filter(id__exact = libro[0].owner.id)

		# Se serializa el owner
		owner = serializers.serialize("python", owner, fields = camposParaSerializarUsuario)

		# Se serializa el libro
		libro = serializers.serialize("python",libro, fields = camposParaSerializarDetallesDeLibros)

		# Se crea respuesta
		response = {"libro": libro, "owner": owner}

		# Se envia respuesta
		return JsonResponse(response)

	# Si es que reques no es ajax
	else:	

		# Se obtiene el template
		template = verDetallesDeLibroTemplate 

		# Se obtiene el contexto
		context = {"idLibro" : idLibro}

		# Se retorna respeusta
		return render(request, template, context)


# Vistar para buscar libros
def buscarLibros_view(request, titulo, ciudad):

	# Si request es ajax
	if request.is_ajax():

		# Se obtiene los libros ya mostrados
		idLibrosMostrados = list(set(map(lambda x: int(x), json.loads(request.GET["idLibrosMostrados"]))))

		# Si se escoge cualqueir ciudad
		if ciudad == cualquierCiudad:

			# Se filtra por titulo
			if titulo == cualquierTitulo:

				# Se obtienen los libros seleccionados
				libros = LibrosParaArrendar.objects.filter(estado__exact = disponible)

			else:

				# Se obtienen los libros seleccionados
				libros = LibrosParaArrendar.objects.filter(Q(titulo__icontains = titulo) & Q(estado__exact = disponible))

		# Si es qeu se escoge alguna ciudad
		else:

			# Se filtra por titulo
			if titulo == cualquierTitulo:

				# Se obtienen los libros
				libros = LibrosParaArrendar.objects.filter(Q(owner__ciudad__id__exact = ciudad) & Q(estado__exact = disponible))


			# Si se escoge un titulo especifico
			else:

				# Se obtienen los libros
				libros = LibrosParaArrendar.objects.filter(Q(owner__ciudad__id__exact = ciudad) & Q(titulo__icontains = titulo) & Q(estado__exact = disponible))

		# Se excluyen los libros ya mostrados
		libros = libros.exclude(id__in=idLibrosMostrados)

		# Mostrar hasta cierta cantidad de libros
		libros = libros[:maximoLibrosPorRequest]

		# Se serializa los libros
		libros = serializers.serialize("python",libros, fields = camposParaSerializarLibrosGeneral)

		# Se crea respuesta
		response = {"libros":libros}

		# Se envia respuesta
		return JsonResponse(response)

	# si reqeust no es aajax
	else:
		
		# Se obtiene template
		template = buscarLibrosTemplate

		# Se crea context
		context = {"titulo": titulo,"ciudad": ciudad}

		return render(request, template, context)
