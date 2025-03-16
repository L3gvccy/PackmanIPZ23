import pytest
import pygame
from berry import Berry 

@pytest.fixture
def setup_berry():
    """Фікстура для створення екземпляра Berry"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    berry = Berry(row=5, col=5, radius=10, color="red", is_power_up=True)
    yield berry, screen
    pygame.quit()

def test_berry_init(setup_berry):
    """Тест ініціалізації об'єкту Berry"""
    berry, _ = setup_berry
    assert berry.radius == 10
    assert berry.color == pygame.Color("red")
    assert berry.power_up is True

def test_berry_position(setup_berry):
    """Тест коректності розрахунку позиції ягоди"""
    berry, _ = setup_berry
    assert berry.pos_x == (5 * 32) + (32 // 2)  # char_size передбачається 32
    assert berry.pos_y == (5 * 32) + (32 // 2)

def test_berry_update(setup_berry):
    """Тест отрисовки ягоди (перевірка на відсутність помилок)"""
    berry, screen = setup_berry
    berry.update(screen)