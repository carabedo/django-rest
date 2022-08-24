from rest_framework import serializers 
from .models import Sucursales

 
class SucursalesSerializer(serializers.ModelSerializer):
     class Meta:
        model = Sucursales
        #indicamos que use todos los campos
        fields = "__all__"
        #les decimos cuales son los de solo lectura 


from .models import Movimientos

class MovimientosSerializer(serializers.ModelSerializer):
     class Meta:
        model = Movimientos
        #indicamos que use todos los campos
        fields = "__all__"
        #les decimos cuales son los de solo lectura 

from .models import Prestamos

class PrestamosSerializer(serializers.ModelSerializer):
     class Meta:
        model = Prestamos
        fields = "__all__"

from .models import Empleados

class EmpleadosSerializer(serializers.ModelSerializer):
     class Meta:
        model = Empleados
        fields = "__all__"