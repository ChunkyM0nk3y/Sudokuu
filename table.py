import pygame
import math
import random
from cell import Cell
#from sudoku import Sudoku
#from clock import Clock
from settings import outer_grid_color

from settings import width, height, n_cells, cell_size, sel_cel_color, cell_color, cell_highlight_color, same_num_highlight_color, wrong_highlight_color
from settings import wrong_font_color

pygame.font.init()

class Table:
	def __init__(self, screen, pos):
		self.screen = screen
		self.table_cells = []
		self.pos = pos
		self.selected_cell = 0

		# Generates the sudoku table
		self.table_cells = [[0] * n_cells for _ in range(n_cells)]
		for row in range(n_cells): 
			for col in range(n_cells):
				cell_value = 0
				self.table_cells[row][col] = Cell(row, col, cell_size, cell_value, pos)
	def draw(self):
		for row in range(n_cells): 
			for col in range(n_cells):
				self.table_cells[row][col].draw(self.screen)
		self._draw_grid()
	def handle_mouse_click(self, click_pos):
		# Selected cell (as an iterator)
		if 0 < click_pos[0] < width and 0 < click_pos[1] < height:
			x = (click_pos[0] - self.pos[0]) // cell_size[0]
			y = (click_pos[1] - self.pos[1]) // cell_size[1]
			
			if(x < 0 or x > len(self.table_cells) or y < 0 or y > len(self.table_cells[0])):
				return
			
			#selected a specific cell
			print(f"selected cell x: {x}")
			print(f"selected cell y: {y}")	
			
			if self.selected_cell:	#unselects the last selected cell - changes its color
				self.selected_cell.color = cell_color
				for i in range(n_cells): #uncolors the row and column highlighter
					for j in range(n_cells):
						self.table_cells[i][j].color = cell_color
			
			cell = self.table_cells[x][y]
			self.selected_cell = cell

			#highlight the row and column and the sector
			for i in range(n_cells):
				self.table_cells[i][y].color = cell_highlight_color
				self.table_cells[x][i].color = cell_highlight_color
			
			cell.color = sel_cel_color

			#highligh other same valued cells
			self._other_value_highlighter(x, y)


	def fill_cell_value(self, value):
		if self.selected_cell:
			self.selected_cell.value = value
			self.selected_cell.input_by_player = True
			if(self.is_valid(self.selected_cell.row, self.selected_cell.col, self.selected_cell.value)):
				pass
			self._other_value_highlighter(self.selected_cell.row, self.selected_cell.col)

	def is_valid(self, table, x, y, num):
		#check rows and cols
		for i in range(n_cells):
			if table[i][y].value == num:
				return False
			if table[x][i].value == num:
				return False
		
		#check 3x3 grid
		start_x, start_y = 3 * (x // 3), 3 * (y // 3)
		for i in range(3):
			for j in range(3):
				if table[start_x + i][start_y + j].value == num:
					return False
		return True
	

	
	# Returns possible nums for a given cell -> does not recycle
	def return_valid_nums(self):
		x = self.selected_cell.row
		y = self.selected_cell.col
		num = self.selected_cell.value
		
		#check rows and cols
		for i in range(n_cells):
			if self.table_cells[i][y].value == num:
				return False
			if self.table_cells[x][i].value == num:
				return False
		
		#check 3x3 grid
		start_x, start_y = 3 * (x // 3), 3 * (y // 3)
		for i in range(3):
			for j in range(3):
				if self.table_cells[start_x + i][start_y + j] == num:
					return False
		return True
	
	'''
		Generates the puzzle - 
	'''
	def backtracking_sudoku_solver(self):
		for row in range(n_cells):
			for col in range(n_cells):
				if self.table_cells[row][col].value == 0: #empty cell
					for num in random.sample(range(1, 10), 9): #takes a random number
						if self.is_valid(self.table_cells, row, col, num):
							self.table_cells[row][col].value = num
							if self.backtracking_sudoku_solver():
								return True
							self.table_cells[row][col].value = 0
					return False
		return True
	
	def count_solutions(self):
		temp_table = [row[:] for row in self.table_cells]
		solutions = [0] # no. of different solutions -> an array so that it can be modified by the insider function

		def solve_with_count(table):
			for row in range(n_cells):
				for col in range(n_cells):
					if table[row][col].value == 0:
						for n in range(1, 10):
							if self.is_valid(table, row, col, n):
								table[row][col].value = n
								solve_with_count(table)
								table[row][col].value = 0
						return
			solutions[0] += 1
			if solutions[0] > 1:
				return
		solve_with_count(temp_table)
		return solutions[0]

	def remove_numbers(self, ammount=40):
		positions = [(r, c) for r in range(n_cells) for c in range(n_cells)]
		random.shuffle(positions)

		removed = 0
		while removed < ammount:
			row, col = positions.pop()
			backup = self.table_cells[row][col]
			self.table_cells[row][col].value = 0

			if self.count_solutions() != 1:
				self.table_cells[row][col] = backup
			else:
				removed += 1

	def generate_puzzle(self):
		self.backtracking_sudoku_solver()
		self.remove_numbers(40)

	def _draw_grid(self):
		# Basic 9x9 sudoku 9 seperate grid parts drawing
		for row in range(3 + 1):
			pygame.draw.line(self.screen, outer_grid_color, (self.pos[0] + row*cell_size[0]*3, self.pos[1]), (self.pos[0] + row*cell_size[0]*3, self.pos[1] + n_cells*cell_size[1]), 2)
		for col in range(3 + 1):
			pygame.draw.line(self.screen, outer_grid_color, (self.pos[0], self.pos[1] + col*cell_size[1]*3), (self.pos[0] + n_cells*cell_size[0], self.pos[1] + col*cell_size[1]*3), 2)
	def _other_value_highlighter(self, x, y):
		for r in range(n_cells):
				for c in range(n_cells):
					if self.table_cells[r][c].value == self.selected_cell.value and not self.selected_cell.value == 0 and not (r == x and c == y):
						if r == x or c == y:
							self.table_cells[r][c].color = wrong_highlight_color
						else:
							self.table_cells[r][c].color = same_num_highlight_color

				
			