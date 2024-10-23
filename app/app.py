import pygame
from elementos.carrito import Carrito
from ventana import manejar_input, dibujar_cuadro_input,dibujar_boton,manejar_click_boton,generar_obstaculos,manejar_velocidades_auto
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE

pygame.init()

# Dimensiones de la ventana
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simulador de Carrito")

# Crear el carrito
carrito = Carrito(ancho=100, largo=50, L=120)  # Define el ancho, largo y distancia entre ruedas

# Generar obstáculos
obstaculos = generar_obstaculos(3, SCREEN_WIDTH-200, SCREEN_HEIGHT, carrito)


# Configuraciones de input
font = pygame.font.Font(None, 30)
input_velocidades = {
    'motor1': pygame.Rect(610, 80, 100, 30),
    'motor2': pygame.Rect(610, 140, 100, 30)
}
activo_input = {'motor1': False, 'motor2': False}
texto_input = {'motor1': "", 'motor2': ""}
clock = pygame.time.Clock()  # Inicializa el reloj

# Bucle principal
running = True
while running:
    dt = clock.tick(60) / 1000  # Tiempo desde el último frame en segundos

    # Manejar eventos (incluyendo salida)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    manejar_velocidades_auto(carrito)
    # Actualizar posición del carrito
    carrito.actualizar_posicion(dt=dt, screen_width=SCREEN_WIDTH-200, screen_height=SCREEN_HEIGHT, obstaculos=obstaculos)

    # Dibujar todo
    screen.fill(WHITE)  # Limpiar la pantalla

    # Dibujar el carrito
    carrito.dibujar(screen)

    # Dibujar los obstáculos
    for obstaculo in obstaculos:
        obstaculo.dibujar(screen)

    # Dibujar el botón para añadir obstáculos
    button_rect = dibujar_boton(screen)

    # Dibujar el cuadro de configuraciones
    dibujar_cuadro_input(screen, carrito, font, input_velocidades, texto_input, activo_input)

    # Manejar el clic en el botón para añadir obstáculos
    manejar_click_boton(button_rect)

    # Actualizar la pantalla
    pygame.display.flip()

pygame.quit()
