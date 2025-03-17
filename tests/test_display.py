import pytest
import pygame
from display import Display

@pytest.fixture
def setup_display():
    """Фікстура для ініціалізації екземпляра Display"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    display = Display(screen)
    yield display
    pygame.quit()


def test_show_life(setup_display):
    """Перевірка, що метод show_life не викликає помилки"""
    display = setup_display
    display.show_life(3)


def test_show_level(setup_display):
    """Перевірка, чи правильно відображається рівень"""
    display = setup_display
    display.show_level(5) 


def test_show_score(setup_display):
    """Перевіряємо, чи відображається рахунок без помилок"""
    display = setup_display
    display.show_score(1500)


def test_game_over(setup_display):
    """Перевірка виклику методу game_over без помилок"""
    display = setup_display
    display.game_over()