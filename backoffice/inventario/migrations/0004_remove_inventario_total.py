# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-16 20:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0003_auto_20180716_1922'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventario',
            name='total',
        ),
    ]