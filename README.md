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
- [hipervinculos](https://github.com/carabedo/django-rest#hipervinculos)
- [viewsets & routers](https://github.com/carabedo/django-rest#viewsets)


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
<img src="https://github.com/carabedo/django-rest/raw/main/noauth.png" width=800px />

Para hacer un requests ahora, necesitamos hacerlo con un usuario del sitio registrado, probemos con la cuenta 'cliente' con la pwd `123`.

<img src="https://github.com/carabedo/django-rest/raw/main/auth.png" width=800px />

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

Esta clase hereda todo lo necesario de `permissions.BasePermission`, el metodo que necesitamos cambiar es `has_permission` el cual devuele true o false dependiendo nuestra necesidad. Vemos como accedemos a la db para confirmar que tipo de usuario esta haciendo el request.

Por ultimo en las vistas agreguemos esta clase `from .permissions import esEmpleado` y luego modifiquemos los permisos de las vistas para que queden asi:


```python
...
class MovimientosDetails(APIView):
    permission_classes = [permissions.IsAuthenticated,esEmpleado]
    def delete(self, request, movimiento_id): 
     ...

```

Probemos acceder a cualquier endpoint con nuestra cuenta de cliente y no tendremos exito. Ahora nuestros endpoints de movimientos solo son accesibles para los empleados.

Ahora vamos a generar un endpoint de prestamos que podra ser accedido por clientes y por empleados. Repasemos, primero generamos el serializador, luego vamos a generar las vistas y por ultimo agregaremos la nueva url.

Serializador:

```python
from .models import Prestamos

class PrestamosSerializer(serializers.ModelSerializer):
     class Meta:
        model = Prestamos
        fields = "__all__"
```

Vista:

```python
from .serializers import PrestamosSerializer 
from .models import Prestamos
class PrestamosListCliente(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, cliente_id): 
        #podemos chequear que un cliente solo haga GET para sus propios prestamos
        username = request.user
        owner=cliente_id
        try:
            user=ids.objects.filter(username=username).first()
            dni=user.cliente_id
        except:
            dni = -1
        if (dni == owner or user.tipo == 'empleado' ):

            prestamos = Prestamos.objects.filter(cliente_id=cliente_id)
            serializer = PrestamosSerializer(prestamos,many=True)
            if prestamos:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response('no hay prestamos asociados a este cliente',status=status.HTTP_404_NOT_FOUND)
        else:
            return Response('no coincide el dni ni es empleado',status=status.HTTP_404_NOT_FOUND)
```      

URL:

```python
path('api/prestamos/<int:cliente_id>/', main_views.PrestamosListCliente.as_view(),name='api_prestamos_list' )
```

Probemos que podemos acceder http://127.0.0.1:8000/api/prestamos/35913755/ desde la cuenta del mismo dni o desde una cuenta de empleado.

Por ultimo vamos a crear un endpoint que liste los prestamos por sucursal:

```python
from .permissions import esEmpleado
class PrestamosListSucursal(APIView):
    permission_classes = [permissions.IsAuthenticated,esEmpleado]

    def get(self, request, sucursal_id): 
        clientes= Clientes.objects.filter(sucursal=sucursal_id)
        prestamos=[]
        for cliente in clientes:
            if Prestamos.objects.filter(cliente_id=cliente.cliente_id).exists():
                prestamos.extend(list(Prestamos.objects.filter(cliente_id=cliente.cliente_id)))
            else:
                pass
        if prestamos:
            serializer = PrestamosSerializer(prestamos,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('No hay prestamos asociados a la sucursal', status=status.HTTP_404_NOT_FOUND)
```

Solo resta agregar la url:

```python
path('api/prestamos_sucursal/<int:sucursal_id>/', main_views.PrestamosListSucursal.as_view(),name='api_prestamos_sucursal') 
```
Probemos esta url `http://127.0.0.1:8000/api/prestamos_sucursal/1/` con una cuenta de empleado.

Como agregarias una vista para que un cliente pueda cancelar un prestamo? 

# Hipervinculos

Vamos a generar una API navegable, primero vamo a definir la vista del 'home' de la api:

```python
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse as reverse2

@login_required
@api_view(['GET'])
def api_root(request, format=None):
    username=request.user.username
    if ids.objects.filter(username=username).first().tipo == 'empleado':
        return Response({
                'sucursales': reverse2('api_sucursales', request=request, format=format),
                'movimientos': reverse2('api_movimientos', request=request, format=format),
                'prestamos': reverse2('api_prestamos_sucursal', request=request, format=format),
            })
    else:
        return Response({
            'sucursales': reverse2('api_sucursales', request=request, format=format)
        })

```

Esto define la lista de endpoints de nuestra api con sus respectivos links.

# Viewsets

Los viewsets en django son una abstraccion mas de las vistas, primero vimos las funciones vista, luego las clases y ahora los viewsets. Su proposito es evitarnos escribir codigo. Por ejemplo, imagenemos que ahora queremos hacer un endpoint para la tabla 'empleados', que harias? Generas el serializador, vas a las vistas  escribis dos clases una lista y otra details, despues vas a la urls y agregas las dos urls no? Buen con las viewsets y los routers, todo es mas facil:

Empecemos con el modelo:

```python
from .models import Empleados

class EmpleadosSerializer(serializers.ModelSerializer):
     class Meta:
        model = Empleados
        fields = "__all__"
```

Ahora vamos a las vistas a escribir la clase detalles y otra de listas.... no, usemos un viewset:

```python
from rest_framework import viewsets
from .models import Empleados
from .serializers import EmpleadosSerializer

class EmpleadosViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` (get al details) actions.
    """
    queryset = Empleados.objects.all()
    serializer_class = EmpleadosSerializer
```



Faltan la urls no?

# Routers

Un router es una clase que contiene ya todo el codigo necesario para las clases list y details que ya vienen en el viewset. 

```python
from rest_framework.routers import DefaultRouter
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'empleados', main_views.EmpleadosViewSet,basename="empleados")
```

Y ahora agregamos esto en nuestra lista de urls:

```python
path('api/', include(router.urls))
```

Listo!

Mira aca:

http://127.0.0.1:8000/api/empleados/

Y ahora mira aca:

http://127.0.0.1:8000/api/empleados/10/

Con mucho menos codigo generamos dos endpoints para la tabla empleados! Podrias reescribir las vistas para otras tablas para practicar.

