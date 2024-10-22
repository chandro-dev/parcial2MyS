import pygame
import random

class Obstaculo:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def dibujar(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    @staticmethod
    def generar_obstaculos(num_obstaculos, screen_width, screen_height):
        obstaculos = []
        for _ in range(num_obstaculos):
            x = random.randint(0, screen_width - 50)
            y = random.randint(0, screen_height - 50)
            obstaculo = Obstaculo(x, y, 50, 50, (255, 0, 0))  # Color rojo
            obstaculos.append(obstaculo)
        return obstaculos
