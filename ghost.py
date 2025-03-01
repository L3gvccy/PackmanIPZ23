import pygame
import random
import time
from settings import width, char_size, ghost_speed

class Ghost(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        super().__init__()
        self.pos_x = (row * char_size)
        self.pos_y = (col * char_size)
        self.rect = pygame.Rect(self.pos_x, self.pos_y, char_size, char_size)  # Прямокутник для розташування привиду
        self.move_speed = ghost_speed
        self.color = pygame.Color(color)
        self.move_directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        self.moving_dir = "up"  # Початковий напрямок руху
        self.img_path = f'assets/ghosts/{color}/'
        self.img_name = f'{self.moving_dir}.png'
        self.image = pygame.image.load(self.img_path + self.img_name)
        self.image = pygame.transform.scale(self.image, (char_size, char_size))
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))  # Встановлення координат для прямокутника
        self.mask = pygame.mask.from_surface(self.image)
        self.directions = {'left': (-self.move_speed, 0), 'right': (self.move_speed, 0), 'up': (0, -self.move_speed), 'down': (0, self.move_speed)}  # Напрямки руху та їх значення
        self.keys = ['left', 'right', 'up', 'down']  # Список можливих напрямків
        self.direction = (0, 0)  # Поточний напрямок руху

    def move_to_start_pos(self):
        self.rect.x = self.pos_x  # Повернення привиду на стартову позицію по X
        self.rect.y = self.pos_y  # Повернення привиду на стартову позицію по Y

    def is_collide(self, x, y, walls_collide_list):#Перевірка на зіткнення привида зі стіною
        tmp_rect = self.rect.move(x, y)
        if tmp_rect.collidelist(walls_collide_list) == -1:
            return False
        return True

    def _animate(self):
        self.img_name = f'{self.moving_dir}.png'
        self.image = pygame.image.load(self.img_path + self.img_name)
        self.image = pygame.transform.scale(self.image, (char_size, char_size))
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))# Оновлюємо координати прямокутника

    def update(self, walls_collide_list):
        # Створюємо список доступних напрямків руху
        available_moves = []
        # Перевіряємо кожну клавішу управління, чи можна рухатися в цьому напрямку без зіткнення зі стінами
        for key in self.keys:
            if not self.is_collide(*self.directions[key], walls_collide_list):
                available_moves.append(key)
        # Визначаємо, чи варто рандомізувати рух
        randomizing = False if len(available_moves) <= 2 and self.direction != (0, 0) else True

        if randomizing and random.randrange(0, 100) <= 60:
            self.moving_dir = random.choice(available_moves)
            self.direction = self.directions[self.moving_dir]

        # Перевіряємо, чи можемо рухатися в поточному напрямку
        if not self.is_collide(*self.direction, walls_collide_list):
            self.rect.move_ip(self.direction)
        else:
            self.direction = (0, 0)  # Якщо зіткнення є, зупиняємо рух

        # Переміщуємо об'єкт на протилежний край екрану, якщо він вийшов за межі
        if self.rect.right <= 0:
            self.rect.x = width
        elif self.rect.left >= width:
            self.rect.x = 0

        self._animate()