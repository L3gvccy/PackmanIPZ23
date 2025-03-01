import pygame
import time

from settings import height, width, nav_height, char_size, map_grid, player_speed
from pac import Pac
from cell import Cell
from berry import Berry
from ghost import Ghost
from display import Display

class World:
	def __init__(self, screen):
		self.screen = screen

		self.player = pygame.sprite.GroupSingle()
		self.ghosts = pygame.sprite.Group()
		self.walls = pygame.sprite.Group()
		self.berries = pygame.sprite.Group()

		self.display = Display(self.screen)

		self.game_over = False
		self.reset_pos = False
		self.player_score = 0
		self.game_level = 1

		self._generate_world()


	# створення та додавання гравця на екран
	def _generate_world(self):
		# рендерить перешкоди з таблиці MAP
		for y_index, col in enumerate(map_grid):
			for x_index, char in enumerate(col):
				if char == "1":	# для стін
					self.walls.add(Cell(x_index, y_index, char_size, char_size))
				elif char == " ":	 # для шляхів, які потрібно заповнити ягодами
					self.berries.add(Berry(x_index, y_index, char_size // 4))
				elif char == "b":	# для великих ягід
					self.berries.add(Berry(x_index, y_index, char_size // 2, is_power_up=True))
				# для стартових позицій примар
				elif char == "s":
					self.ghosts.add(Ghost(x_index, y_index, "skyblue"))
				elif char == "p":
					self.ghosts.add(Ghost(x_index, y_index, "pink"))
				elif char == "o":
					self.ghosts.add(Ghost(x_index, y_index, "orange"))
				elif char == "r":
					self.ghosts.add(Ghost(x_index, y_index, "red"))

				elif char == "P":	# для стартової позиції PacMan
					self.player.add(Pac(x_index, y_index))

		self.walls_collide_list = [wall.rect for wall in self.walls.sprites()]
