import pygame
import random

class Obstaculo:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def dibujar(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

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