# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-24 23:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ofcatalogo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InsumoProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(blank=True, default=0)),
                ('unidad', models.CharField(choices=[(b'und', b'Unidad'), (b'par', b'Par'), (b'fr', b'Fardo'), (b'pq', b'Paquete'), (b'm', b'Metros'), (b'cm', b'Centimetros')], max_length=100)),
                ('insumo', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='ofcatalogo.Insumo')),
                ('producto', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='ofcatalogo.Producto')),
            ],
        ),
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='insumoproducto',
            name='seccion',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='produccion.Seccion'),
        ),
    ]