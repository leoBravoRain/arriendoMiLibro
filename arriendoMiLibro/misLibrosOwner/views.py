# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from forms import AgregarLibro, CambiarEstadoDeLibro
from libros.models import LibrosParaArrendar, estadosDelLibro, ArriendoDeLibro
from django.utils import timezone
from django.core.urlresolvers import reverse
from usuarios.models import Usuario
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q
import json
from arriendoMiLibro.variablesGlobales import precioArriendo, maximoLibrosPorRequest

# Variables generales
camposParaSerializarLibros = ["fechaCreacion", "titulo","autor","resumen","foto","comentario","estado"]
camposParaSerializarDetallesDeLibros = ["titulo","autor","resumen","foto","comentario"]
camposParaSerializarUsuario = ["nombre","foto"]

# Variables for book state
disponible = estadosDelLibro[0][0]
arrendado = estadosDelLibro[2][0]

# Template
misLibrosOwnerTemplate = "misLibrosOwner/misLibrosOwner/misLibrosOwner.html"
agregarLibroTemplate = "misLibrosOwner/agregarLibro/agregarLibro.html"
cambiarEstadoDeLibroTemplate = "misLibrosOwner/cambiarEstadoDeLibro/cambiarEstadoDeLibro.html"
verDetallesDeQuienQuiereArrendarloTemplate  = "misLibrosOwner/verDetallesDeQuienQuiereArrendarlo/verDetallesDeQuienQuiereArrendarlo.html"
verDetallesDeArriendoDeLibroTemplate = "misLibrosOwner/verDetallesDeArriendoDeLibro/verDetallesDeArriendoDeLibro.html"
verDetallesDeLibroOwnerTemplate = "misLibrosOwner/verDetallesDeLibroOwner/verDetallesDeLibroOwner.html"

# Messagess
mRegistroDeLibroExitoso = "Se ha registrado exitosamente su libro, ahora solo debe esperar a que alguien quiera leerlo, ¡ Suerte !"
mCambioDeEstadoExitoso = "Se ha cambiado el estado del libro"
mArriendoFinalizadoExitosamente = "Se ha finalizado el arriendo de tu libro. Ahora está disponible para ser arrendado nuevamente. ¡Suerte!"
mInicioPeriodoArriendoExitoso = "Has iniciado correctamente el periodo de arriendo"

# Create your views here.


# Vista para ver detalles de libro
def verDetallesDeLibroOwner_view(request, idLibro):

	# Si reques is ajax
	if request.is_ajax():

		# Se obtiene el libro
		libro = LibrosParaArrendar.objects.filter(id__exact = idLibro)

		# Se obtiene el owner
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
		template = verDetallesDeLibroOwnerTemplate 

		# Se obtiene el contexto
		context = {"idLibro" : idLibro}

		# Se retorna respeusta
		return render(request, template, context)


# Vista para finalizar periodo de arriendo
@login_required
def terminarPeriodoDeArriendo_view(request):

	# Se obtiene la relacion de arriendo
	relacionArriendo = ArriendoDeLibro.objects.get(Q(libro__id__exact = request.POST["idLibro"]) & Q(finalizado__exact = False))

	# Se cambia variable de finalizado a True
	relacionArriendo.finalizado = True

	# Se almacena en DB
	relacionArriendo.save()

	# Se toma el libro asociado
	libro = LibrosParaArrendar.objects.get(id__exact = relacionArriendo.libro.id)

	# Se cambia el estado del libro a disponible
	libro.estado = disponible

	# Se almacena en DB
	libro.save()

	# Add message
	messages.add_message(request, messages.SUCCESS, mArriendoFinalizadoExitosamente)

	# Se crea respuest
	response = {"success": True}

	# Se envia respuesta
	return JsonResponse(response)

# Vista para retornar detalles de arriendo de libro
@login_required
def verDetallesDeArriendoDeLibro_view(request, idLibro):

	# Se obtiene el template
	template = verDetallesDeArriendoDeLibroTemplate

	# Se obtiene el libro
	relacionArriendo = ArriendoDeLibro.objects.get(Q(libro__id__exact = idLibro) & Q(finalizado__exact = False))

	# Se obtiene usuario que esta arrendando el libro
	usuario = Usuario.objects.get(id__exact = relacionArriendo.arrendatario.id)

	# Crear context
	context = {"idLibro": idLibro, "usuario": usuario, "relacionArriendo": relacionArriendo, "precioArriendo": precioArriendo}

	# Se envia respuesta
	return render(request, template, context)

# Vista para iniciar periodo de arriendo
@login_required
def iniciarPeriodoDeArriendo_view(request):

	# Si peticion es AJAX
	if request.is_ajax():

		# idRelacionArriendo
		idLibro = request.GET["idLibro"]

		# Se toma la relacion de arriendo
		relacionArriendo = ArriendoDeLibro.objects.get(Q(libro__id__exact = idLibro) & Q(finalizado__exact = False))

		# Se setea inicio de periodo de arriendo
		relacionArriendo.fechaInicioArriendo = timezone.now()

		# Se setea final de periodo de arriendo
		relacionArriendo.fechaFinalArriendo = timezone.now() + timezone.timedelta(weeks = 1)	

		# Se almacenan cambios de relacion
		relacionArriendo.save()

		# Se obtiene el libro
		libro = relacionArriendo.libro

		# Se cambia el estado del libro
		libro.estado = arrendado

		# Se almacenan cambios en DB
		libro.save()

		# Add message
		messages.add_message(request, messages.SUCCESS, mInicioPeriodoArriendoExitoso)

		# Se crea respuesta
		response = {"success": True}

		# Se envia respuesta
		return JsonResponse(response)


# Vistar para ver detalles de quien quiere arrendar el libro
@login_required
def verDetallesDeQuienQuiereArrendarlo_view(request, idLibro):

	# Se obtiene tempalte
	template = verDetallesDeQuienQuiereArrendarloTemplate

	# idRelacion arriendo
	relacionArriendo = ArriendoDeLibro.objects.get(Q(libro__id__exact = idLibro) & Q(finalizado__exact = False))

	# Se obtiene id de usuario
	idUsuarioQueQuiereArrendar = relacionArriendo.arrendatario.id

	# Se obtiene el usuario
	usuario = Usuario.objects.get(id__exact = idUsuarioQueQuiereArrendar)

	# Se obtiene context
	context = {"usuario": usuario, "idLibro": idLibro, "precioArriendo": precioArriendo}

	# se envia respuesta
	return render(request, template, context)

# Vistar para cambiar estado de libro
@login_required
def cambiarEstadoDeLibro_view(request, idLibro):

	# Se obtiene el template
	template = cambiarEstadoDeLibroTemplate

	# si request es post
	if request.method == "GET":

		# Se crea context
		context = crearContextParaCambiarEstadoDeLibro()

		# Se envia respuesta
		return render(request, template, context)

	# Si request es POST
	else:

		# get form
		formulario = CambiarEstadoDeLibro(request.POST)

		# Si formulario es valido
		if formulario.is_valid():

			# Se limpia la data
			formulario = formulario.cleaned_data

			# Create book 
			libro = LibrosParaArrendar.objects.get(id__exact = idLibro)

			# Se cambia estado de libro
			libro.estado = formulario["estado"]

			# Se almcenca cambio
			libro.save()

			# Add message
			messages.add_message(request, messages.SUCCESS, mCambioDeEstadoExitoso)

			# Redirect to my books
			return redirect(reverse("misLibrosOwner:misLibrosOwner"))

		# If form is not valid
		else:

			# Se crea context
			context = crearContextParaCambiarEstadoDeLibro()

			# Se envia respuesta
			return render(request, template, context)

# Se cea contexto para cambiar estado de libro
def crearContextParaCambiarEstadoDeLibro():

	# Se obtiene formulario
	formulario = CambiarEstadoDeLibro()

	# Se crea context
	context = {"formulario": formulario}

	# Retorno
	return context


# Vista para agregar un libro
@login_required
def agregarLibro_view(request):

	# Template
	template = agregarLibroTemplate

	# Agregar si peticion es POST (se almacena libro)
	# Quizas agregar formulario para agregar libro

	# Si peticion es GET
	if request.method == "GET":

		# Create context
		context = crearContextParaAgregarLibro()

		# Se crea respuesta
		return render(request, template, context)

	# Si request is POST
	else:

		# get form
		formulario = AgregarLibro(request.POST, request.FILES)

		# Si formulario es valido
		if formulario.is_valid():

			# Se limpia la data
			formulario = formulario.cleaned_data

			# Create book and save it on DB
			LibrosParaArrendar(owner = Usuario.objects.get(email__exact = request.user), fechaCreacion = timezone.now(), titulo = formulario["titulo"], autor = formulario["autor"], resumen = formulario["resumen"], foto = formulario["foto"], comentario = formulario["comentario"], estado = disponible).save()

			# Add message
			messages.add_message(request, messages.SUCCESS, mRegistroDeLibroExitoso)

			# Redirect to my books
			return redirect(reverse("misLibrosOwner:misLibrosOwner"))

		# If form is not valid
		else:

			# Create context
			context = crearContextParaAgregarLibro()

			# Se crea respuesta
			return render(request, template, context)


# Funcion para agregar libro
def crearContextParaAgregarLibro():

	# Se obtiene el formulario
	formulario = AgregarLibro()

	# Se crea context
	context = {"formulario" : formulario}

	# Return context
	return context

# Vista para ver todos los libros que tiene un dueño
@login_required
def misLibrosOwner_view(request):

	# Se obtiene el template
	template = misLibrosOwnerTemplate

	# Si request es AJAX
	if request.is_ajax():

		# Se obtienen los libros del dueño
		libros = LibrosParaArrendar.objects.filter(owner__email__exact = request.user)

		# Se obtiene los libros ya mostrados
		idLibrosMostrados = list(set(map(lambda x: int(x), json.loads(request.GET["idLibrosMostrados"]))))

		# Se excluyen los libros ya mostrados
		libros = libros.exclude(id__in=idLibrosMostrados)

		# Mostrar hasta cierta cantidad de libros
		libros = libros[:maximoLibrosPorRequest]

		# Se serializan los libros
		libros = serializers.serialize("python",libros, fields = camposParaSerializarLibros)

		# Se crea respuesta
		response = {"libros": libros}

		# Se envia respuesta
		return JsonResponse(response)

	# Se crea contexto
	context = {"libros": []}

	# Se envia respuesta
	return render(request, template, context)