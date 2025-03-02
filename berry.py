import pygame
from settings import char_size

class Berry(pygame.sprite.Sprite):
    def __init__(self, row, col, radius, is_power_up=False):
        super().__init__()
        self.power_up = is_power_up  # Чи є ягода бонусною
        self.radius = radius
        self.color = pygame.Color("yellow")
        self.border_thickness = radius  # Товщина межі

        # Обчислюємо позицію ягоди у пікселях
        self.pos_x = (row * char_size) + (char_size // 2)
        self.pos_y = (col * char_size) + (char_size // 2)

        # Створюємо прямокутник для визначення області ягоди
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.radius * 2, self.radius * 2)

    def update(self, screen):
        # Малюємо ягоду та оновлюємо його область
        self.rect = pygame.draw.circle(screen, self.color, (self.pos_x, self.pos_y), self.radius, self.border_thickness)
