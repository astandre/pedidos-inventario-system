from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import loader
from rest_framework import status
from django.shortcuts import redirect
from inventarioHandler.models import Categoria, Producto
from pedidosHandler.models import Pedido, Item
from django.db.models import Sum, Count
from rest_framework.decorators import api_view
from django.contrib import messages
from .serializers import PedidoSerializer
import datetime
from .utils import constants


# Create your views here.

def pedido_nuevo(request):
    template = loader.get_template('pedidosHandler/pedido_nuevo.html')
    context = {
        'mesas': constants.MESA_CHOICES
    }
    return HttpResponse(template.render(context, request))


@api_view(['GET'])
def productos_todos_api(request):
    if request.method == 'GET':
        categorias = list(Categoria.objects.values().all().order_by("nombre"))

        for categoria in categorias:
            categoria["productos"] = list(Producto.objects.values().filter(categoria=categoria["id_categoria"]))

        return JsonResponse({"categorias": categorias}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"Error": "Only get Allowed"}, status=status.HTTP_403_FORBIDDEN)


@login_required
def pedidos(request):
    pedidos_list = Pedido.objects.filter(pagado=False, fecha__date=datetime.datetime.today()).order_by("pagado")
    template = loader.get_template('pedidosHandler/pedidos.html')
    context = {
        'pedidos': pedidos_list,
    }
    return HttpResponse(template.render(context, request))


@login_required
def pedidos_todos(request):
    pedidos_list = Pedido.objects.all().order_by("fecha")
    template = loader.get_template('pedidosHandler/pedidos.html')
    context = {
        'pedidos': pedidos_list,
    }
    return HttpResponse(template.render(context, request))


def cocina(request):
    pedidos_list = Pedido.objects.filter(terminado=False)
    template = loader.get_template('pedidosHandler/cocina.html')
    context = {
        'pedidos': pedidos_list,
    }
    return HttpResponse(template.render(context, request))


@login_required
def pedido_detalle(request, id_pedido):
    categorias = Categoria.objects.all().order_by("nombre")
    pedido = Pedido.objects.get(id_pedido=id_pedido)
    template = loader.get_template('pedidosHandler/pedido_nuevo.html')
    context = {
        'mesas': constants.MESA_CHOICES,
        'categorias': categorias,
        'pedido': pedido,
    }
    return HttpResponse(template.render(context, request))


@login_required
def pedido_update_estado_pagado(request, id_pedido):
    try:
        pedido = Pedido.objects.get(id_pedido=id_pedido)
    except Pedido.DoesNotExist:
        messages.warning(request, "Pedido no encontrado")
    else:
        pedido.pagado = True
        pedido.save()
        messages.success(request, "Pedido finalizado correctamente")

    return redirect('pedidos')


def pedido_update_estado_completo(request, id_pedido):
    try:
        pedido = Pedido.objects.get(id_pedido=id_pedido)
    except Pedido.DoesNotExist:
        messages.warning(request, "Pedido no encontrado")
    else:
        # actualizando estado de terminado y tiempo que tomo el pedido
        pedido.terminado = True

        tiempo_inicio = pedido.fecha.timestamp()
        ahora = datetime.datetime.now().timestamp()
        tiempo_total = ahora - tiempo_inicio

        tiempo_total = datetime.datetime.utcfromtimestamp(tiempo_total)

        pedido.tiempo_total = tiempo_total

        pedido.save()
        messages.success(request, "Pedido terminado correctamente")

    return redirect('cocina')


def pedido_delete(request, id_pedido):
    try:
        pedido = Pedido.objects.get(id_pedido=id_pedido)
    except Pedido.DoesNotExist:
        messages.warning(request, "Pedido no encontrado")
    else:
        # actualizando estado de terminado y tiempo que tomo el pedido
        pedido.delete()

        messages.success(request, "Pedido eliminado correctamente")

    return redirect('pedidos')


@api_view(['POST'])
def pedido_nuevo_api(request):
    if request.method == 'POST':
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            resp = {}
            if "id" not in serializer.validated_data:
                pedido = serializer.save()
                print(pedido)
                resp["id-orden"] = pedido.id_pedido
            else:
                pedido = serializer.save()
                print(pedido)
                resp["id-orden"] = pedido.id_pedido

            return JsonResponse(resp, status=status.HTTP_200_OK)
        else:
            messages.warning(request, "Ha ocurrido un error")
            return JsonResponse(serializer.errors, status=status.HTTP_404_NOT_FOUND)


@login_required
def reporte_hoy(request):
    template = loader.get_template('pedidosHandler/reporte_hoy.html')

    # Total de dinero en ventas
    total_ventas = Pedido.objects.filter(fecha__date=datetime.datetime.today(), pagado=True,
                                         terminado=True).aggregate(Sum('total'))["total__sum"]

    if total_ventas is not None:
        total_ventas = '%.2f' % total_ventas
    # Todos los items vendidos en el dia
    items = Item.objects.values("producto__nombre", "precio") \
        .filter(pedido__fecha__date=datetime.datetime.today(), pedido__pagado=True, pedido__terminado=True) \
        .annotate(cantidad_prod=Sum('cantidad')).order_by("-cantidad_prod")
    list(items)
    for item in items:
        item["total_aux"] = item["precio"] * item["cantidad_prod"]

    # Item mas y menos vendidos
    item_mas_vendido = items[0]
    item_menos_vendido = items[len(items) - 1]

    # Promedio de completar pedido
    tiempos_serv = Pedido.objects.only("tiempo_total").filter(fecha__date=datetime.datetime.today(),
                                                              terminado=True)
    total_secs = 0
    for tm in tiempos_serv:
        tm = tm.tiempo_total.strftime('%H:%M:%S')
        time_parts = [int(s) for s in tm.split(':')]
        total_secs += (time_parts[0] * 60 + time_parts[1]) * 60 + time_parts[2]
    total_secs = total_secs / len(tiempos_serv)
    total_secs, sec = divmod(total_secs, 60)
    hr, min_time = divmod(total_secs, 60)
    prom_serv = ("%d:%02d:%02d" % (hr, min_time, sec))
    # print(prom_serv)
    context = {
        'total_ventas': total_ventas,
        'item_mas_vendido': item_mas_vendido,
        'item_menos_vendido': item_menos_vendido,
        'items': items,
        'prom_serv': prom_serv
    }
    return HttpResponse(template.render(context, request))


@api_view(['GET'])
def pedidos_frecuencia_api(request):
    if request.method == 'GET':
        pedidos_frec = []
        date_aux = datetime.datetime.now().strftime("%Y-%m-%dT")
        for x in range(12, 23):
            frec_cont = len(Pedido.objects.filter(fecha__date=datetime
                                                  .datetime.today(), fecha__hour__gte=x,
                                                  fecha__hour__lt=x + 1))
            pedidos_frec.append({"x": date_aux + str(x) + ":00:00", "y": frec_cont})
        # print(pedidos_frec)
        return JsonResponse({"pedidos": pedidos_frec}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"Error": "Only get Allowed"}, status=status.HTTP_403_FORBIDDEN)
