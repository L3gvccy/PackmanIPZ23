import pygame

from settings import WIDTH, HEIGHT, CHAR_SIZE

pygame.font.init()

class Display:
	def __init__(self, screen):
		self.screen = screen
		self.font = pygame.font.SysFont("ubuntumono", CHAR_SIZE)
		self.game_over_font = pygame.font.SysFont("dejavusansmono", 48)
		self.text_color = pygame.Color("crimson")