import pygame, sys
from table import Table
from settings import width, height, cell_size, padding_x, padding_y, upper_padding

pygame.init()

screen = pygame.display.set_mode((width + padding_x*2, height + padding_y*2 + upper_padding))
pygame.display.set_caption("Sudokuuu")

pygame.font.init()

class Main:
	def __init__(self, screen):
		self.screen = screen
	def main(self):
		table = Table(self.screen, (padding_x, padding_y))
		playing = True
		table.generate_puzzle(20)
		while True:
			# Events
			self.handle_events(table, playing)
			self.screen.fill("gray")
			table.draw(screen)
			pygame.display.flip()
	def handle_events(self, table, playing):
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if playing:
					table.handle_mouse_click(event.pos)
			if event.type == pygame.KEYDOWN:
				if not table.mistake:
					if pygame.K_0 <= event.key <= pygame.K_9:
						table.fill_cell_value(event.key - pygame.K_0)
					elif pygame.K_KP1 <= event.key <= pygame.K_KP9:
						table.fill_cell_value(event.key - pygame.K_KP1 + 1)
				if (event.key == pygame.K_KP0 or event.key == pygame.K_BACKSPACE) and table.selected_cell.input_by_player:
					table.fill_cell_value(0)
					table.mistake = False

if __name__ == "__main__":
	play = Main(screen)
	play.main()

			