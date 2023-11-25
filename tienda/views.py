from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Videojuego, Carrito
from .form import CustomUserCreationForm

def index(request):
    return render(request, 'tienda/index.html')
def lista_videojuegos(request):
    videojuegos = Videojuego.objects.all()

    for videojuego in videojuegos:
        videojuego.total = videojuego.cantidad_en_carrito * videojuego.precio

    return render(request, 'tienda/lista_videojuegos.html', {'videojuegos': videojuegos})


@login_required
def agregar_al_carrito(request, videojuego_id):
    videojuego = Videojuego.objects.get(id=videojuego_id)

    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    # Obtén la cantidad de la solicitud o establece el valor predeterminado a 1
    cantidad = int(request.GET.get('cantidad', 1))

    # Incrementa la cantidad en el carrito
    videojuego.cantidad_en_carrito += cantidad
    videojuego.save()

    # Agrega el videojuego al carrito
    carrito.videojuegos.add(videojuego)

    return redirect('lista_videojuegos')

@login_required
def ver_carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user).first()

    if request.method == 'POST':
        videojuego_id = request.POST.get('videojuego_id')
        if videojuego_id:
            videojuego_a_eliminar = get_object_or_404(Videojuego, pk=videojuego_id)
            carrito.videojuegos.remove(videojuego_a_eliminar)
            messages.success(request, 'Videojuego eliminado del carrito.')

    videojuegos_en_carrito = carrito.videojuegos.all() if carrito else []

    context = {
        'videojuegos_en_carrito': videojuegos_en_carrito,
    }

    return render(request, 'tienda/ver_carrito.html', context)

@login_required
def eliminar_del_carrito(request, videojuego_id):
    carrito = Carrito.objects.filter(usuario=request.user).first()
    videojuego_a_eliminar = get_object_or_404(Videojuego, id=videojuego_id)

    if carrito and videojuego_a_eliminar:
        # Establecer la cantidad en cero para el videojuego en el carrito
        videojuego_a_eliminar.cantidad_en_carrito = 0
        videojuego_a_eliminar.save()

        # Eliminar el videojuego del carrito
        carrito.videojuegos.remove(videojuego_a_eliminar)

        messages.success(request, 'Videojuego eliminado del carrito.')

    return redirect('ver_carrito')

def eliminar_carrito_pagado(request):
    carrito = Carrito.objects.filter(usuario=request.user).first()
    listavid= Videojuego.objects.all()

    for vid in listavid:
        videojuegoscar = get_object_or_404(Videojuego, id=vid.id)
        if carrito and videojuegoscar:
            videojuegoscar.cantidad_en_carrito = 0
            videojuegoscar.save()
            carrito.videojuegos.remove(videojuegoscar)

    text = request.POST['text']
    response = text + ":)"
    return HttpResponse(response)

    # videojuego_a_eliminar = get_object_or_404(Videojuego, id=videojuego_id)

    # if carrito and videojuego_a_eliminar:
        # Establecer la cantidad en cero para el videojuego en el carrito
        # videojuego_a_eliminar.cantidad_en_carrito = 0
        # videojuego_a_eliminar.save()

        # Eliminar el videojuego del carrito
        # carrito.videojuegos.remove(videojuego_a_eliminar)

        # messages.success(request, 'Videojuego eliminado del carrito.')

    # return redirect('ver_carrito')

def register(request):  
    if request.method == 'POST':  
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():  
            try:
                nuevo_usuario = form.save(commit=False)
                Carrito.objects.create(usuario=nuevo_usuario)
                messages.success(request, 'Usuario creado exitosamente')
                return redirect('login')
            except Exception as e:
                print(e)
    else:  
        form = CustomUserCreationForm()
    return render(request, 'tienda/crear_usuario.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('lista_videojuegos')
    else:
        form = AuthenticationForm()
    return render(request, 'tienda/login.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('lista_videojuegos')

def procesar_pago(request):
    if request.method == 'POST':
        numero_tarjeta = request.POST.get('numero_tarjeta')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        cvv = request.POST.get('cvv')

        if not numero_tarjeta or not fecha_vencimiento or not cvv:
            messages.error(request, 'Por favor, completa todos los campos del formulario de pago.')
            return redirect('procesar_pago')
        eliminar_carrito_pagado(request)
        messages.success(request, '¡Pago realizado con éxito!')
        
        return redirect('ver_carrito')
    else:
        return render(request, 'tienda/procesar_pago.html')
