from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'inicio'

urlpatterns = [

	url(r'^$', views.inicio_view, name="inicio"),

	url(r'login/$', views.login_view, name = "login"),

	url(r'logout/$', views.logout_view, name = "logout"),
	
]