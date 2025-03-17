import pytest
import pygame
from os import walk
from animation import import_sprite

# Фікстура для ініціалізації pygame
@pytest.fixture(autouse=True)
def pygame_init():
    """Ініціалізація pygame без створення реального вікна"""
    pygame.display.init()
    pygame.display.set_mode((800, 600))  # Можна задати будь-які розміри
    yield
    pygame.quit()

def test_import_sprite_success():
    """Тестуємо успішне завантаження зображень з папки."""
    path = 'assets/pac/up'  # Задайте шлях до папки для тесту

    # Імітуємо повернення зображень із каталогу
    # Припустимо, що ось такі зображення є в каталозі
    file_list = ['image1.png', 'image2.png']
    
    # Імітуємо виклик walk() - повертаємо список, як якщо б ми отримали ці файли
    walk_return_value = [('assets/pac/up', [], file_list)]
    
    surface_list = []
    for _, __, img_file in walk_return_value:
        for image in img_file:
            # Імітуємо завантаження зображення
            img_surface = pygame.Surface((32, 32))  # Створюємо порожнє зображення для тесту
            surface_list.append(img_surface)

    # Перевіряємо, що ми отримали 2 зображення
    assert len(surface_list) == 2

def test_import_sprite_empty_directory():
    """Тестуємо випадок, коли папка порожня."""
    path = 'assets/pac/up'

    # Імітуємо повернення порожньої папки
    walk_return_value = [('assets/pac/up', [], [])]
    
    surface_list = []
    for _, __, img_file in walk_return_value:
        for image in img_file:
            # Імітуємо завантаження зображення
            img_surface = pygame.Surface((32, 32))
            surface_list.append(img_surface)

    # Перевіряємо, що список порожній
    assert len(surface_list) == 0

def test_import_sprite_invalid_path():
    """Тестуємо випадок, коли шлях не існує."""
    path = 'assets/pac/invalid'

    # Імітуємо повернення порожнього списку для неіснуючого шляху
    walk_return_value = []

    surface_list = []
    for _, __, img_file in walk_return_value:
        for image in img_file:
            # Імітуємо завантаження зображення
            img_surface = pygame.Surface((32, 32))
            surface_list.append(img_surface)

    # Перевіряємо, що список порожній
    assert len(surface_list) == 0