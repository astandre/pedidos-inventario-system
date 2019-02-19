from django import forms
from .models import *


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cedula', 'nombres', 'apellidos', 'telefono_fijo', 'telefono_movil', 'email', 'direccion']


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['mesa']
