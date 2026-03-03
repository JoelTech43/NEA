from Cell import Cell

class Maze:
    #__init__ method:
    #parent is object that instantiated this object, cell_array is a 2D array of lists representing each cell (3D array),
    #maze_height is a integer representing how many rows/cols the maze has,
    #cell_height is the height of each cell in pixels.
    #screen_pos is a tuple (x, y) where x and y are integers. Represents coord in screen of top left of maze.
    def __init__(self, parent, cell_array: list, maze_height: int, cell_height: int, screen_pos: tuple) -> None:
        self.__parent = parent
        self.__maze_height = maze_height
        self.__screen_pos = screen_pos
        self.__cell_height = cell_height
        self.__cells = [] #will be a 2D list of Cell objects, each inner list is a row in the maze.

        for row in range(self.__maze_height):
            new_row = [] #new list for each row
            for col in range(self.__maze_height):
                cell_screen_pos = (self.__screen_pos[0]+col*self.__cell_height, self.__screen_pos[1]+row*self.__cell_height) #calculate position of cell on screen.
                new_row.append(Cell(self, cell_array[row][col], (col, row), cell_screen_pos, self.__cell_height)) #instantiating a Cell object for each cell in the cell_array and storing it in a list for each row.
            self.__cells.append(new_row) #appending the row to the full list of cells.
    
    def draw_maze(self, canvas):
        for row in self.__cells: #go through each row.
            for cell in row: #then each cell in the row.
                cell.draw_cell(canvas) #and call the cell's draw_cell method, to draw it on the canvas.
    
    def get_screen_pos(self) -> tuple: #returns the top left screen coordinate of the maze
        return self.__screen_pos

    def get_cell(self, maze_pos: tuple) -> Cell: #returns the Cell object for the given position.
        return self.__cells[maze_pos[1]][maze_pos[0]]
    
    def get_cells(self) -> list: #returns the 2D list of Cell objects representing the maze.
        return self.__cells
    
    def get_cell_height(self) -> int: #returns the height/width of each cell in pixels.
        return self.__cell_height
    
    def get_maze_height(self) -> int:
        return self.__maze_height
