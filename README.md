# django-restframework

## indice:

- [instalacion](https://github.com/carabedo/django-restk#instalacion)
- [serializadores](https://github.com/carabedo/django-rest#serialización)
- [apiviews](https://github.com/carabedo/django-rest#apiviews)
- [requests GET PUT DELETE]()
- [permisos](https://github.com/carabedo/django-rest#permisos)
- [hipervinculos]()
- [viewsets y routers]()

# Instalacion:

```
pip3 install djangorestframework
```

Vamos agregarle una API a nuestro proyecto django, para eso agreguemos la app en `settings.py`:


```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

# Serialización

Entedemos por serializacion la accion de convertir la informacion en la base de datos en json para la respuesta http y tambien nos interesa la relacion inversa, es decir poder impactar en la base de datos a partir de un post json. La idea es generar una API para consultar los movimientos de diferentes usuarixs, asi como creamos un modelo para la tabla de movimientos, vamos a crear un 'serializador' en el archivo `serializers.py`en la misma app de los modelos que querramos disponibilizar en la api.


```python
from rest_framework import serializers 
from .models import Sucursales

 
class SucursalesSerializer(serializers.ModelSerializer):
     class Meta:
        model = Sucursales
        #indicamos que use todos los campos
        fields = "__all__"
        #les decimos cuales son los de solo lectura 

```
Esta clase, automaticamente genera una serializacion de las filas, al heradar la clase `serializers.ModelSerializer` hacemos todo el trabajo.



Probemos que esto funciona:

Ejecutemos el siguiente codigo en la consola de django `python3 manage.py shell`

```python
from main.models import Sucursales
from main.serializers import SucursalesSerializer
from rest_framework.renderers import JSONRenderer 
from rest_framework.parsers import JSONParser

participante = Sucursales.objects.get(id=1) 

serializer = SucursalesSerializer(participante) 
serializer.data

```
Deberiamos ver en consola:

```
{'id': 1, 'calle': 'AV. CORRIENTES ', 'altura': '3328'}
```

En este punto, hemos traducido la instancia del modelo a tipos de datos nativos de Python, podremos ingresar a cualquiera de sus valores como cualquier diccionario:

```
serializer.data['calle']

```


Para finalizar el proceso de serialización, procesamos los datos en json.

```
content = JSONRenderer().render(serializer.data)
content
```

Notar b' y las comillas dobles :

```
b'{"id":0,"calle":"AV. CABILDO","altura":"2040"}'
```
Vamos a crear una nueva sucursal:

```python
data2={'id': 6, 'calle': 'esmeralda', 'altura': '400'}
serial2=SucursalesSerializer(data=data2)
serial2.is_valid()
# ok!
serial2.validated_data
serial2.save()
# miremos la db...
```

Podemos ver que hay una nueva sucursal en la db!

Vamos a crear otro serializador, esta  vez de movimientos:

```python
class MovimientosSerializer(serializers.ModelSerializer):
     class Meta:
        model = Movimientos
        #indicamos que use todos los campos
        fields = "__all__"
        #les decimos cuales son los de solo lectura 
```


También podemos serializar conjuntos de consultas, para hacerlo simplemente agregamos un indicador `many=True` a los argumentos del serializador.
(Si modificamos el serializer.py hay que reiniciar la shell)

```python

# filter para devuelva muchos
# get devuelve uno solo

movimientos = Movimientos.objects.filter(cliente_id=35913755) 
# agregar many
serializer = MovimientosSerializer(movimientos,many=True) 
serializer.data
```

Esta consulta nos devuelve todos los movimientos del cliente con dni 35913755

Hacer esto desde la consola es solo una muestra de como podemos interactuar con la db desde estos objetos nuevos, pero la idea es que poder interactuar con requests HTTP como post, get. Empecemos con el POST, vamos a generar una vista que agregue movimientos a la db.

# Apiviews

El objetivo de una api es poder integrar nuestra db a la internet y el lenguaje de la internet es el protocolo HTTP, es por esto que tenemos que adaptar nuestras vistas de django para incorporar los serializadores que traducen filas de la db a json.


## GET

Vamos a generar una ruta de nuestro sitio para que comunicar el serializador, como vimos para django todas las conexiones son 'vistas', por eso vamos a agregar esto a `views.py`:


```
# importamos serializador y modelo

from .serializers import SucursalesSerializer 
from .models import Sucursales

from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status

# Create your views here.
class SucursalesLists(APIView):
    def get(self, request):
        sucursales = Sucursales.objects.all()
        serializer = SucursalesSerializer(sucursales,many=True)
        if sucursales:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
```

Ahora como es un requests GET podemos entrar desde el navegador:

http://127.0.0.1:8000/api/sucursales/

Vemos como respuesta todos las sucursales.

## POST
## DELETE
## PUT

# Permisos

# Hipervinculos

# Viewsets y Routers

