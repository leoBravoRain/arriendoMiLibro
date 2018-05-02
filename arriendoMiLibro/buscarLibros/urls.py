from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'buscarLibros'

urlpatterns = [

	url(r'confirmarArriendoDeLibro/(?P<idLibro>[\w]+)/$', views.confirmarArriendoDeLibro_view, name = "confirmarArriendoDeLibro"),

	url(r'buscarLibros/(?P<titulo>[\w\s]+)/(?P<ciudad>[\w]+)/$', views.buscarLibros_view, name = "buscarLibros"),

	url(r'verDetallesDeLibro/(?P<idLibro>[\w]+)/$', views.verDetallesDeLibro_view, name = "verDetallesDeLibro"),

	url(r'arrendarLibro/(?P<idLibro>[\w]+)/$', views.arrendarLibro_view, name = "arrendarLibro"),
	
	url(r'verDetallesOwner/(?P<idOwner>[\w]+)/$', views.verDetallesOwner_view, name = "verDetallesOwner"),

]

# La sigueinte linea se agrega para que Django cargue los archivos estaticos

# https://docs.djangoproject.com/en/1.11/howto/static-files/

# Se debe agregar en la aplicacion desde donde se cargara el archivo ya que el link 
# corresponde a localHost(o lo que sea)/nombreDeLaAplicacion/rutaDeLaImagen, entonces
# el archivo ahora la siguiente ruta localHost(o lo que sea)/nombreDeLaAplicacion/rutaDeLaImagen/media/rutaDelArchivo, 
# entonces el media seguido del nombre de la aplicacion es el patro que decta la siguiente linea y lo envia al MEDIA_ROOT cargandose correctamente la imagen

if settings.DEBUG:

    # La siguiente es para que Django sirva los archivos subidos por el usuario (Esto solo es para desarrollo)

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

