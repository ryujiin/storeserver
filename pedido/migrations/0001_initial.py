# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-24 17:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cliente', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoPedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('slug_estado', models.CharField(blank=True, max_length=120, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GrupoMetodoEnvio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('titulo', models.CharField(blank=True, max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MetodoEnvio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('icono', models.CharField(blank=True, max_length=20)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=12)),
                ('grupo_metodo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pedido.GrupoMetodoEnvio')),
            ],
        ),
        migrations.CreateModel(
            name='MetodoPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('titulo', models.CharField(blank=True, max_length=100, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('img', models.ImageField(blank=True, upload_to=b'tienda')),
            ],
        ),
        migrations.CreateModel(
            name='ModificacionPedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, db_index=True)),
                ('estado_actual', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('id_pago', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('descripcion', models.CharField(blank=True, max_length=100, null=True)),
                ('transaccion', models.CharField(blank=True, max_length=100, null=True)),
                ('valido', models.BooleanField(default=False)),
                ('metodo_pago', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pedido.MetodoPago')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_pedido', models.CharField(blank=True, max_length=120, null=True)),
                ('gasto_envio', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('fecha_compra', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('fecha_final', models.DateTimeField(blank=True, null=True)),
                ('estado_pedido', models.CharField(choices=[(b'autenticado', '<b>Autenticado</b> - Usted se encuentra idenficado en la plataforma'), (b'metodo_envio', '<b>Metodo de Envio</b> - Ya selecciono el metodo de envio, esperando metodo de pago'), (b'metodo_pago', '<b>Metodo de Pago</b> - Ya selecciono el metodo de pago'), (b'esperando_pago', '<b>Esperando Pago</b> - Ya selecciono el metodo de pago, pero aun no se realiza el pago'), (b'pagado', '<b>Pagado</b> - El pago se realizo correctamente, espere el envio del producto'), (b'error_pago', '<b>Error en Pago</b> - Ocurrio un error al pagar'), (b'enviado', '<b>Enviado</b> - El producto fue enviado'), (b'devuelto', '<b>Devuelto</b> - El producto fue devuelto'), (b'fucionado', '<b>Fusionado</b> - Este Pedido se Fusiono con otro pedido')], default=b'autenticado', max_length=120)),
                ('pagado', models.BooleanField(default=False)),
                ('enviado', models.BooleanField(default=False)),
                ('telefono_pedido', models.CharField(blank=True, max_length=100)),
                ('direccion_envio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cliente.Direccion')),
                ('metodo_pago', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pedido.MetodoPago')),
                ('metodoenvio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pedido.MetodoEnvio')),
                ('pago_pedido', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pedido.Pago')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Pedido', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='modificacionpedido',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedido.Pedido'),
        ),
    ]
