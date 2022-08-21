#Importamos forms
from django import forms



lista=[('A','30 Cuotas'),  ('B','60 Cuotas'), ('C', '90 Cuotas')]


class PrestamoForm(forms.Form):
    monto = forms.IntegerField(label="Monto", required=True)
    tipo = forms.CharField(label='Que Tipo de Prestamo Necesitas?', widget=forms.Select(choices=lista))

 

class RegistroForm(forms.Form):
    username= forms.CharField(label="username", required=True)
    cliente_id = forms.CharField(label="cliente_id", required=True)
    email = forms.CharField(label="email", required=False)
    pwd = forms.CharField(label="pwd", required=False)

