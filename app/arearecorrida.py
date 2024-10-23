import pygame
import random

# Configuraciones de la ventana
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clase Carrito
class Carrito:
    def __init__(self, start_x, start_y):
        self.x = start_x  # Posición inicial en x
        self.y = start_y  # Posición inicial en y
        self.width = 20
        self.height = 10
        self.step_size = 5  # Tamaño del paso
        self.path = []  # Almacena el recorrido
        self.current_direction = 1  # 1: derecha, -1: izquierda

    def mover(self, obstaculos):
        # Mover el carrito en un patrón de escaneo
        self.x += self.step_size * self.current_direction

        # Cambiar de dirección al llegar a los bordes
        if self.x >= SCREEN_WIDTH - 200 - self.width:  # Llega al borde derecho del área de trabajo
            self.x = SCREEN_WIDTH - 200 - self.width
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

        # Evitar obstáculos
        for obstaculo in obstaculos:
            if self.colision(obstaculo):
                # Cambiar dirección al colisionar
                self.current_direction *= -1  # Cambia de dirección
                break  # Salir del bucle para evitar múltiples colisiones

        # Agregar la posición actual a la trayectoria
        self.path.append((self.x + self.width // 2, self.y + self.height // 2))

    def colision(self, obstaculo):
        # Verifica si hay colisión con un obstáculo
        return (self.x < obstaculo.x + obstaculo.width and
                self.x + self.width > obstaculo.x and
                self.y < obstaculo.y + obstaculo.height and
                self.y + self.height > obstaculo.y)

    def dibujar(self, screen):
        # Dibujar el carrito
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

    def dibujar_recorrido(self, screen):
        # Dibujar el recorrido del carrito
        for pos in self.path:
            pygame.draw.circle(screen, RED, pos, 2)  # Dibuja un punto rojo en el recorrido

# Clase Obstáculo
class Obstaculo:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH - 230)  # Ajustar para evitar superposición con el panel
        self.y = random.randint(0, SCREEN_HEIGHT - 30)
        self.width = 30
        self.height = 30

    def dibujar(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))

# Clase Panel
class Panel:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.button_color = (0, 0, 255)
        self.button_rect = pygame.Rect(self.x + 10, self.y + 10, self.width - 20, 50)

    def dibujar(self, screen):
        # Dibujar el panel
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
        
        # Dibujar el botón dentro del panel
        pygame.draw.rect(screen, self.button_color, self.button_rect)
        font = pygame.font.SysFont(None, 24)
        text = font.render("Agregar Obstáculos", True, WHITE)
        text_rect = text.get_rect(center=self.button_rect.center)
        screen.blit(text, text_rect)

# Clase principal
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simulación de Carritos")

    # Inicializa dos carritos en posiciones distintas
    carritos = [Carrito(50, 50), Carrito(100, 100)]  # Cada carrito tiene una posición inicial diferente
    obstaculos = []  # Lista para almacenar obstáculos
    panel = Panel(200, SCREEN_HEIGHT)  # Crear el panel lateral
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del ratón
                    # Verificar si se ha hecho clic en el botón
                    if panel.button_rect.collidepoint(event.pos):
                        # Agregar un nuevo obstáculo
                        obstaculos.append(Obstaculo())

        # Mover cada carrito
        for carrito in carritos:
            carrito.mover(obstaculos)

        # Limpiar la pantalla
        screen.fill(WHITE)

        # Dibujar el panel
        panel.dibujar(screen)

        # Dibujar los obstáculos
        for obstaculo in obstaculos:
            obstaculo.dibujar(screen)

        # Dibujar el área recorrida de cada carrito
        for carrito in carritos:
            carrito.dibujar_recorrido(screen)

        # Dibujar los carritos
        for carrito in carritos:
            carrito.dibujar(screen)

        # Actualizar la pantalla
        pygame.display.flip()
        clock.tick(60)  # Limitar a 60 fps

    pygame.quit()

if __name__ == "__main__":
    main()
