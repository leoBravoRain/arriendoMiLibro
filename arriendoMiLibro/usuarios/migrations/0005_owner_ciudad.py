# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-26 14:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_ciudad'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='ciudad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='usuarios.Ciudad'),
        ),
    ]
