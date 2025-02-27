import pygame

from settings import CHAR_SIZE, PLAYER_SPEED

class Pac(pygame.sprite.Sprite):
	def __init__(self, row, col):
		super().__init__()

		self.abs_x = (row * CHAR_SIZE)
		self.abs_y = (col * CHAR_SIZE)

		self._import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.5
		self.image = self.animations["idle"][self.frame_index]
		self.rect = self.image.get_rect(topleft = (self.abs_x, self.abs_y))
		self.mask = pygame.mask.from_surface(self.image)

		self.pac_speed = PLAYER_SPEED
		self.immune_time = 0
		self.immune = False

		self.directions = {'left': (-PLAYER_SPEED, 0), 'right': (PLAYER_SPEED, 0), 'up': (0, -PLAYER_SPEED), 'down': (0, PLAYER_SPEED)}
		self.keys = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN}
		self.direction = (0, 0)
	
		# pac status
		self.status = "idle"
		self.life = 3
		self.pac_score = 0