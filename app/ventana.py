import pygame
from elementos.obstaculos import Obstaculo
import math
import random
from elementos.carrito import Carrito
# Variables globales para los obstáculos
obstaculos = []

def manejar_input(carrito, activo_input):
    """Maneja la entrada del usuario para el movimiento del carrito si no está escribiendo en los inputs."""
    
    # Solo usar el teclado si no hay inputs activos
    if not activo_input['motor1'] and not activo_input['motor2']:
        keys = pygame.key.get_pressed()  # Obtiene el estado de todas las teclas

        velocidad_motor1 = 0
        velocidad_motor2 = 0

        # Movimiento hacia adelante
        if keys[pygame.K_UP]:
            velocidad_motor1 = 100
            velocidad_motor2 = 100
        # Movimiento hacia atrás
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




def dibujar_cuadro_input(screen, carrito, font, input_velocidades, texto_input, activo_input):
    """Dibuja los cuadros de texto y las etiquetas en pantalla."""
     # Dimensiones del área de configuración
    config_width = 200  # Ancho fijo para el área de configuración
    config_height = 600  # Alto ajustado al alto de la pantalla
    config_x = 600  # Posición X fija (puedes ajustar según necesites)

    # Dibuja el área de configuración que ocupa todo el height
    pygame.draw.rect(screen, (200, 200, 200), (config_x, 0, config_width, config_height))  # Fondo para los inputs

    # Dibuja el área de configuración

    # Etiquetas
    motor1_label = font.render("Motor 1 Velocidad:", True, (0, 0, 0))
    screen.blit(motor1_label, (610, 50))
    motor2_label = font.render("Motor 2 Velocidad:", True, (0, 0, 0))
    screen.blit(motor2_label, (610, 110))

    # Dibujar cuadros de texto
    for motor, rect in input_velocidades.items():
        # Cambiar el color del cuadro si está activo
        color = (0, 255, 0) if activo_input[motor] else (255, 255, 255)
        pygame.draw.rect(screen, color, rect, 0)

        # Mostrar el texto ingresado
        texto_superficie = font.render(texto_input[motor], True, (0, 0, 0))
        screen.blit(texto_superficie, (rect.x + 5, rect.y + 5))

        # Dibujar el borde del cuadro
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)


def dibujar_boton(screen):
    """Dibuja un botón para agregar obstáculos."""
    button_rect = pygame.Rect(610, 100, 150, 40)
    pygame.draw.rect(screen, (0, 0, 255), button_rect)  # Botón azul

    font = pygame.font.Font(None, 30)
    text = font.render("Añadir Obstáculo", True, (255, 255, 255))
    screen.blit(text, (615, 110))

    return button_rect

def manejar_click_boton(button_rect):
    """Maneja el clic en el botón para añadir un obstáculo."""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(mouse_x, mouse_y):
        obstaculo = Obstaculo(mouse_x, mouse_y, 50, 50, (255, 0, 0))  # Crea un nuevo obstáculo
        obstaculos.append(obstaculo)  # Añade el obstáculo a la list
@staticmethod
def generar_obstaculos(cantidad, ancho_pantalla, alto_pantalla, carrito):
    """Genera obstáculos aleatorios que no colisionen con el carrito."""
    obstaculos = []
    for _ in range(cantidad):
        while True:
            x = random.randint(0, ancho_pantalla - 50)
            y = random.randint(0, alto_pantalla - 50)
            obstaculo = Obstaculo(x, y, 50, 50, color=(0, 255, 0))
            
            # Verificar que el obstáculo no esté sobre el carrito
            if not obstaculo.rect.colliderect(pygame.Rect(carrito.x, carrito.y, carrito.ancho, carrito.largo)):
                obstaculos.append(obstaculo)
                break  # Sale del bucle si el obstáculo es válido y no colisiona con el carrito

    return obstaculos
def manejar_eventos_input(event, input_velocidades, activo_input, texto_input):
    """Maneja los eventos para interactuar con los cuadros de texto."""
    if event.type == pygame.MOUSEBUTTONDOWN:
        # Verifica si el clic ocurrió dentro de algún input de velocidad
        for motor, rect in input_velocidades.items():
            if rect.collidepoint(event.pos):
                # Activa el cuadro de texto clicado y desactiva los demás
                activo_input[motor] = True
                for other_motor in activo_input:
                    if other_motor != motor:
                        activo_input[other_motor] = False
            else:
                activo_input[motor] = False

    if event.type == pygame.KEYDOWN:
        for motor, activo in activo_input.items():
            if activo:
                # Si está activo, captura la entrada de texto
                if event.key == pygame.K_BACKSPACE:
                    texto_input[motor] = texto_input[motor][:-1]  # Borra el último carácter
                else:
                    texto_input[motor] += event.unicode  # Añade el nuevo carácter
def aplicar_velocidades_inputs(carrito, texto_input):
    """Aplica las velocidades ingresadas en los inputs al carrito."""
    try:
        velocidad_motor1 = int(texto_input['motor1']) if texto_input['motor1'] else 0
        velocidad_motor2 = int(texto_input['motor2']) if texto_input['motor2'] else 0
        carrito.establecer_velocidades(velocidad_motor1, velocidad_motor2)
    except ValueError:
        pass  # Manejar error si no es un número válido
