from django.db import models


# Create your models here.


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)

    class Meta:
        default_related_name = 'categorias'
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=300, null=True)
    disponible = models.BooleanField(default=True)
    # tamano_producto =
    precio = models.DecimalField(null=False, max_digits=5, decimal_places=2)
    # imagen = models.CharField(max_length=300)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'productos'
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.categoria.nombre + " -  " + self.nombre
