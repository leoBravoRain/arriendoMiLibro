# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-27 00:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0004_auto_20180426_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='arriendodelibro',
            name='finalizado',
            field=models.BooleanField(default=False),
        ),
    ]
