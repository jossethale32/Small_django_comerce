# En admin.py de la aplicación tienda
from django.contrib import admin
from .models import Videojuego

admin.site.register(Videojuego)
