from rest_framework import serializers
from .models import *


class PedidoSerializer(serializers.Serializer):
    mesa = serializers.CharField(required=True, max_length=2)
    items = serializers.JSONField(required=True)
    id_pedido = serializers.IntegerField(required=False)
    llevar = serializers.BooleanField(default=False)

    def update(self, instance, validated_data):
        if "id_pedido" in validated_data:
            try:
                mesa = Mesa.objects.get(id_mesa=validated_data["mesa"])
            except Mesa.DoesNotExist:
                print("Mesa does not exists.")
            else:
                pedido = Pedido.objects.get(id_pedido=validated_data["id_pedido"])
                if "llevar" in validated_data and validated_data["llevar"]:
                    pedido.llevar = True
                    pedido.mesa = mesa
                Item.objects.filter(pedido=pedido).delete()
                total = 0
                for item in validated_data["items"]:
                    try:
                        producto = Producto.objects.get(id_producto=item["id_producto"])
                    except Producto.DoesNotExist:
                        print("Producto no encontrado")
                    else:
                        total += producto.precio * item["cantidad"]
                        new_item = Item(producto=producto, cantidad=int(item["cantidad"]), precio=producto.precio,
                                        pedido=pedido)
                        if "llevar" in validated_data and validated_data["llevar"]:
                            new_item.llevar = True
                        else:
                            new_item.llevar = False
                        if "esp" in validated_data:
                            new_item.especificacion = item["esp"]
                        new_item.save()

                pedido.total = float(total)
                # pedido.save()
                # return pedido
        pass

    def create(self, validated_data):
        # print(validated_data)
        mesa = Mesa.objects.get(id_mesa=validated_data["mesa"])
        if "id_pedido" not in validated_data:
            today = datetime.now().date()
            tomorrow = today + timedelta(1)
            today_start = datetime.combine(today, time())
            today_end = datetime.combine(tomorrow, time())
            codigo = Pedido.objects.filter(fecha__lte=today_end, fecha__gte=today_start).latest("codigo").codigo
            codigo += 1
            # print(codigo)
            try:
                cliente = Cliente.objects.get(cedula=9999999999)
            except Cliente.DoesNotExist:
                print("Cliente final added.")
                Cliente(cedula=9999999999, nombres="CONSUMIDOR", apellidos="FINAL").save()
            else:

                # try:
                #     mesa = Mesa.objects.get(id_mesa=validated_data["mesa"])
                # except Mesa.DoesNotExist:
                #     print("Mesa does not exists.")
                # else:
                pedido = Pedido(mesa=mesa, estado=Pedido.PREPARANDO, cliente=cliente, codigo=codigo)
        else:
            pedido = Pedido.objects.get(id_pedido=validated_data["id_pedido"])
            pedido.mesa = mesa
            if pedido.estado is Pedido.PREPARANDO:
                items = Item.objects.filter(pedido=pedido)
                items.delete()

        if "llevar" in validated_data and validated_data["llevar"]:
            pedido.llevar = True

        pedido.save()
        total = 0
        for item in validated_data["items"]:
            try:
                producto = Producto.objects.get(id_producto=item["id_producto"])
            except Producto.DoesNotExist:
                print("Producto no encontrado")
            else:
                total += producto.precio * item["cantidad"]
                new_item = Item(producto=producto, cantidad=int(item["cantidad"]), precio=producto.precio,
                                pedido=pedido, especificacion=item["especificacion"])
                if "llevar" in validated_data and validated_data["llevar"]:
                    new_item.llevar = True
                else:
                    new_item.llevar = False
                new_item.save()

            pedido.total = float(total)
            pedido.save()
        return pedido
