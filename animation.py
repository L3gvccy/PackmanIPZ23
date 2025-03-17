from os import walk
import pygame
from settings import width, height, nav_height

def import_sprite(path):
	pygame.display.init()
	pygame.display.set_mode((width, height + nav_height))

	surface_list = []
	for _, __, img_file in walk(path):
		for image in img_file:
			full_path = f"{path}/{image}"
			img_surface = pygame.image.load(full_path).convert_alpha()
			surface_list.append(img_surface)
	return surface_list