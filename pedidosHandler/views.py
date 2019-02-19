from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from inventarioHandler.models import Categoria
from pedidosHandler.models import Pedido
from .forms import PedidoForm
from django.db.models import Q


# Create your views here.
# TODO create method to get the price

@login_required
def pedido_nuevo(request):
    categorias = Categoria.objects.all()
    template = loader.get_template('pedidosHandler/pedido_nuevo.html')
    form = PedidoForm()
    # TODO try to create custom form
    context = {
        'form': form,
        'categorias': categorias,
    }
    return HttpResponse(template.render(context, request))


@login_required
def pedidos(request):
    pedidos_list = Pedido.objects.filter(~Q(estado="G"))
    print(pedidos_list)
    template = loader.get_template('pedidosHandler/pedidos.html')
    context = {
        'pedidos': pedidos_list,
    }
    return HttpResponse(template.render(context, request))
