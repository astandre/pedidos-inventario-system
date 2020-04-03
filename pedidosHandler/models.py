from django.db import models
from inventarioHandler.models import Producto
from datetime import datetime, timedelta, time


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


class Mesa(models.Model):
    id_mesa = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=4, null=False)
    mesa = models.CharField(max_length=40, null=False)

    class Meta:
        default_related_name = 'mesas'
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"

    def __str__(self):
        return f"{self.mesa}"


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


class PedidoManager(models.Manager):
    def pedidos_today(self):
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())
        return self.filter(fecha__lte=today_end, fecha__gte=today_start)

    def pedidos_today_json(self):
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())
        return list(self.filter(fecha__lte=today_end, fecha__gte=today_start).values())

    def pedidos_by_estado_json(self, status):
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())
        status = status.upper()
        return list(self.filter(estado=status, fecha__lte=today_end, fecha__gte=today_start)
                    .values("id_pedido", "codigo", "mesa__mesa", "estado", "llevar", "fecha", "total"))


class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    codigo = models.IntegerField(blank=False, null=False, default=1)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, null=True, blank=True, on_delete=models.CASCADE)
    llevar = models.BooleanField(default=False)
    fecha = models.DateTimeField(default=datetime.now)
    PREPARANDO = "P"
    PREPARADO = "C"
    SERVIDO = "S"
    PAGADO = "G"
    ESTADO_CHOICES = (
        (PREPARANDO, 'PREPARANDO'),
        (PREPARADO, 'PREPARADO'),
        (SERVIDO, 'COMPLETO'),
        (PAGADO, 'PAGADO'),
    )
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES, blank=False, default=PREPARANDO)
    tiempo_total = models.TimeField(blank=True, null=True)
    total = models.DecimalField(default=0, max_digits=5, decimal_places=2)

    objects = PedidoManager()

    class Meta:
        default_related_name = 'pedidos'
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return str(self.codigo)


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
