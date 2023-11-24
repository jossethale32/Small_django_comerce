from django import template

register = template.Library()

@register.filter(name='total_precio')
def total_precio(videojuegos):
    # Lógica para calcular el total del precio
    total = sum(videojuego.cantidad_en_carrito * videojuego.precio for videojuego in videojuegos)
    return total
