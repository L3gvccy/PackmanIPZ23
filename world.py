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

		self.cell_color, self.berry_color = self.show_color_selection_menu()

		self._generate_world()

	def show_color_selection_menu(self):
		pygame.init()
		menu_screen = pygame.display.set_mode((width, height + nav_height))
		pygame.display.set_caption("Вибір кольорів")

		font = pygame.font.Font(None, 30)

        # Варіанти кольорів
		colors_cell = {
            "blue": (0, 44, 225),
            "purple": (130, 0, 225),
            "green": (14, 192, 5),
			"aqua": (0, 225, 174),
        }
		colors_berry = {
			"yellow": (255, 255, 0),
			"red": (255, 0, 0),
			"pink": (255, 0, 255),
			"teal": (0, 255, 255),
		}

		color_keys_cell = list(colors_cell.keys())
		color_keys_berry = list(colors_berry.keys())

		selected_cell_color = "blue"
		selected_berry_color = "yellow"

		running = True
		while running:
			menu_screen.fill((50, 50, 50))

			text1 = font.render("Оберіть колір стін:", True, (255, 255, 255))
			text2 = font.render("Оберіть колір ягід:", True, (255, 255, 255))

			menu_screen.blit(text1, (50, 30))
			menu_screen.blit(text2, (50, 150))

			text3 = font.render("Натисніть 'Enter' для підтвердження вибору", True, (255, 255, 255))
			menu_screen.blit(text3, (50, 270))

            # Відображення кнопок вибору кольору стін
			for i, color in enumerate(color_keys_cell):
				pygame.draw.rect(menu_screen, colors_cell[color], (50 + i * 90, 60, 80, 40))
				if selected_cell_color == color:
					pygame.draw.rect(menu_screen, (255, 255, 255), (50 + i * 90, 60, 80, 40), 3)

            # Відображення кнопок вибору кольору ягід
			for i, color in enumerate(color_keys_berry):
				pygame.draw.rect(menu_screen, colors_berry[color], (50 + i * 90, 180, 80, 40))
				if selected_berry_color == color:
					pygame.draw.rect(menu_screen, (255, 255, 255), (50 + i * 90, 180, 80, 40), 3)

			pygame.display.flip()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = event.pos

                    # Вибір кольору стін
					for i, color in enumerate(color_keys_cell):
						if 50 + i * 90 <= x <= 130 + i * 90 and 60 <= y <= 100:
							selected_cell_color = color

                    # Вибір кольору ягід
					for i, color in enumerate(color_keys_berry):
						if 50 + i * 90 <= x <= 130 + i * 90 and 180 <= y <= 220:
							selected_berry_color = color

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:  # Натискання Enter для підтвердження вибору
						running = False

		return selected_cell_color, selected_berry_color

	# створення та додавання гравця на екран
	def _generate_world(self):
		# рендерить перешкоди з таблиці MAP
		pygame.display.set_caption("Pacman")
		
		for y_index, col in enumerate(map_grid):
			for x_index, char in enumerate(col):
				if char == "1":	# для стін
					self.walls.add(Cell(x_index, y_index, char_size, char_size, self.cell_color))
				elif char == " ":	 # для шляхів, які потрібно заповнити ягодами
					self.berries.add(Berry(x_index, y_index, char_size // 4, self.berry_color))
				elif char == "b":	# для великих ягід
					self.berries.add(Berry(x_index, y_index, char_size // 2, self.berry_color, is_power_up=True))
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


	def generate_new_level(self):
		# Генерація ягід для нового рівня
		for y_index, col in enumerate(map_grid):
			for x_index, char in enumerate(col):
				if char == " ":
					self.berries.add(Berry(x_index, y_index, char_size // 4, self.berry_color))
				elif char == "b":
					self.berries.add(Berry(x_index, y_index, char_size // 2, self.berry_color, is_power_up=True))
		time.sleep(2)  # Затримка перед початком рівня


	def restart_level(self):
		# Перезапуск рівня
		self.berries.empty()
		[ghost.move_to_start_pos() for ghost in self.ghosts.sprites()]
		self.game_level = 1
		self.player.sprite.pac_score = 0
		self.player.sprite.life = 3
		self.player.sprite.move_to_start_pos()
		self.player.sprite.direction = (0, 0)
		self.player.sprite.status = "idle"
		self.generate_new_level()


	def _dashboard(self):
		# Панель з інформацією (рівень, життя, рахунок)
		nav = pygame.Rect(0, height, width, nav_height)
		pygame.draw.rect(self.screen, pygame.Color("cornsilk4"), nav)

		self.display.show_life(self.player.sprite.life)
		self.display.show_level(self.game_level)
		self.display.show_score(self.player.sprite.pac_score)


	def _check_game_state(self):
		# Перевірка стану гри
		if self.player.sprite.life == 0:
			self.game_over = True

		if len(self.berries) == 0 and self.player.sprite.life > 0:
			self.game_level += 1
			for ghost in self.ghosts.sprites():
				ghost.move_speed += self.game_level
				ghost.move_to_start_pos()
			self.player.sprite.move_to_start_pos()
			self.player.sprite.direction = (0, 0)
			self.player.sprite.status = "idle"
			self.generate_new_level()


	def update(self):
		if not self.game_over:
			# Рух гравця
			pressed_key = pygame.key.get_pressed()
			self.player.sprite.animate(pressed_key, self.walls_collide_list)

			# Телепортування на протилежний бік карти
			if self.player.sprite.rect.right <= 0:
				self.player.sprite.rect.x = width
			elif self.player.sprite.rect.left >= width:
				self.player.sprite.rect.x = 0

			# Поїдання ягід
			for berry in self.berries.sprites():
				if self.player.sprite.rect.colliderect(berry.rect):
					if berry.power_up:
						self.player.sprite.immune_time = 150
						self.player.sprite.pac_score += 50
					else:
						self.player.sprite.pac_score += 10
					berry.kill()

			# Зіткнення з привидами
			for ghost in self.ghosts.sprites():
				if self.player.sprite.rect.colliderect(ghost.rect):
					if not self.player.sprite.immune:
						time.sleep(2)
						self.player.sprite.life -= 1
						self.reset_pos = True
						break
					else:
						ghost.move_to_start_pos()
						self.player.sprite.pac_score += 100

		self._check_game_state()

		# Відображення об'єктів на екрані
		[wall.update(self.screen) for wall in self.walls.sprites()]
		[berry.update(self.screen) for berry in self.berries.sprites()]
		[ghost.update(self.walls_collide_list) for ghost in self.ghosts.sprites()]
		self.ghosts.draw(self.screen)

		self.player.update()
		self.player.draw(self.screen)
		self.display.game_over() if self.game_over else None

		self._dashboard()

		# Скидання позицій після зіткнення
		if self.reset_pos and not self.game_over:
			[ghost.move_to_start_pos() for ghost in self.ghosts.sprites()]
			self.player.sprite.move_to_start_pos()
			self.player.sprite.status = "idle"
			self.player.sprite.direction = (0, 0)
			self.reset_pos = False

		# Перезапуск гри при натисканні кнопки "R"
		if self.game_over:
			pressed_key = pygame.key.get_pressed()
			if pressed_key[pygame.K_r]:
				self.game_over = False
				self.restart_level()