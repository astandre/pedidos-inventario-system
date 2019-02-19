from django.db import models
from inventarioHandler.models import Producto


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
    id_pedido = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    A1 = 'AI'
    A2 = 'AD'
    A3 = 'AT'
    A4 = 'AM'
    A5 = 'AE'
    B1 = 'B1'
    B2 = 'B2'
    B3 = 'B3'
    B4 = 'B4'
    B5 = 'B5'
    B6 = 'B6'
    B7 = 'B7'
    B8 = 'B8'
    B9 = 'B9'
    MESA_CHOICES = (
        (A1, 'Afuera puerta izquierda'),
        (A2, 'Afuera puerta derecha'),
        (A3, 'Afuera televisor'),
        (A4, 'Afuera meson'),
        (A5, 'Afuera extra1'),
        (B1, 'Adentro #1'),
        (B2, 'Adentro #2'),
        (B3, 'Adentro #3'),
        (B4, 'Adentro #4'),
        (B5, 'Adentro #5'),
        (B6, 'Adentro #6'),
        (B7, 'Adentro #7'),
        (B8, 'Adentro #8'),
        (B9, 'Adentro extra 1'),

    )
    mesa = models.CharField(max_length=2, choices=MESA_CHOICES, blank=False, default=A1)
    PREPARANDO = "P"
    COMPLETO = "C"
    PAGADO = "G"
    ESTADO_CHOICES = (
        (PREPARANDO, 'PREPARANDO'),
        (COMPLETO, 'COMPLETO'),
        (PAGADO, 'PAGADO'),
    )
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, blank=False, default=PREPARANDO)
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
    especificacion = models.CharField(max_length=200, null=True,blank=True)
    precio = models.DecimalField(null=False, max_digits=5, decimal_places=2)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'items'
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return self.producto.nombre
