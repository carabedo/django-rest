#Sprint 7 - Primera aplicacion

#Vamos a importar un método del módulo django.http llamado HttpResponse

from django.shortcuts import render, HttpResponse
from .forms import PrestamoForm
from .forms import RegistroForm

from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

##para crear usuarios
from .forms import RegistroForm
from django.contrib.auth.models import User

# para leer la db
from .models import Movimientos
from .models import Clientes
from .models import Prestamos
from .models import Empleados
from .models import ids

# fecha del prestamo
from datetime import date

def home(request):
    if request.user.username:
        #cliente= Clientes.objects.get(cliente_id=int(request.user.username))
        cliente=request.user.username

        return render(request,"main/home.html", {'cliente' : cliente})
    else:    
        return render(request,"main/home.html")


@login_required
def cuentas(request):

    row_cliente_id= ids.objects.filter(username=request.user.username)[0]
    
    movimientos= Movimientos.objects.filter(cliente_id=row_cliente_id.cliente_id).order_by('-id')

    return render(request,"main/cuentas.html", {'movimientos': movimientos})




#Agregamos la vista de contacto que teniamos en la aplicacion de prueba
@login_required
def prestamos(request):
    #creamos una isntancia del formulario
    prestamo_form = PrestamoForm
    #validamos que ocurrio una peticiPreson POST
    if request.method == "POST":
        #Traemos los datos enviados
        prestamo_form = prestamo_form(data=request.POST)
        #Chequeamos que los datos son validos, de ser asi, los asignamos a una variable
        if prestamo_form.is_valid():
            monto = request.POST.get('monto','')
            tipo = request.POST.get('tipo','')

            try:
                row_cliente_id= ids.objects.filter(username=request.user.username)[0]
                cliente_id =row_cliente_id.cliente_id
                #Generamos el prestamo
                #hay que poner un if consultando si ya se excedio el limite
                #manando un denied q mostrara un mensaje en el template
                prestamo = Prestamos(cliente_id=cliente_id,monto=monto, tipo=tipo, fecha_inicio=date.today())
                movimiento = Movimientos(cliente_id=cliente_id,importe=monto,fecha=date.today())
                movimiento.save()
                prestamo.save()
                return redirect(reverse('prestamos')+"?ok")
            except:
                return redirect(reverse('home'))
        #En lugar de renderizar el template de prestamoo hacemos un redireccionamiento enviando una variable OK
        
    return render(request,"main/prestamos.html",{'form': prestamo_form})


def registro(request):
    registro_form = RegistroForm

    if request.method == "POST":
        #Traemos los datos enviados
        registro_form = registro_form(data=request.POST)
        #Chequeamos que los datos son validos, de ser asi, los asignamos a una variable
        #if registro_form.is_valid():
        cliente_id= request.POST.get('cliente_id','')
        usuario= request.POST.get('username','')
        email = request.POST.get('email','')
        pwd = request.POST.get('pwd','')
        print(cliente_id,email,pwd)
        #user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        try:
            persona= Clientes.objects.filter(cliente_id=cliente_id)[0]
            tipo='cliente'
        except:
            persona= Empleados.objects.filter(cliente_id=cliente_id)[0]
            tipo='empleado'

        dni = ids(cliente_id=cliente_id,username=usuario,tipo=tipo)
        dni.save()
        user = User.objects.create_user(usuario, email, pwd)
        user.save()
        print('creado')
        #En lugar de renderizar el template de prestamoo hacemos un redireccionamiento enviando una variable OK
        return redirect(reverse('login'))
    return render(request,"main/registro.html",{'form': registro_form})

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

from .models import Movimientos
from .serializers import MovimientosSerializer 
from rest_framework import permissions

from .permissions import esEmpleado
class MovimientosLists(APIView):
    permission_classes = [permissions.IsAuthenticated,esEmpleado]
    def post(self, request):
        data=request.data
        data['fecha']=date.today().strftime('%Y-%m-%d')
        serializer = MovimientosSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovimientosDetails(APIView):
    permission_classes = [permissions.IsAuthenticated,esEmpleado]
    def delete(self, request, movimiento_id): 
        movimiento = Movimientos.objects.filter(pk=movimiento_id).first()
        if movimiento:
            serializer = MovimientosSerializer(movimiento)
            movimiento.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND) 

    def put(self, request, movimiento_id):
        movimiento = Movimientos.objects.filter(pk=movimiento_id).first()
        serializer = MovimientosSerializer(movimiento, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)               



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

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse as reverse2


@login_required
@api_view(['GET'])
def api_root(request, format=None):
    username=request.user.username
    if ids.objects.filter(username=username).first().tipo == 'empleado':
        return Response({
                'sucursales': reverse2('api_sucursales', request=request, format=format),
                'movimientos': reverse2('api_movimientos', request=request, format=format)
            })
    else:
        return Response({
            'sucursales': reverse2('api_sucursales', request=request, format=format)
        })