import os
import pytest
import pygame
from pac import Pac
from settings import char_size, player_speed, height, width
from animation import import_sprite

@pytest.fixture(scope="module")
def pygame_setup():
    pygame.init()
    pygame.display.set_mode((width, height), pygame.NOFRAME)
    yield
    pygame.quit()

@pytest.fixture
def pac():
    pygame.init()
    return Pac(1, 1)

def test_initial_position(pac):
    """Перевірка початкової позиції"""
    assert pac.rect.x == 1 * char_size
    assert pac.rect.y == 1 * char_size

def test_initial_status(pac):
    """Перевірка початкового статусу"""
    assert pac.status == "idle"

def test_initial_life(pac):
    """Перевірка кількості життів"""
    assert pac.life == 3

def test_initial_score(pac):
    """Перевірка початкового рахунку"""
    assert pac.pac_score == 0

def test_move_to_start_pos(pac):
    """Перевірка повернення на стартову позицію"""
    pac.rect.x = 100
    pac.rect.y = 100
    pac.move_to_start_pos()
    assert pac.rect.x == pac.abs_x
    assert pac.rect.y == pac.abs_y

def test_immune_state(pac):
    """Перевірка роботи імунітету"""
    pac.immune_time = 5
    pac.update()
    assert pac.immune is True
    pac.immune_time = 0
    pac.update()
    assert pac.immune is False

def test_animation_change(pac):
    """Перевірка зміни анімації після натискання клавіші"""
    walls = []
    keys = {pygame.K_LEFT: True, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False}
    pac.animate(keys, walls)
    assert pac.status == "left"

def test_collision_handling(pac):
    """Перевірка реакції на перешкоди"""
    pac.walls_collide_list = [pygame.Rect(50, 50, char_size, char_size)]
    pac.rect.x, pac.rect.y = 48, 48 
    assert pac._is_collide(2, 2) is True
    assert pac._is_collide(-2, -2) is True
