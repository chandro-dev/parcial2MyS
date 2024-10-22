import pygame
import math

# Inicialización de pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Parámetros del móvil
x, y = 400, 300  # Posición inicial
angle = 0  # Ángulo inicial
speed_left, speed_right = 0, 0  # Velocidades iniciales de los motores
path = []  # Para almacenar el área recorrida

# Función para dibujar el móvil
def draw_robot(x, y):
    pygame.draw.circle(screen, BLACK, (int(x), int(y)), 10)

# Función para actualizar el movimiento
def update_position(speed_left, speed_right, x, y, angle):
    angular_speed = (speed_right - speed_left) / 50
    angle += angular_speed
    avg_speed = (speed_left + speed_right) / 2
    x += avg_speed * math.cos(angle)
    y += avg_speed * math.sin(angle)
    return x, y, angle

# Función para recorrer un polígono regular
def recorrer_poligono(vertices, x, y):
    current_vertex = 0
    while True:
        x_dest, y_dest = vertices[current_vertex]
        direction_x = x_dest - x
        direction_y = y_dest - y
        distance = math.hypot(direction_x, direction_y)

        if distance > 1:
            x += direction_x / distance
            y += direction_y / distance
        else:
            current_vertex = (current_vertex + 1) % len(vertices)

        yield x, y

# Algoritmo básico de búsqueda de materiales (variables del sistema)
material_positions = [(100, 100), (700, 500)]
material_collected = []

def buscar_material(x, y):
    for pos in material_positions:
        if math.hypot(x - pos[0], y - pos[1]) < 20:
            material_collected.append(pos)
            material_positions.remove(pos)

# Obstáculos en el área de trabajo
obstacles = [(200, 300), (500, 400), (400, 500)]

# Función para dibujar los obstáculos
def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(screen, BLUE, (*obs, 30, 30))

# Bucle principal de simulación
running = True
while running:
    screen.fill(WHITE)
    path.append((x, y))  # Guardar el recorrido

    # Eventos de teclado para controlar las velocidades
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                speed_left, speed_right = 2, 2  # Avanzar recto
            elif event.key == pygame.K_DOWN:
                speed_left, speed_right = -2, -2  # Retroceder
            elif event.key == pygame.K_LEFT:
                speed_left, speed_right = 2, 1  # Girar izquierda
            elif event.key == pygame.K_RIGHT:
                speed_left, speed_right = 1, 2  # Girar derecha

    # Actualizar posición y buscar materiales
    x, y, angle = update_position(speed_left, speed_right, x, y, angle)
    buscar_material(x, y)

    # Dibujar el móvil y el recorrido
    draw_robot(x, y)
    draw_obstacles(obstacles)
    for point in path:
        pygame.draw.circle(screen, (200, 200, 200), point, 1)

    # Mostrar el área recorrida
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
