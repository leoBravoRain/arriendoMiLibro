# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from usuarios.models import Usuario, Ciudad
from libros.models import LibrosParaArrendar, ArriendoDeLibro

# Register your models here.

admin.site.register(Usuario)
admin.site.register(LibrosParaArrendar)
admin.site.register(Ciudad)
admin.site.register(ArriendoDeLibro)