
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
    path('accounts/registro',main_views.registro, name="registro") ]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)