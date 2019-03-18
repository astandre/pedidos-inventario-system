from django.db import models
from inventarioHandler.models import Producto
from .utils import constants
from datetime import datetime

# Create your models here.


class Direccion(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    provincia = models.CharField(max_length=200, null=False)
    ciudad = models.CharField(max_length=12, null=False)
    calles = models.CharField(max_length=12, null=False)

    class Meta:
        default_related_name = 'direccion'
        verbose_name = "Direccion"
        verbose_name_plural = "Direcciones"

    def __str__(self):
        return self.provincia + " (" + self.ciudad + "), " + self.calles


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=12, null=False)
    nombres = models.CharField(max_length=200, null=False)
    apellidos = models.CharField(max_length=200, null=True, blank=True)
    telefono_fijo = models.CharField(max_length=16, null=True, blank=True)
    telefono_movil = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    direccion = models.ForeignKey(Direccion, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'clientes'
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.cedula


class Pedido(models.Model):
    # TODO add begin time and end time
    # TODO make id_pedido unique for day
    id_pedido = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mesa = models.CharField(max_length=2, choices=constants.MESA_CHOICES, blank=False, default=constants.A1)
    fecha = models.DateTimeField(default=datetime.now)
    pagado = models.BooleanField(default=False)
    terminado = models.BooleanField(default=False)
    tiempo_total = models.TimeField(blank=True, null=True)
    total = models.DecimalField(null=False, max_digits=5, decimal_places=2)

    class Meta:
        default_related_name = 'pedidos'
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return self.cliente.nombres


class Item(models.Model):
    # TODO rewrite when item is saved to store actual price
    id_item = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(blank=False, null=False, default=1)
    especificacion = models.CharField(max_length=200, null=True, blank=True)
    llevar = models.BooleanField(default=False)
    precio = models.DecimalField(null=False, max_digits=5, decimal_places=2)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'items'
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return self.producto.nombre
