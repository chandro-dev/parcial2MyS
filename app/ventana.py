import pygame
from elementos.obstaculos import Obstaculo
import math
import random

# Variables globales para los obstáculos
obstaculos = Obstaculo.generar_obstaculos(0, 800, 600)  # Genera 5 obstáculos aleatorios

def manejar_input(carrito):
    # Manejar entradas para el movimiento del carrito
   import pygame
from elementos.carrito import Carrito

def manejar_input(carrito):
    """Maneja la entrada del usuario para el movimiento del carrito."""
    keys = pygame.key.get_pressed()  # Obtiene el estado de todas las teclas

    velocidad_motor1 = 0
    velocidad_motor2 = 0

    # Movimiento hacia arriba
    if keys[pygame.K_UP]:
        velocidad_motor1 = 100
        velocidad_motor2 = 100
    # Movimiento hacia abajo
    if keys[pygame.K_DOWN]:
        velocidad_motor1 = -100
        velocidad_motor2 = -100
    # Girar a la izquierda
    if keys[pygame.K_LEFT]:
        velocidad_motor1 = -100
        velocidad_motor2 = 100
    # Girar a la derecha
    if keys[pygame.K_RIGHT]:
        velocidad_motor1 = 100
        velocidad_motor2 = -100

    # Establece las velocidades en el carrito
    carrito.establecer_velocidades(velocidad_motor1, velocidad_motor2)


def dibujar_cuadro_input(screen, carrito):
    # Dibuja el carrito y los obstáculos
    carrito_rect = pygame.Rect(carrito.x, carrito.y, carrito.ancho, carrito.largo)
    rotated_surface = pygame.transform.rotate(pygame.Surface((carrito.ancho, carrito.largo)), -math.degrees(carrito.theta))
    screen.blit(rotated_surface, carrito_rect.topleft)

    for obstaculo in obstaculos:
        obstaculo.dibujar(screen)

    # Verificar colisiones
    for obstaculo in obstaculos:
        if carrito_rect.colliderect(obstaculo.rect):
            print("Colisión detectada con un obstáculo!")

def dibujar_boton(screen):
    button_rect = pygame.Rect(10, 10, 150, 40)
    pygame.draw.rect(screen, (0, 0, 255), button_rect)  # Botón azul
    font = pygame.font.Font(None, 30)
    text = font.render("Añadir Obstáculo", True, (255, 255, 255))
    screen.blit(text, (15, 15))

    return button_rect

def manejar_click_boton(carrito, button_rect):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_x, mouse_y):
        obstaculo = Obstaculo(mouse_x, mouse_y, 50, 50, (255, 0, 0))
        obstaculos.append(obstaculo)  # Añadir el nuevo obstáculo
def generar_obstaculos(cantidad, ancho_pantalla, alto_pantalla):
    """Genera obstáculos aleatorios en la pantalla."""
    obstaculos = []
    for _ in range(cantidad):
        x = random.randint(0, ancho_pantalla - 50)  # Ajusta 50 al ancho del obstáculo
        y = random.randint(0, alto_pantalla - 50)   # Ajusta 50 al alto del obstáculo
        obstaculos.append(Obstaculo(x, y, 50, 50,color=(0, 255, 0)))   # Ajusta 50 y 50 al tamaño del obstáculo
    return obstaculos
