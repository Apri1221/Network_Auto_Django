from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

urlpatterns = [
    path('admin/', admin.site.urls),
    # artinya kita akan include file urls.py yg berada di folder app1
    # path di url pusat akan mengikuti url apa saja yg ada di url app1
    # maksudnya '' -> menandakan 127.0.0.1:8000 di ikuti route url yg ada di url app1
    # misal di app1 tanda '' berisi 'hello_world', maka harus diakses dengan 127.0.0.1:8000/hello_world
    # path('hai', include('app1.urls')) ini dapat diakses dgn 127.0.0.1:8000/haihello_world
    
    path('net_auto/', include('net_auto.urls'))
]
