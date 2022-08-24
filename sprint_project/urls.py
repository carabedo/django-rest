
from django.contrib import admin
from main import views as main_views
from django.conf  import settings
from django.urls import path,include


urlpatterns = [
    #Creamos un patrón url, en la raíz del sitio (cadena vacía) desde el que llamaremos a la vista views.home que tiene el nombre home.
    path('',main_views.home, name="home"), 
    path('prestamos/',main_views.prestamos, name="prestamos"), 
    path('cuentas/',main_views.cuentas, name="cuentas"), 
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/registro',main_views.registro, name="registro"),
    path('api/sucursales/', main_views.SucursalesLists.as_view(),name='api_sucursales'),
    path('api/movimientos/', main_views.MovimientosLists.as_view(),name='api_movimientos'),
    path('api/movimientos/<int:movimiento_id>/',main_views.MovimientosDetails.as_view()),
    path('api/prestamos/<int:cliente_id>/', main_views.PrestamosListCliente.as_view(),name='api_prestamos_list' ),
    path('api/prestamos_sucursal/<int:sucursal_id>/', main_views.PrestamosListSucursal.as_view(),name='api_prestamos_sucursal'),
    path('api/', main_views.api_root,name='api_root'),

    ]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

