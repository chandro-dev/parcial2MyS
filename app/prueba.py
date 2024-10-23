import pygame
import random

# Configuraciones de la ventana
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Clase Carrito
class Carrito:
    def __init__(self):
        self.x = 0  # Posición inicial en x
        self.y = 0  # Posición inicial en y
        self.width = 20
        self.height = 10
        self.step_size = 5  # Tamaño del paso
        self.path = []  # Almacena el recorrido
        self.current_direction = 1  # 1: derecha, -1: izquierda

    def mover(self, obstaculos):
        # Mover el carrito en un patrón de escaneo
        nueva_x = self.x + self.step_size * self.current_direction
        
        # Comprobar colisiones con los obstáculos
        for obstaculo in obstaculos:
            if (
                nueva_x < obstaculo.x + obstaculo.width and
                nueva_x + self.width > obstaculo.x and
                self.y < obstaculo.y + obstaculo.height and
                self.y + self.height > obstaculo.y
            ):
                # Si colisiona, cambiar de dirección
                self.current_direction *= -1
                nueva_x = self.x + self.step_size * self.current_direction
                break

        self.x = nueva_x

        # Cambiar de dirección al llegar a los bordes
        if self.x >= SCREEN_WIDTH - self.width:  # Llega al borde derecho
            self.x = SCREEN_WIDTH - self.width
            self.current_direction = -1  # Cambia dirección a izquierda
            self.y += self.step_size  # Baja un paso
        elif self.x <= 0:  # Llega al borde izquierdo
            self.x = 0
            self.current_direction = 1  # Cambia dirección a derecha
            self.y += self.step_size  # Baja un paso

        # Si el carrito llega al borde inferior, reinicia
        if self.y >= SCREEN_HEIGHT - self.height:  
            self.y = 0  # Reinicia la posición y para cubrir nuevamente el área
            self.path.clear()  # Limpia el recorrido

        # Agregar la posición actual a la trayectoria
        self.path.append((self.x + self.width // 2, self.y + self.height // 2))

    def dibujar(self, screen):
        # Dibujar el carrito
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

    def dibujar_recorrido(self, screen):
        # Dibujar el recorrido del carrito
        for pos in self.path:
            pygame.draw.circle(screen, RED, pos, 2)  # Dibuja un punto rojo en el recorrido

# Clase Obstáculo
class Obstaculo:
    def __init__(self, x, y, width=50, height=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def dibujar(self, screen):
        # Dibujar el obstáculo
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simulación de Carrito")

    carrito = Carrito()  # Inicializa el carrito
    obstaculos = []

    # Generar obstáculos en posiciones aleatorias
    for _ in range(5):  # Puedes ajustar el número de obstáculos
        x = random.randint(0, SCREEN_WIDTH - 50)
        y = random.randint(0, SCREEN_HEIGHT - 50)
        obstaculo = Obstaculo(x, y)
        obstaculos.append(obstaculo)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Mover el carrito
        carrito.mover(obstaculos)

        # Limpiar la pantalla
        screen.fill(WHITE)

        # Dibujar el área recorrida
        carrito.dibujar_recorrido(screen)

        # Dibujar los obstáculos
        for obstaculo in obstaculos:
            obstaculo.dibujar(screen)

        # Dibujar el carrito
        carrito.dibujar(screen)

        # Actualizar la pantalla
        pygame.display.flip()
        clock.tick(190)  # Limitar a 60 fps

    pygame.quit()

if __name__ == "__main__":
    main()
