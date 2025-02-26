from itertools import islice

width, height = 500, 500
n_cells = 9
cell_size = (width // n_cells, height // n_cells)

#sudoku window padding
padding_x = 10
padding_y = 10

#color pallete
cell_color = (255, 255, 255)
cell_border_color = (220, 220, 225)
outer_grid_color = (45, 62, 84) #(60, 60, 70)
sel_cel_color = (161, 192, 217)
cell_highlight_color = (195, 203, 210)
default_font_color = outer_grid_color
added_font_color = (65, 65, 120)
wrong_font_color = (250, 160, 175)
same_num_highlight_color = (168, 185, 202)
wrong_highlight_color = (213, 179, 185)