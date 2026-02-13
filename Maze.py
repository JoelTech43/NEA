from Cell import Cell

class Maze:
    #__init__ method:
    #parent is object that instantiated this object, cells is a list of Cell objects,
    #maze_dimensions is a tuple of (width, height) where width and height are integers,
    #cell_height is the height of each cell in pixels.
    def __init__(self, parent, cell_array: list, maze_dimensions: tuple, cell_height: int) -> None:
        self.parent = parent
        self.maze_dimensions = maze_dimensions
        self.cell_height = cell_height
        self.cells = [] #will be a 2D list of Cell objects, each inner list is a row in the maze.

        for row in range(self.maze_dimensions[1]):
            new_row = [] #new list for each row
            for col in range(self.maze_dimensions[0]):
                new_row.append(Cell(self, cell_array[row][col], (col, row))) #instantiating a Cell object for each cell in the cell_array, and storing it in the list for that row.
            self.cells.append(new_row) #appending the row to the full list of cells.
    
    def draw_maze(self, canvas):
        ...
    
    def get_cell(self, maze_pos: tuple) -> Cell: #returns the Cell object for the given position.
        return self.cells[maze_pos[1]][maze_pos[0]]
    
    def get_cells(self) -> list: #returns the 2D list of Cell objects representing the maze.
        return self.cells
    
    def get_cell_height(self) -> int: #returns the height/width of each cell in pixels.
        return self.cell_height
