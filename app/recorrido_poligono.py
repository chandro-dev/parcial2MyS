import pygame
import math

# Definir los polígonos
def generar_vertices_poligono(n, radio, centro):
    """Genera los vértices de un polígono regular en 2D."""
    vertices = []
    for i in range(n):
        angulo = 2 * math.pi * i / n  # Calcular el ángulo para cada vértice
        x = centro[0] + radio * math.cos(angulo)
        y = centro[1] + radio * math.sin(angulo)
        vertices.append((x, y))
    return vertices

# Mover el carrito entre los vértices
def mover_carrito_poligono(carrito, vertices, velocidad, dt):
    """Mueve el carrito a lo largo de los vértices del polígono."""
    for i in range(len(vertices)):
        # Calcular la dirección del próximo vértice
        dx = vertices[i][0] - carrito.x
        dy = vertices[i][1] - carrito.y
        distancia = math.sqrt(dx ** 2 + dy ** 2)

        # Mover el carrito hacia el siguiente vértice
        if distancia > 1:
            carrito.x += velocidad * (dx / distancia) * dt
            carrito.y += velocidad * (dy / distancia) * dt

        # Si está cerca del vértice, girar hacia el próximo
        if distancia < 5:  # Umbral de cercanía
            if i < len(vertices) - 1:
                siguiente_vertice = vertices[i + 1]
            else:
                siguiente_vertice = vertices[0]  # Volver al primer vértice
            angulo_nuevo = math.atan2(siguiente_vertice[1] - carrito.y, siguiente_vertice[0] - carrito.x)
            carrito.omega = angulo_nuevo

# Función principal
def recorrer_poligono(screen, carrito, vertices, velocidad, dt):
    """Simula el movimiento del carrito por un polígono."""
    # Dibujar el polígono
    pygame.draw.polygon(screen, (0, 0, 255), vertices, 1)
    
    # Mover el carrito a lo largo de los vértices
    mover_carrito_poligono(carrito, vertices, velocidad, dt)