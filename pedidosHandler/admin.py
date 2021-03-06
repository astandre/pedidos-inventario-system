from django.contrib import admin
from .models import *


# Register your models here.


class ItemsInline(admin.TabularInline):
    model = Item
    extra = 5


class ItemsAdmin(admin.ModelAdmin):
    list_display = ('producto', 'pedido', 'precio', 'cocinado', 'entregado')
    list_filter = ['producto__nombre', 'pedido__cliente', 'cocinado', 'entregado']


class PedidosAdmin(admin.ModelAdmin):
    inlines = [ItemsInline]
    search_fields = ['id_pedido']
    list_display = ('id_pedido', 'cliente', 'total', 'fecha', 'estado', 'tiempo_total', 'mesa')
    # list_filter = ['cliente__cedula', 'cliente__nombres', 'cliente__apellidos', 'estado', 'fecha', 'mesa__mesa']
    list_filter = ['estado', 'fecha', 'mesa__mesa']


class ClientesAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombres', 'apellidos', 'telefono_fijo', 'telefono_movil', 'email')
    search_fields = ['cedula', 'nombres', 'apellidos']
    list_per_page = 10


class DireccionesAdmin(admin.ModelAdmin):
    list_display = ('provincia', 'ciudad', 'calles')
    search_fields = ['provincia', 'ciudad', 'calles']


class MesaAdmin(admin.ModelAdmin):
    search_fields = ['codigo']
    list_display = ('codigo', 'mesa')
    list_filter = ['codigo', 'mesa']


admin.site.register(Cliente, ClientesAdmin)
admin.site.register(Direccion, DireccionesAdmin)
admin.site.register(Pedido, PedidosAdmin)
admin.site.register(Mesa, MesaAdmin)
admin.site.register(Item, ItemsAdmin)
