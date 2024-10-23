import math
import pygame
import sys

class Carrito:
    def __init__(self, x, y, ancho, largo):
        self.rect = pygame.Rect(x, y, ancho, largo)
        self.vL = 2  # Velocidad del motor izquierdo
        self.vR = 2  # Velocidad del motor derecho
        self.theta = 0  # Ángulo de orientación del carrito
        self.vertices = []
        self.current_vertex_index = 0
        self.frenando = False  # Estado de frenado

    def establecer_vertices(self, vertices):
        """Establece los vértices del polígono."""
        self.vertices = vertices
        self.current_vertex_index = 0

    def mover(self):
        """Mueve el carrito a lo largo de la línea entre los vértices."""
        if not self.vertices or self.frenando:
            return  # No se mueve si no hay vértices o está frenado

        # Obtener el vértice objetivo actual
        target_x, target_y = self.vertices[self.current_vertex_index]

        # Calcular la distancia hacia el siguiente vértice
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        distancia = math.hypot(dx, dy)

        # Si está cerca del vértice, avanzar al siguiente
        if distancia < 2:
            self.current_vertex_index = (self.current_vertex_index + 1) % len(self.vertices)
            target_x, target_y = self.vertices[self.current_vertex_index]
            dx = target_x - self.rect.x
            dy = target_y - self.rect.y
            distancia = math.hypot(dx, dy)

        # Calcular el ángulo hacia el siguiente vértice
        self.theta = math.atan2(dy, dx)

        # Actualizar la posición a lo largo de la línea
        v = (self.vL + self.vR) / 2  # Velocidad promedio
        self.rect.x += v * math.cos(self.theta)
        self.rect.y += v * math.sin(self.theta)

    def dibujar(self, screen):
        """Dibuja el carrito como un cuadrado azul."""
        pygame.draw.rect(screen, (0, 0, 255), self.rect)  # Cuadrado azul

    def manejar_frenado(self, pos):
        """Inicia o detiene el frenado si se hace clic en el carrito."""
        if self.rect.collidepoint(pos):
            self.frenando = not self.frenando  # Alternar estado de frenado

def generar_vertices_poligono(num_lados, centro, radio):
    """Genera los vértices de un polígono regular."""
    vertices = []
    for i in range(num_lados):
        angulo = 2 * math.pi * i / num_lados
        x = centro[0] + radio * math.cos(angulo)
        y = centro[1] + radio * math.sin(angulo)
        vertices.append((x, y))
    return vertices

def mostrar_velocidades(screen, carrito):
    """Muestra las velocidades de los motores en pantalla."""
    font = pygame.font.SysFont(None, 36)
    texto = f"vL: {carrito.vL:.2f} | vR: {carrito.vR:.2f}"
    text_surface = font.render(texto, True, (0, 0, 0))
    screen.blit(text_surface, (10, 10))

def cambiar_poligono():
    """Cambia entre triángulo, cuadrado y pentágono."""
    global tipo_poligono
    if tipo_poligono == "triángulo":
        tipo_poligono = "cuadrado"
    elif tipo_poligono == "cuadrado":
        tipo_poligono = "pentágono"
    else:
        tipo_poligono = "triángulo"
    actualizar_vertices()

def actualizar_vertices():
    """Actualiza los vértices según el polígono seleccionado."""
    if tipo_poligono == "cuadrado":
        vertices = generar_vertices_poligono(4, centro, radio)
    elif tipo_poligono == "triángulo":
        vertices = generar_vertices_poligono(3, centro, radio)
    elif tipo_poligono == "pentágono":
        vertices = generar_vertices_poligono(5, centro, radio)
    carrito.establecer_vertices(vertices)

# Configuración de Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Recorrido Suave del Polígono")

# Crear el carrito
carrito = Carrito(100, 100, 20, 20)  # Cuadrado azul

# Variables del polígono
tipo_poligono = "triángulo"  # Polígono inicial
centro = (400, 300)
radio = 150
actualizar_vertices()

# Botón para cambiar de polígono
boton_rect = pygame.Rect(10, 50, 200, 40)

# Bucle principal
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if boton_rect.collidepoint(event.pos):
                cambiar_poligono()  # Cambiar polígono al hacer clic
            else:
                carrito.manejar_frenado(event.pos)  # Frenar o reanudar al hacer clic

    # Mover el carrito
    carrito.mover()

    # Dibujar en la pantalla
    screen.fill((255, 255, 255))  # Fondo blanco
    pygame.draw.polygon(screen, (0, 0, 0), carrito.vertices, 2)  # Dibujar polígono
    carrito.dibujar(screen)  # Dibujar carrito
    mostrar_velocidades(screen, carrito)  # Mostrar velocidades

    # Dibujar botón de cambio de polígono
    pygame.draw.rect(screen, (100, 200, 100), boton_rect)
    font = pygame.font.SysFont(None, 36)
    text_surface = font.render("Cambiar Polígono", True, (0, 0, 0))
    screen.blit(text_surface, (boton_rect.x + 10, boton_rect.y + 5))

    pygame.display.flip()
    clock.tick(60)  # Limitar a 60 FPS

pygame.quit()
sys.exit()
