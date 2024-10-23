import math
import pygame

class Carrito:
    def __init__(self, ancho, largo, L, x_inicial=500, y_inicial=500):
        self.ancho = ancho  # Ancho del carrito
        self.largo = largo  # Largo del carrito
        self.motor1 = 0  # Velocidad del motor izquierdo
        self.motor2 = 0  # Velocidad del motor derecho
        self.x = x_inicial  # Posición inicial en X
        self.y = y_inicial  # Posición inicial en Y
        self.theta = 0  # Ángulo de orientación (radianes)
        self.L = L  # Distancia entre las ruedas
        self.v = 0  # Velocidad lineal
        self.omega = 0  # Velocidad angular   
        self.velocidad = 0
     
        # Cargar la imagen del carrito
        self.image = pygame.image.load("app/public/carrito.png")  # Cambia la ruta a tu imagen
        self.image = pygame.transform.scale(self.image, (self.ancho, self.largo))  # Escalar la imagen al tamaño del carrito

        # Invertir la imagen horizontalmente (True para horizontal, False para vertical)
        self.image = pygame.transform.flip(self.image, True, False)  # Invertir solo horizontalmente


    def establecer_velocidades(self, velocidad_motor1, velocidad_motor2):
        """Establece las velocidades de los motores."""
        self.motor1 = velocidad_motor1
        self.motor2 = velocidad_motor2
        self.velocidad = (velocidad_motor1 + velocidad_motor2) / 2
        self.actualizar_movimiento()

    def actualizar_movimiento(self):
        """Calcula la velocidad lineal y angular basadas en las ecuaciones de mecánica."""
        self.v = (self.motor1 + self.motor2) / 2
        self.omega = (self.motor2 - self.motor1) / self.L

    def actualizar_posicion(self, dt, screen_width, screen_height, obstaculos):
        """Actualiza la posición del carrito y lo limita dentro de los bordes."""
        self.theta += self.omega * dt
        new_x = self.x + self.v * math.cos(self.theta) * dt
        new_y = self.y + self.v * math.sin(self.theta) * dt

        # Crear un rectángulo temporal para el carrito
        carrito_rect = pygame.Rect(new_x, new_y, self.ancho, self.largo)

        # Verificar colisiones con obstáculos
        for obstaculo in obstaculos:
            if carrito_rect.colliderect(obstaculo.rect):
                # Si hay colisión, detener el carrito
                self.motor1 = 0
                self.motor2 = 0
                self.v = 0
                self.omega = 0
                break  # Salir del bucle si hay colisión

        # Si no hay colisión, actualizar posición
        else:
            # Limitar el movimiento del carrito dentro de la pantalla
            if 0 <= new_x <= screen_width - self.ancho:
                self.x = new_x
            if 0 <= new_y <= screen_height - self.largo:
                self.y = new_y

    def mostrar_estado(self):
        """Muestra el estado actual del carrito."""
        print(f"Posición: x={self.x:.2f}, y={self.y:.2f}, ángulo={math.degrees(self.theta):.2f}°")
        print(f"Velocidad lineal: {self.v:.2f}, Velocidad angular: {self.omega:.2f}")
    def dibujar(self, screen):
        # Rotar la imagen según el ángulo theta
        rotated_image = pygame.transform.rotate(self.image, -math.degrees(self.theta))
        
        # Obtener el rectángulo de la imagen rotada centrado en la nueva posición (x, y)
        rect = rotated_image.get_rect(center=(self.x + self.ancho // 2, self.y + self.largo // 2))
        
        # Dibujar la imagen en la pantalla
        screen.blit(rotated_image, rect.topleft)