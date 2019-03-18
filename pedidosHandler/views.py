from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import loader
from rest_framework import status
from django.shortcuts import redirect
from inventarioHandler.models import Categoria, Producto
from pedidosHandler.models import Pedido
from .forms import PedidoForm
from django.db.models import Q
from rest_framework.decorators import api_view
from django.contrib import messages
from .serializers import PedidoSerializer
import datetime


# Create your views here.
# TODO create method to get the price

@login_required
def pedido_nuevo(request):
    template = loader.get_template('pedidosHandler/pedido_nuevo.html')
    form = PedidoForm()
    context = {
        'form': form,
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
    pedidos_list = Pedido.objects.filter(pagado=False).order_by("pagado")
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
    form = PedidoForm()
    context = {
        'form': form,
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
        # print(ahora)
        # print(tiempo_inicio)
        # print(datetime.datetime.utcfromtimestamp(tiempo_total).strftime('%H:%M:%S'))
        tiempo_total = datetime.datetime.utcfromtimestamp(tiempo_total)

        pedido.tiempo_total = tiempo_total

        pedido.save()
        messages.success(request, "Pedido terminado correctamente")

    return redirect('cocina')


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
