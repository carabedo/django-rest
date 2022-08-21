# restframework

## indice:

- [instalacion](https://github.com/carabedo/django-restk#instalacion)
- [serializadores](https://github.com/carabedo/django-rest#serialización)
- [apiviews](https://github.com/carabedo/django-rest#apiviews)
- [requests methods]()
    - [GET](https://github.com/carabedo/django-rest#get)
    - [POST](https://github.com/carabedo/django-rest#post)
    - [DELETE](https://github.com/carabedo/django-rest#delete)
    - [PUT](https://github.com/carabedo/django-rest#put)
- [permisos](https://github.com/carabedo/django-rest#permisos)
- [hipervinculos]()


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

from .models import Movimientos

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

Hacer esto desde la consola es solo una muestra de como podemos interactuar con la db desde estos objetos nuevos, pero la idea es que poder interactuar con requests HTTP como post, get. 

Empecemos con el GET, vamos a generar una vista que ante un request GET devuelva un json con la informacion de la tabla sucursales.

# Apiviews

El objetivo de una api es poder integrar nuestra db a la internet y el lenguaje de la internet es el protocolo HTTP, es por esto que tenemos que adaptar nuestras vistas de django para incorporar los serializadores que traducen filas de la db a json.


## GET

Vamos a generar una ruta de nuestro sitio para que comunicar el serializador, como vimos para django todas las conexiones son 'vistas', por eso vamos a agregar esto a `views.py`:


```python
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

Esta vista es una clase, no una funcion como veniamos laburando, la ventaja es que dentro de esta clase podemos crear funciones que automaticamente responde al tipo de metodo del requests. En este ejemplo era un GET.

Como toda vista tenemos que agregarla en `urls.py`.

Ahora como es un requests GET podemos entrar desde el navegador:

```python
    path('api/sucursales/', main_views.SucursalesLists.as_view(),name='api_sucursales' )
```


http://127.0.0.1:8000/api/sucursales/

Vemos como respuesta todas las sucursales en un template que jamas escribimos! Tambien podemos probar con postman, con requests de python o con fetch desde el chrome.


## POST

Ahora queremos generar un nuevo movimiento en la db, necesitamos generar otra vista usando el modelo y el serializador para los movimientos.

```python
from .models import Movimientos
from .serializers import MovimientosSerializer 


class MovimientosLists(APIView):
    def post(self, request):
        data=request.data
        data['fecha']=date.today().strftime('%Y-%m-%d')
        serializer = MovimientosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Y tambien tenemos que agregar la url para este endpoint:

```python
...
path('api/movimientos/', main_views.MovimientosLists.as_view(),name='api_movimientos' )
...
```

Ahora no podemos acceder desde el navegador, por que solo hace requests GET, necesitamos otra cosa, postman, requests o fetch.

La url es: 

`http://127.0.0.1:8000/api/movimientos/`

El metodo es `POST` y el body:

```json
{"cliente_id":35913755,"importe":-5}

```
Vemos que el movimiento impacta en la db, tambien podemos loguearnos con el usuario `cliente` y ver como si refrescamos la pagina podemos observar el nuevo movimiento.


## DELETE


Ahora agreguemos un endpoint para borrar un movimiento. Para eso vamos a definir un nuevo método: `DELETE` en otra clase, vamos a generar la clase `MovimientosDetails`. Esto es por que las urls para pedido seran diferentes, vamos a usar el `id` del movimiento para eliminarlo.

```python
class MovimientosDetails(APIView):
     def delete(self, request, movimiento_id): 
        movimiento = Movimientos.objects.filter(pk=movimiento_id).first()
        if movimiento:
            serializer = MovimientosSerializer(movimiento)
            movimiento.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND) 
```

Generamos un metodo para la clase que responde al metodo HTTP del mismo nombre, hicimos una query de la db y borramos. Notar que podriamos borrar sin necesida de serializar, pero la respuesta del borrado es la data, por eso necesitamos serializar.

Fijate que los parametros del metodo incluyen el id del movimiento `movimiento_id` ese valor se lo vamos a pasar en la url:

```python
    path('api/movimientos/<int:movimiento_id>/',main_views.MovimientosDetails.as_view())
```

Ahora tenemos que hacer un request DELETE a: `http://127.0.0.1:8000/api/movimientos/150009/` si actualizamos la pagina vemos como el movimiento se borro.

## PUT

Agreguemos un endpoint para modificar un movimiento. Para eso vamos a definir un nuevo método (`PUT`)  en la clase `MovimientosDetails`.


```python
    def put(self, request, movimiento_id):
        movimiento = Movimientos.objects.filter(pk=movimiento_id).first()
        serializer = MovimientosSerializer(movimiento, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)               
```

Ahora probemos modificar el movimiento `150001`, la url es `http://127.0.0.1:8000/api/movimientos/150001/`, el metodo `PUT` y el body:

```json
{ "importe": -15  }
```


# Permisos

Asi como tenemos armada la API, cualquier persona puede acceder a modificar informacion de los movimientos de nuestros clientes. Tenemos que agregar una capa de seguridad. Para hacer esto necesitamos agregar un atributo en las clases `MovimientosDetails` y  `MovimientosList` que definen las vista de la api.


Agreguemos:

```python
...
class MovimientosDetails(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, movimiento_id): 
...
```


No olvidar importar esto al principio del archivo:

```python
from rest_framework import permissions
```

Esto obliga a que cualquier requests GET/POST/PUT/DELETE sea hecho por un usuario registrado. Podemos probar un simple GET y vemos como nos pide credenciales.

```json
{
    "detail": "Authentication credentials were not provided."
}
```

Para hacer un requests ahora, necesitamos hacerlo con un usuario del sitio registrado, probemos con la cuenta `cliente` con la pwd `123`.

Ahora nos gustaria poder discriminar para el mismo endpoint si el request proviene de un cliente o de un empleado, por que como esta nuestra api cualquier usuario del homebanking puede modificar la db.


Para esto vamos a generar un nuevo tipo de permiso, similar al `permissions.IsAuthenticated`, primero creemos un archivo `permissions.py` en nuestra app y copiemos esto:

```python
from rest_framework import permissions
from .models import ids

class esEmpleado(permissions.BasePermission):
    def has_permission(self, request, view):
        username = request.user
        if ids.objects.filter(username=username).first().tipo == 'empleado':
            return True
        else:
            return False
```

Por ultimo en las vistas agreguemos esta clase `from .permissions import esEmpleado` y luego modifiquemos los permisos de las vistas para que queden asi:


```python
...
class MovimientosDetails(APIView):
    permission_classes = [permissions.IsAuthenticated,esEmpleado]
    def delete(self, request, movimiento_id): 
     ...

```


# Hipervinculos

Vamos a generar una API navegable, primero vamo a definir la vista del 'home' de la api:

```python
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse as reverse2

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'sucursales': reverse2('api_sucursales', request=request, format=format),
        'movimientos': reverse2('api_movimientos', request=request, format=format)
    })
```

Esto define la lista de endpoints de nuestra api con sus respectivos links.

