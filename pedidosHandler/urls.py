from django.urls import path
from pedidosHandler import views


urlpatterns = [
    path(r'pedido/nuevo', views.pedido_nuevo, name='pedido_nuevo'),
    path(r'pedido', views.pedidos, name='pedidos'),
]
