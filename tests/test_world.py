import pytest
import pygame
from world import World
from settings import width, height, nav_height

def mock_show_color_selection_menu(self):
    """ Мок для вибору кольору """
    return "blue", "yellow"

@pytest.fixture
def setup_world(mocker):
    pygame.init()
    screen = pygame.Surface((width, height + nav_height))
    mocker.patch.object(World, "show_color_selection_menu", mock_show_color_selection_menu)
    return World(screen)

def test_world_creation(setup_world):
    """ Перевіряємо, що світ створюється без помилок """
    world = setup_world
    assert world is not None
    assert len(world.walls) > 0
    assert len(world.berries) > 0
    assert len(world.ghosts) > 0
    assert world.player.sprite is not None

def test_pac_eats_berry(setup_world):
    """ Перевіряємо, що PacMan може з'їсти ягоду """
    world = setup_world
    pac = world.player.sprite
    berry = next(iter(world.berries))  
    pac.rect.topleft = berry.rect.topleft  
    world.update()
    assert berry not in world.berries  
    assert pac.pac_score > 0  

def test_pac_collides_with_ghost(setup_world):
    """ Перевіряємо, що PacMan втрачає життя при зіткненні із привидом """
    world = setup_world
    pac = world.player.sprite
    ghost = next(iter(world.ghosts))
    pac.rect.topleft = ghost.rect.topleft  
    initial_lives = pac.life
    world.update()
    assert pac.life == initial_lives - 1  

def test_game_over(setup_world):
    """ Перевіряємо, що гра закінчується, якщо життя закінчилося """
    world = setup_world
    pac = world.player.sprite
    pac.life = 1 
    ghost = next(iter(world.ghosts))
    pac.rect.topleft = ghost.rect.topleft 
    world.update()
    assert world.game_over is True 