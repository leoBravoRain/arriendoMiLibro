from django.conf.urls import url

from . import views


app_name = 'misLibrosOwner'

urlpatterns = [

	url(r'misLibrosOwner/$', views.misLibrosOwner_view, name = "misLibrosOwner"),

	url(r'agregarLibro/$', views.agregarLibro_view, name = "agregarLibro"),

	url(r'cambiarEstadoDeLibro/(?P<idLibro>[\w]+)/$', views.cambiarEstadoDeLibro_view, name = "cambiarEstadoDeLibro"),

	url(r'verDetallesDeQuienQuiereArrendarlo/(?P<idLibro>[\w]+)/$', views.verDetallesDeQuienQuiereArrendarlo_view, name = "verDetallesDeQuienQuiereArrendarlo"),

	url(r'iniciarPeriodoDeArriendo/$', views.iniciarPeriodoDeArriendo_view, name = "iniciarPeriodoDeArriendo"),

	url(r'verDetallesDeArriendoDeLibro/(?P<idLibro>[\w]+)/$', views.verDetallesDeArriendoDeLibro_view, name = "verDetallesDeArriendoDeLibro"),

	url(r'terminarPeriodoDeArriendo/$', views.terminarPeriodoDeArriendo_view, name = "terminarPeriodoDeArriendo"),

	url(r'verDetallesDeLibroOwner/(?P<idLibro>[\w]+)/$', views.verDetallesDeLibroOwner_view, name = "verDetallesDeLibroOwner"),

	url(r'editarLibro/(?P<idLibro>[\w]+)/$', views.editarLibro_view, name = "editarLibro"),

	url(r'eliminarLibro/(?P<idLibro>[\w]+)/$', views.eliminarLibro_view, name = "eliminarLibro"),

]

