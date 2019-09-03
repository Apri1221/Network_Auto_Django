from django.urls import path
from . import views
# import semua yg ada di views

urlpatterns = [
    # views -> manggil method yang ada di file views.py
    path('beranda/', views.beranda, name='beranda'),
    
    # gunanya name='' adalah untuk digunakan pada href link navbar, dengan cara url='namanya'
    path('perangkat/', views.perangkat, name='perangkat'),

    path('konfigurasi/', views.konfigurasi, name='konfigurasi'),

    path('cek_konfigurasi/', views.cek_konfigurasi, name='cek_konfigurasi'),

    path('riwayat/', views.riwayat, name='riwayat')
]
