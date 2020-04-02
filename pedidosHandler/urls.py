from django.urls import path
from pedidosHandler import views

urlpatterns = [
    # path(r'pedido/nuevo', views.pedido_nuevo, name='pedido_nuevo'),

    path(r'pedido', views.pedidos, name='pedidos'),
    path(r'pedido/todos', views.pedidos_todos, name='pedidos_todos'),
    path(r'pedido/status', views.get_changes_pedidos, name='get_changes_pedidos'),
    path(r'cocina', views.cocina, name='cocina'),
    path(r'api/mesas', views.mesas_list_api, name='mesas_list_api'),
    path(r'api/pedido/nuevo', views.pedido_nuevo_api, name='pedido_nuevo_api'),
    path(r'api/pedido/today', views.all_pedido_today_api, name='all_pedido_today_api'),
    path(r'api/pedido/estado/<str:estado>', views.pedido_by_estado_api, name='pedido_by_estado_api'),
    path(r'api/pedido/preparando', views.pedido_preparando_api, name='pedido_preparando_api'),
    path(r'api/pedido/<int:id_pedido>', views.pedido_detalle_api, name='pedido_detalle_api'),
    path(r'api/productos', views.productos_todos_api, name='productos_todos_api'),
    path(r'api/pedido/frec', views.pedidos_frecuencia_api, name='pedidos_frecuencia_api'),
    path(r'pedido/<int:id_pedido>', views.pedido_detalle, name='pedido_detalle'),
    path(r'pedido/<int:id_pedido>/pagar', views.pedido_update_estado_pagado, name='pedido_update_estado_pagado'),
    path(r'pedido/<int:id_pedido>/completar', views.pedido_update_estado_completo,
         name='pedido_update_estado_completo'),
    path(r'pedido/<int:id_pedido>/borrar', views.pedido_delete, name='pedido_delete'),
    path(r'reporte/hoy', views.reporte_hoy, name='reporte_hoy'),
]
