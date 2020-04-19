from rest_framework import serializers
from .models import *


class PedidoSerializer(serializers.Serializer):
    mesa = serializers.CharField(required=False, max_length=2)
    items = serializers.JSONField(required=True)
    id_pedido = serializers.IntegerField(required=False)
    llevar = serializers.BooleanField(default=False)
    estado = serializers.CharField(required=False, max_length=2)
    user = serializers.CharField(required=False, max_length=100)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        # print(validated_data)

        if "id_pedido" not in validated_data:
            today = datetime.now().date()
            tomorrow = today + timedelta(1)
            today_start = datetime.combine(today, time())
            today_end = datetime.combine(tomorrow, time())
            try:
                codigo = Pedido.objects.filter(fecha__lte=today_end, fecha__gte=today_start).latest("codigo").codigo
            except Pedido.DoesNotExist:
                codigo = 1
            else:
                codigo += 1
            # print(codigo)
            # if "user" in validated_data:
            #     cliente = Cliente.objects.get(cedula=9999999999, nombres=validated_data["user"])
            # else:
            #     try:
            #         cliente = Cliente.objects.get(cedula=9999999999)
            #     except Cliente.DoesNotExist:
            #         print("Cliente final added.")
            #         Cliente(cedula=9999999999, nombres="CONSUMIDOR", apellidos="FINAL").save()
            #     else:
            #         cliente = Cliente.objects.get(cedula=9999999999)

            pedido = Pedido(estado=Pedido.PREPARANDO, codigo=codigo)
        else:
            pedido = Pedido.objects.get(id_pedido=validated_data["id_pedido"])
            # if pedido.estado is Pedido.PREPARANDO:
            items = Item.objects.filter(pedido=pedido)
            items.delete()

        if "mesa" in validated_data:
            mesa = Mesa.objects.get(id_mesa=validated_data["mesa"])
            pedido.mesa = mesa
        elif "llevar" in validated_data and validated_data["llevar"]:
            pedido.llevar = True

        if "estado" in validated_data:
            pedido.estado = validated_data["estado"]

        if "user" in validated_data and len(validated_data["user"]) > 0:
            pedido.cliente = validated_data["user"]

        pedido.save()
        total = 0
        for item in validated_data["items"]:
            # print(item)
            try:
                producto = Producto.objects.get(id_producto=item["id_producto"])
            except Producto.DoesNotExist:
                print("Producto no encontrado")
            else:
                total += producto.precio * item["cantidad"]
                new_item = Item(producto=producto, cantidad=int(item["cantidad"]), precio=producto.precio,
                                pedido=pedido, especificacion=item["especificacion"],
                                entregado=item["entregado"], cocinado=item["cocinado"])
                if pedido.llevar:
                    new_item.llevar = True
                else:
                    new_item.llevar = item["llevar"]
                new_item.save()

            pedido.total = float(total)
            pedido.save()
        return pedido
