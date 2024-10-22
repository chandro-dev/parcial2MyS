import pygame
from elementos.carrito import Carrito
from ventana import manejar_input, dibujar_cuadro_input,dibujar_boton,manejar_click_boton,generar_obstaculos
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
pygame.init()

# Dimensiones de la ventana
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simulador de Carrito")
# Generar obstáculos
obstaculos = generar_obstaculos(3, SCREEN_WIDTH, SCREEN_HEIGHT)
# Crear el carrito

carrito = Carrito(ancho=50, largo=30, L=60)  # Define el ancho, largo y distancia entre ruedas


clock = pygame.time.Clock()  # Inicializa el reloj

# Bucle principal
running = True
while running:
    dt = clock.tick(60) / 1000  # Tiempo desde el último frame en segundos
 # Manejar eventos (incluyendo salida)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    manejar_input(carrito)
    # Actualizar posición del carrito
    carrito.actualizar_posicion(dt=dt, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, obstaculos=obstaculos)

    # Dibujar todo
    screen.fill(WHITE)
    
    # Dibuja los obstáculos
    for obstaculo in obstaculos:
        obstaculo.dibujar(screen)  # Llama al método dibujar para cada obstáculo

    dibujar_cuadro_input(screen, carrito)
    # Dibuja el carrito
    carrito.dibujar(screen)
    pygame.display.flip()




pygame.quit()