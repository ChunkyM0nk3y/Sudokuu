import pygame
from settings import cell_color, cell_border_color as border_color, default_font_color, added_font_color, upper_padding

pygame.font.init()

class Cell:
	def __init__(self, row, col, cell_size, value, padding):
		self.row = row
		self.input_by_player = False
		self.col = col
		self.cell_size = cell_size
		self.value = value
		self.width = cell_size[0]
		self.height = cell_size[1]
		self.abs_x = row * self.width + padding[0]
		self.abs_y = col * self.height + padding[1] + upper_padding
		self.font = pygame.font.SysFont("monspace", self.cell_size[0])
		self.g_font = pygame.font.SysFont("monspace", self.cell_size[0] // 3)
		self.rect = pygame.Rect(self.abs_x, self.abs_y, self.width, self.height)
		self.color = cell_color
	def draw(self, screen):
		pygame.draw.rect(screen, self.color, self.rect)
		pygame.draw.rect(screen, border_color, self.rect, 1)
		if self.value != 0:
			font_color = added_font_color if self.input_by_player else default_font_color
			value_surface = self.font.render(str(self.value), True, font_color)
			value_rect = value_surface.get_rect(center = self.rect.center)
			screen.blit(value_surface, value_rect)
		elif self.value == 0:
			pass
		