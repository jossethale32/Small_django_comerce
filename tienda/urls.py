# tienda/urls.py
from django.urls import path
from . import views
from .models import CrearUsuarioView
from .views import lista_videojuegos, agregar_al_carrito, ver_carrito, login, logout, procesar_pago, eliminar_del_carrito, register

urlpatterns = [
    path('index/', views.index, name='index'),
    path('lista_videojuegos/', lista_videojuegos, name='lista_videojuegos'),
    path('agregar_al_carrito/<int:videojuego_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('ver_carrito/', ver_carrito, name='ver_carrito'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('procesar_pago/', procesar_pago, name='procesar_pago'),
    path('eliminar_del_carrito/<int:videojuego_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    # path('crear_usuario/', CrearUsuarioView.as_view(), name='crear_usuario'),
    path('crear_usuario/', register, name='crear_usuario'),


]
