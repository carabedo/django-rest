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
from .models import Participantes

 
class ParticipantesSerializer(serializers.ModelSerializer):
     class Meta:
        model = Participantes
        #indicamos que use todos los campos
        fields = "__all__"
        #les decimos cuales son los de solo lectura 

```
Esta clase, automaticamente genera una serializacion de las filas, al heradar la clase `serializers.ModelSerializer` hacemos todo el trabajo.



Probemos que esto funciona:

Ejecutemos el siguiente codigo en la consola de django `python3 manage.py shell`

```python
from app_prueba.models import Participantes
from app_prueba.serializers import ParticipantesSerializer
from rest_framework.renderers import JSONRenderer 
from rest_framework.parsers import JSONParser

participante = Participantes.objects.get(id=1) 

serializer = ParticipantesSerializer(participante) 
serializer.data

```
Deberiamos ver en consola:

```
{'id': 1, 'name': 'Tammie', 'last_name': 'Pineda', 'mail': 'pineda@itbank.com', 'team': 'front', 'proyect_id': 5, 'url_im': 'https://randomuser.me/api/portraits/women/1.jpg'}
```

En este punto, hemos traducido la instancia del modelo a tipos de datos nativos de Python, podremos ingresar a cualquiera de sus valores como cualquier diccionario:

```
serializer.data['mail']

```


Para finalizar el proceso de serialización, procesamos los datos en json.

```
content = JSONRenderer().render(serializer.data)
content
```

Notar b' y las comillas dobles :

```
b'{"id":1,"name":"Tammie","last_name":"Pineda","mail":"pineda@itbank.com","team":"front","proyect_id":5,"url_im":"https://randomuser.me/api/portraits/women/1.jpg"}'
```
