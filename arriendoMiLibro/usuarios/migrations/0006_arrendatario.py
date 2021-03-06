# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-26 19:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuarios', '0005_owner_ciudad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arrendatario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=500)),
                ('email', models.CharField(max_length=500)),
                ('numeroContacto', models.CharField(max_length=500)),
                ('password', models.CharField(max_length=500)),
                ('foto', models.ImageField(null=True, upload_to='imagenes/owners')),
                ('fechaCreacion', models.DateTimeField()),
                ('ciudad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='usuarios.Ciudad')),
                ('user', models.OneToOneField(default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
