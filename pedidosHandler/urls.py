from django.urls import path
from pedidosHandler import views

urlpatterns = [
    path(r'pedido/nuevo', views.pedido_nuevo, name='pedido_nuevo'),
    path(r'pedido', views.pedidos, name='pedidos'),
    path(r'pedido/todos', views.pedidos_todos, name='pedidos_todos'),
    path(r'cocina', views.cocina, name='cocina'),
    path(r'api/pedido/nuevo', views.pedido_nuevo_api, name='pedido_nuevo_api'),
    path(r'api/productos/', views.productos_todos_api, name='productos_todos_api'),
    path(r'pedido/<int:id_pedido>', views.pedido_detalle, name='pedido_detalle'),
    path(r'pedido/<int:id_pedido>/pagar', views.pedido_update_estado_pagado, name='pedido_update_estado_pagado'),
    path(r'pedido/<int:id_pedido>/completar', views.pedido_update_estado_completo, name='pedido_update_estado_completo'),
]
