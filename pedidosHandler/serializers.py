from rest_framework import serializers
from .models import *
import logging


#
class PedidoSerializer(serializers.Serializer):
    mesa = serializers.CharField(required=True, max_length=2)
    items = serializers.JSONField(required=True)
    pedido = serializers.IntegerField(required=False)
    id = serializers.IntegerField(required=False)
    total = serializers.DecimalField(required=True, max_digits=5, decimal_places=2)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):

        try:
            cliente = Cliente.objects.get(cedula=9999999999)
        except Cliente.DoesNotExist:
            print("Cliente final added.")
            Cliente(cedula=9999999999, nombres="CONSUMIDOR", apellidos="FINAL").save()
        else:
            pedido = Pedido(mesa=validated_data["mesa"], estado="P", cliente=cliente, total=validated_data["total"])
            pedido.save()
            # print(pedido.id_pedido)

            for item in validated_data["items"]:
                item["precio"] = item["precio"].replace(",", ".")
                item["precio"] = float(item["precio"])
                try:
                    producto = Producto.objects.get(id_producto=item["id"])
                except Producto.DoesNotExist:
                    print("Producto no encontrado")
                else:
                    try:
                        pedido = Pedido.objects.get(id_pedido=pedido.id_pedido)
                    except Pedido.DoesNotExist:
                        print("Pedido no encontrado")
                    else:

                        new_item = Item(producto=producto, cantidad=item["cantidad"], precio=item["precio"],
                                        especificacion=item["esp"], pedido=pedido)
                        print(new_item)
                        new_item.save()
            return pedido
