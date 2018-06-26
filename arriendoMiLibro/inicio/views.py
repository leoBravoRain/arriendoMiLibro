# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from forms import RegistrarOwner, LoginOwner
from django.core.urlresolvers import reverse
from django.contrib import messages
from usuarios.models import Usuario, Ciudad
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from buscarLibros.views import enviarEmail

# Templates
inicioTemplate = "inicio/inicio/inicio.html"
loginTemplate = "inicio/login/login.html"

# Mensajes
mErrorIntenteNuevamente = "Ocurrio un error, porfavor intentelo nuevamente."
mUsuarioNoEstaRegistrado = "Este email no esta registrado. Porfavor, debe registrarse antes de entrar."
mRegistroExitoso = "¡ Registro totalmente exitoso !"
mLogoutExitoso = "Ha cerrado su sesión exitosamente. ¡ Nos vemos !"
mLoginExitoso = "Ha iniciado sesión exitosamente."
mErrorUsuarioYaEstaRegistrado = "Este mail ya esta registrado, por lo que solo debe ingresar con su email y clave."

# Variables generales

cualquierTitulo = "cualquierTitulo"
cualquierCiudad = "cualquierCiudad"

# Create your views here.

# Vista para logout
def logout_view(request):

	# Se realiza logout
	logout(request)

	# Se agrega mensaje de exito de logout
	messages.add_message(request, messages.SUCCESS, mLogoutExitoso)

	# Se redirige hacia inicio
	return redirect(reverse("inicio:inicio"))

# Vista para hacer login
def login_view(request):

	# Se obtiene el template
	template = loginTemplate

	# Si request es GET
	if request.method == "GET":

		# Funcion para crear contexto a login
		context = crearContextParaLoginView()

		# Se envia respuesta
		return render(request, template, context)

	# Si respuesta es POST 
	else:

		# Si se quiere loguear
		if "login_button" in request.POST:

			# Se obtiene formulario de login
			formulario = LoginOwner(request.POST)
			
			# Si formulario es valido
			if formulario.is_valid():

				# Se limpia la data
				formulario = formulario.cleaned_data

				# funcion para autenticar a usuario
				user = authenticate(username = formulario["email"], password = formulario["password"])

				#Si es correcto el login
				if user is not None:

					if user.is_active:

						login(request,user)

						# Se agrega mensaje de exito de logout
						messages.add_message(request, messages.SUCCESS, mLoginExitoso)

						# Redirigir hacia pagina dada en aprametro next de url
						urlParaRedirigir = obtenerUrlParaRedirigir(request)

						return redirect(urlParaRedirigir)

				else:

					# Se agrega mensaje de error en login
					messages.add_message(request, messages.WARNING, mErrorIntenteNuevamente)

					print 'usuario no registrado'

					# Funcion para crear contexto a login
					context = crearContextParaLoginView()

					# Se crea respuesta
					return render(request, template, context)

			# Si es que no es valido
			else:

				# Se agrega mensaje de error en login
				messages.add_message(request, messages.WARNING, mErrorIntenteNuevamente)

				print 'Ocurrio un error'

				# Funcion para crear contexto a login
				context = crearContextParaLoginView()

				# Se crea respuesta
				return render(request, template, context)

		# Si usuario se quiere registrar
		elif "register_button" in request.POST:

			# Se obtiene formulario de login
			formulario = RegistrarOwner(request.POST, request.FILES)
			
			# Si formulario es valido
			if formulario.is_valid():

				# Se limpia la data
				formulario = formulario.cleaned_data

				# Se toma el email 
				email = formulario["email"]

				# Se toma el password
				password = formulario["password"]

				# Se chequea si existe el usuario
				auth_user = User.objects.filter(username__exact = email)

				# Si usuario ya esta registrado
				if auth_user:

					# Se agrega mensaje de error que email ya esta registrado
					messages.add_message(request, messages.WARNING, mErrorUsuarioYaEstaRegistrado)

					# Se envia respuesta
					return redirect(request.META.get('HTTP_REFERER'))


				# Si usuario no esta registrado
				else:

					# Se crea usuario de modelo de usuario de django
					auth_user = User.objects.create_user(username = email, password = password)

					# Se almacena en DB
					auth_user.save()

					# Se crea Usuario
					owner = Usuario(user = auth_user, nombre = formulario["nombre"], email = email, numeroContacto = formulario["numeroContacto"], password = password, foto = formulario["foto"], fechaCreacion = timezone.now(), ciudad = formulario["ciudad"])

					# Se almacena en DB
					owner.save()

					# funcion para autenticar a usuario
					user = authenticate(username = email, password = password)

					#Si es correcto el login
					if user is not None:

						if user.is_active:

							# Se agrega mensaje de exito de registro
							messages.add_message(request, messages.SUCCESS, mRegistroExitoso)

							print 'Registro exitoso'

							# Se loguea
							login(request,user)

							# Redirigir hacia pagina dada en aprametro next de url
							urlParaRedirigir = obtenerUrlParaRedirigir(request)

							# Se retorna respuesta
							return redirect(urlParaRedirigir)

					else:

						# Se agrega mensaje de exito de registro
						messages.add_message(request, messages.SUCCESS, mRegistroExitoso)

						print 'Se ha registrado un usuario'

						# Funcion para crear contexto a login
						context = crearContextParaLoginView()

						# Se crea respuesta
						return render(request, template, context)

			# Si es que no es valido
			else:

				# Se agrega mensaje de error en login
				messages.add_message(request, messages.WARNING, mErrorIntenteNuevamente)

				print 'Ocurrio un error'

				# Funcion para crear contexto a login
				context = crearContextParaLoginView()

				# Se crea respuesta
				return render(request, template, context)

# Funcion para redirigir hacia pagina dada en aprametro next de url
def obtenerUrlParaRedirigir(request):

	# Se obtiene url completa
	redirigirHacia = request.META.get('HTTP_REFERER')

	# Se corta el string desde 'next='
	desdeDondeCortar = 'next='

	# inicio de corte de string
	inicioCorte = redirigirHacia.find(desdeDondeCortar) + len(desdeDondeCortar)

	# inicio de corte de string
	finCorte = len(redirigirHacia)

	# Se obtiene nueva url
	redirigirHacia = redirigirHacia[inicioCorte: finCorte]

	# se retorna
	return redirigirHacia

# Funcion para crear context para login
def crearContextParaLoginView():

	# Se obtiene el formulario de registro
	formularioRegistro = RegistrarOwner

	# Se obtiene formulario de login
	formularioLogin = LoginOwner

	# Se crea context
	context = {"formularioRegistro": formularioRegistro, "formularioLogin": formularioLogin}

	# Se retorna context
	return context


# vista para retornar el inicio de la app
def inicio_view(request):

	# Funcion para testear el enio de email
	enviarEmail()

	# Se obtiene el template
	template = inicioTemplate

	# Se obtienen las ciudades en donde se puede arrendar
	ciudades = Ciudad.objects.all()

	# Se setea el context
	context = {"ciudades" : ciudades, "cualquierTitulo": cualquierTitulo, "cualquierCiudad" : cualquierCiudad}

	# Se envia respuesta
	return render(request, template, context)