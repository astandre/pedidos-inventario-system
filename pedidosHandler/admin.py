from django.contrib import admin
from .models import *


# Register your models here.


class ItemsInline(admin.TabularInline):
    model = Item
    extra = 5


class ItemsAdmin(admin.ModelAdmin):
    list_display = ('producto', 'pedido', 'precio')
    list_filter = ['producto__nombre', 'pedido__cliente']


class PedidosAdmin(admin.ModelAdmin):
    inlines = [ItemsInline]
    search_fields = ['id_pedido']
    list_display = ('id_pedido', 'cliente', 'total', 'fecha', 'pagado', 'terminado')
    list_filter = ['cliente__cedula', 'cliente__nombres', 'cliente__apellidos', 'pagado','terminado']


class ClientesAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombres', 'apellidos', 'telefono_fijo', 'telefono_movil', 'email')
    search_fields = ['cedula', 'nombres', 'apellidos']
    list_per_page = 10


class DireccionesAdmin(admin.ModelAdmin):
    list_display = ('provincia', 'ciudad', 'calles')
    search_fields = ['provincia', 'ciudad', 'calles']


admin.site.register(Cliente, ClientesAdmin)
admin.site.register(Direccion, DireccionesAdmin)
admin.site.register(Pedido, PedidosAdmin)
admin.site.register(Item, ItemsAdmin)
