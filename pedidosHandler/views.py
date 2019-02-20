from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import loader
from rest_framework import status
from django.shortcuts import redirect
from inventarioHandler.models import Categoria
from pedidosHandler.models import Pedido
from .forms import PedidoForm
from django.db.models import Q
from rest_framework.decorators import api_view
from django.contrib import messages
from .serializers import PedidoSerializer
from .utils import constants


# Create your views here.
# TODO create method to get the price

@login_required
def pedido_nuevo(request):
    categorias = Categoria.objects.all().order_by("nombre")
    template = loader.get_template('pedidosHandler/pedido_nuevo.html')
    form = PedidoForm()
    # TODO instead of form send data to render manually
    context = {
        'form': form,
        'categorias': categorias,
    }
    return HttpResponse(template.render(context, request))


@login_required
def pedidos(request):
    pedidos_list = Pedido.objects.filter(~Q(estado=constants.PAGADO))
    template = loader.get_template('pedidosHandler/pedidos.html')
    context = {
        'pedidos': pedidos_list,
    }
    return HttpResponse(template.render(context, request))


def cocina(request):
    pedidos_list = Pedido.objects.filter(estado=constants.PREPARANDO)
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
        pedido.estado = constants.PAGADO
        pedido.save()
        messages.success(request, "Pedido finalizado correctamente")

    return redirect('pedidos')


def pedido_update_estado_completo(request, id_pedido):
    try:
        pedido = Pedido.objects.get(id_pedido=id_pedido)
    except Pedido.DoesNotExist:
        messages.warning(request, "Pedido no encontrado")
    else:
        pedido.estado = constants.COMPLETO
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
                old_pedido = Pedido.objects.get(id_pedido=serializer.validated_data["id"])
                print("Must update pedido")
                print(old_pedido)

            return JsonResponse(resp, status=status.HTTP_200_OK)
        else:
            messages.warning(request, "Ha ocurrido un error")
            return JsonResponse(serializer.errors, status=status.HTTP_404_NOT_FOUND)
