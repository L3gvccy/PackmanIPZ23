import pytest
import pygame
from ghost import Ghost  

@pytest.fixture
def setup_ghost():
    """Фікстура для створення об'єкта Ghost"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    ghost = Ghost(row=5, col=5, color="skyblue")
    yield ghost, screen
    pygame.quit()

def test_ghost_init(setup_ghost):
    """Перевіряємо коректність ініціалізації об'єкту Ghost"""
    ghost, _ = setup_ghost
    assert ghost.rect.x == (5 * 32)
    assert ghost.rect.y == (5 * 32)
    assert ghost.color == pygame.Color("skyblue")
    assert ghost.move_speed > 0

def test_ghost_move_to_start_pos(setup_ghost):
    """Перевіряємо, що move_to_start_pos коректно повертає привид у початкову позицію"""
    ghost, _ = setup_ghost
    ghost.rect.x += 50
    ghost.rect.y += 50
    ghost.move_to_start_pos()
    assert ghost.rect.x == (5 * 32)
    assert ghost.rect.y == (5 * 32)

def test_ghost_collision(setup_ghost):
    """Перевіряємо, що is_collide працює коректно"""
    ghost, _ = setup_ghost
    ghost.rect.topleft = (160, 160)  # Привид знаходиться в цій точці
    walls = [pygame.Rect(192, 160, 32, 32)]  # Стіна праворуч від привиду
    # Якщо привид рухається праворуч, він має зіткнутися
    assert ghost.is_collide(33, 0, walls) is True, "Привид повинен стикатися зі стіною праворуч"
    # Якщо рухається вліво (де немає стіни) - зіткнення не повинно бути
    assert ghost.is_collide(-33, 0, walls) is False, "Привид не повинен стикатися під час руху вліво"


def test_ghost_update(setup_ghost):
    """Перевіряємо, що update не викликає помилок"""
    ghost, _ = setup_ghost
    walls = [
        pygame.Rect(160, 160, 32, 32),  
        pygame.Rect(160, 192, 32, 32)   
    ]
    ghost.rect.topleft = (128, 160)  
    ghost.update(walls) 
    

