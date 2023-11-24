# models.py
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import render, redirect
from django.views import View


class Videojuego(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='videojuegos/', null=True, blank=True)
    cantidad_en_carrito = models.PositiveIntegerField(default=0)  # Nuevo campo

    def __str__(self):
        return self.titulo


class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    videojuegos = models.ManyToManyField(Videojuego)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"


class CrearUsuarioView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'tienda/crear_usuario.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                nuevo_usuario = form.save(commit=False)
                Carrito.objects.create(usuario=nuevo_usuario)
                messages.success(request, 'Usuario creado exitosamente')
                return redirect('login')
            except Exception as e:
                print(e)

        else:
            form = UserCreationForm()  
            context = {  
                'form':form  
            }  
            return render(request, 'tienda/crear_usuario.html', context)
