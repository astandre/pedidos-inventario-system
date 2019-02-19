from django.contrib import admin
from .models import *


# Register your models here.

class ProductosInline(admin.TabularInline):
    model = Producto
    extra = 5


class ProductosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'disponible')
    list_filter = ['categoria__nombre', 'disponible']
    search_fields = ['nombre']


class CategoriasAdmin(admin.ModelAdmin):
    inlines = [ProductosInline]
    list_display = ['nombre']
    search_fields = ['nombre']


admin.site.register(Categoria, CategoriasAdmin)
admin.site.register(Producto, ProductosAdmin)
