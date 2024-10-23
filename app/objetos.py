import pygame
import math
import random

# Inicialización de Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador con Cambio de Trayectoria Dinámico")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BUTTON_COLOR = (100, 200, 100)

# Parámetros generales
d = 50  # Distancia entre los dos motores
friction = 0.95  # Coeficiente de fricción
object_weight = 0.7  # Peso del objeto
base_speed = 100  # Velocidad base del móvil
collision_radius = 50  # Radio efectivo para evitar colisiones

# Objetos y punto de entrega
objects = [(WIDTH // 2, HEIGHT // 4), (3 * WIDTH // 4, HEIGHT // 4)]
drop_position = (WIDTH // 2, 3 * HEIGHT // 4)  # Punto de entrega

class Movil:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.theta = 0  
        self.vL, self.vR = 0, 0  
        self.target = random.choice(objects)  
        self.carrying_object = False  
        self.paused = False  
        self.path = []  

    def calcular_velocidades(self, moviles):
        """Ajusta las velocidades y busca evitar colisiones."""
        if self.paused:
            self.vL *= friction
            self.vR *= friction
            return

        # Buscar otro camino si está cerca de otro móvil
        for otro_movil in moviles:
            if otro_movil is not self and self.detectar_colision(otro_movil):
                self.ajustar_direccion()
                break

        target_x, target_y = self.target
        angle_to_target = math.atan2(target_y - self.y, target_x - self.x)
        angle_diff = angle_to_target - self.theta
        angle_diff = (angle_diff + math.pi) % (2 * math.pi) - math.pi  

        speed = base_speed * (1 - object_weight) if self.carrying_object else base_speed

        if abs(angle_diff) > 0.1:  
            self.vL = speed * (1 - angle_diff / math.pi)
            self.vR = speed * (1 + angle_diff / math.pi)
        else:  
            self.vL = self.vR = speed

    def ajustar_direccion(self):
        """Cambia ligeramente la dirección del móvil para evitar colisiones."""
        giro = random.uniform(-0.5, 0.5)  
        self.theta += giro  

    def actualizar_posicion(self, dt):
        if self.paused and abs(self.vL) < 0.01 and abs(self.vR) < 0.01:
            self.vL = self.vR = 0
            return

        V = (self.vL + self.vR) / 2  
        omega = (self.vR - self.vL) / d  

        self.theta += omega * dt
        self.x += V * math.cos(self.theta) * dt
        self.y += V * math.sin(self.theta) * dt

        self.path.append((self.x, self.y))

    def detectar_colision(self, otro_movil):
        """Detecta si se está acercando a otro móvil."""
        return math.hypot(self.x - otro_movil.x, self.y - otro_movil.y) < collision_radius

    def objetivo_alcanzado(self):
        return math.hypot(self.target[0] - self.x, self.target[1] - self.y) < collision_radius

    def manejar_objetivo(self):
        if self.objetivo_alcanzado():
            if self.target in objects and not self.carrying_object:
                self.carrying_object = True
                self.target = drop_position
            elif self.target == drop_position and self.carrying_object:
                self.carrying_object = False
                self.target = random.choice(objects)

    def manejar_pausa(self, pos):
        if math.hypot(self.x - pos[0], self.y - pos[1]) < 15:
            self.paused = not self.paused

moviles = []

def agregar_movil():
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    moviles.append(Movil(x, y))

boton_rect = pygame.Rect(WIDTH - 160, 10, 150, 40)

running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if boton_rect.collidepoint(event.pos):
                agregar_movil()
            else:
                for movil in moviles:
                    movil.manejar_pausa(event.pos)

    pygame.draw.rect(screen, BUTTON_COLOR, boton_rect)
    font = pygame.font.SysFont(None, 24)
    text = font.render("Agregar Móvil", True, BLACK)
    screen.blit(text, (boton_rect.x + 10, boton_rect.y + 10))

    dt = clock.get_time() / 1000
    for i, movil in enumerate(moviles):
        movil.calcular_velocidades(moviles)
        movil.actualizar_posicion(dt)
        movil.manejar_objetivo()

        for point in movil.path:
            pygame.draw.circle(screen, BLUE, (int(point[0]), int(point[1])), 2)

        pygame.draw.circle(screen, RED, (int(movil.x), int(movil.y)), 15)

        if movil.carrying_object:
            pygame.draw.rect(screen, GREEN, (int(movil.x) - 10, int(movil.y) - 30, 20, 20))

        info = f"Móvil {i + 1} - vL: {movil.vL:.2f}, vR: {movil.vR:.2f}"
        text = font.render(info, True, BLACK)
        screen.blit(text, (10, 50 + i * 20))

    for obj in objects:
        pygame.draw.rect(screen, GREEN, (*obj, 20, 20))

    pygame.draw.circle(screen, BLACK, drop_position, 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
