import math
import pygame
import sys

class Carrito:
    def __init__(self, x, y, ancho, largo):
        self.rect = pygame.Rect(x, y+20, ancho, largo)
        self.velocidad = 2
        self.vertices = []
        self.current_vertex_index = 0
        self.ancho=50
        self.largo=100

        # Cargar la imagen del carrito
        self.image = pygame.image.load("app/public/carrito.png")  # Cambia la ruta a tu imagen
        self.image = pygame.transform.scale(self.image, (self.ancho, self.largo))  # Escalar la imagen al tamaño del carrito

        # Invertir la imagen horizontalmente (True para horizontal, False para vertical)
        self.image = pygame.transform.flip(self.image, True, False)  # Invertir solo horizontalmente
        print('Hola')

    def establecer_vertices(self, vertices):
        self.vertices = vertices
        self.current_vertex_index = 0  # Reiniciar índice de vértices

    def mover(self):
        if not self.vertices:
            return
        
        target_x, target_y = self.vertices[self.current_vertex_index]

        # Mover hacia el siguiente vértice
        if self.rect.x < target_x:
            self.rect.x += self.velocidad
        elif self.rect.x > target_x:
            self.rect.x -= self.velocidad
        
        if self.rect.y < target_y:
            self.rect.y += self.velocidad
        elif self.rect.y > target_y:
            self.rect.y -= self.velocidad

        # Verificar si ha llegado al vértice
        if abs(self.rect.x - target_x) < self.velocidad and abs(self.rect.y - target_y) < self.velocidad:
            self.current_vertex_index = (self.current_vertex_index + 1) % len(self.vertices)

    def dibujar(self, screen):
        # Rotar la imagen según el ángulo theta
        rotated_image = pygame.transform.rotate(self.image, -math.degrees(0))
        
        # Obtener el rectángulo de la imagen rotada centrado en la nueva posición (x, y)
        rect = rotated_image.get_rect(center=(500 + 500 // 2, 500 + self.largo // 2))
        
        # Dibujar la imagen en la pantalla
        screen.blit(rotated_image, rect.topleft)




def generar_vertices_poligono(num_lados, centro, radio):
    """Genera los vértices de un polígono regular dado el número de lados, el centro y el radio."""
    vertices = []
    for i in range(num_lados):
        angulo = 2 * math.pi * i / num_lados  # Calcular el ángulo para cada vértice
        x = centro[0] + radio * math.cos(angulo)
        y = centro[1] + radio * math.sin(angulo)
        vertices.append((x, y))
    return vertices

# Configuración inicial
pygame.init()

# Dimensiones de la ventana
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Recorrido de Polígono")

# Crear el carrito
carrito = Carrito(100, 100, 20, 20)
carrito.dibujar(screen)

# Elegir un polígono (triángulo, cuadrado, pentágono)
tipo_poligono = "pentágono"  # Cambiar a "triángulo" o "pentágono" según sea necesario
centro = (400, 300)  # Centro del polígono
radio = 100  # Radio del polígono

# Generar los vértices del polígono
if tipo_poligono == "cuadrado":
    vertices = generar_vertices_poligono(4, centro, radio)
elif tipo_poligono == "triángulo":
    vertices = generar_vertices_poligono(3, centro, radio)
elif tipo_poligono == "pentágono":
    vertices = generar_vertices_poligono(5, centro, radio)

# Establecer los vértices en el carrito
carrito.establecer_vertices(vertices)

# Bucle principal
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mover el carrito
    carrito.mover()

    # Dibujar todo
    screen.fill((255, 255, 255))  # Limpiar la pantalla
    pygame.draw.polygon(screen, (0, 0, 0), vertices, 2)  # Dibujar el polígono
    pygame.draw.rect(screen, (255, 0, 0), carrito.rect)  # Dibujar el carrito

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(60)  # Limitar a 60 FPS

pygame.quit()
sys.exit()