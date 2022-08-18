# django-restframework

## indice:

- [instalacion](https://github.com/carabedo/django-restframework#instalacion)
- [serializadores](https://github.com/carabedo/django-restframework#serialización)
- [apiviews](https://github.com/carabedo/django-restframework#apiviews)
- [requests GET PUT DELETE]()
- [permisos](https://github.com/carabedo/django-restframework#permisos)
- [hipervinculos]()
- [viewsets y routers]()

## instalacion:

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

## serialización

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
