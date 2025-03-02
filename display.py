import pygame

from settings import width, height, char_size

pygame.font.init()

class Display:
	def __init__(self, screen):
		self.screen = screen
		self.font = pygame.font.SysFont("ubuntumono", char_size)
		self.game_over_font = pygame.font.SysFont("dejavusansmono", 48)
		self.text_color = pygame.Color("crimson")

    # Показати кількість життів			
	def show_life(self, life):
		img_path = "assets/life/life.png"
		life_image = pygame.image.load(img_path)
		life_image = pygame.transform.scale(life_image, (char_size, char_size))
		life_x = char_size // 2

		if life != 0:
			for life in range(life):
				self.screen.blit(life_image, (life_x, height + (char_size // 2)))
				life_x += char_size

    # Показати рівень
	def show_level(self, level):
		level_x = width // 3
		level = self.font.render(f'Level {level}', True, self.text_color)
		self.screen.blit(level, (level_x, (height + (char_size // 2))))

    # Показати рахунок
	def show_score(self, score):
		score_x = width // 3
		score = self.font.render(f'{score}', True, self.text_color)
		self.screen.blit(score, (score_x * 2, (height + (char_size // 2))))

    # Повідомлення про завершення гри 
	def game_over(self):
		message = self.game_over_font.render(f'Гра завершена!', True, pygame.Color("chartreuse"))
		instruction = self.font.render(f'Натисніть "R" щоб почати знову', True, pygame.Color("aqua"))
		self.screen.blit(message, ((width // 4), (height // 3)))
		self.screen.blit(instruction, ((width // 4), (height // 2)))