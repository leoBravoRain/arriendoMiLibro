# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-26 19:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0003_arriendodelibro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arriendodelibro',
            name='arrendatario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Owner'),
        ),
    ]
