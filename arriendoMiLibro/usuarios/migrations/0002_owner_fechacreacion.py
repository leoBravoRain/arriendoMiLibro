# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-23 03:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='fechaCreacion',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 23, 3, 25, 0, 882437, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
