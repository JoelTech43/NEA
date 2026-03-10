from Cell import Cell
import pygame

class Maze:
    #__init__ method:
    #parent is object that instantiated this object, cell_array is a 2D array of lists representing each cell (3D array),
    #maze_height is a integer representing how many rows/cols the maze has,
    #cell_height is the height of each cell in pixels.
    #screen_pos is a tuple (x, y) where x and y are integers. Represents coord in screen of top left of maze.
    def __init__(self, parent, cell_array: list, maze_height: int, cell_height: int, screen_pos: tuple, finish_coord: tuple) -> None:
        self.__parent = parent
        self.__maze_height = maze_height
        self.__screen_pos = screen_pos
        self.__cell_height = cell_height
        self.__finish_coord = finish_coord
        self.__cells = [] #will be a 2D list of Cell objects, each inner list is a row in the maze.

        for row in range(self.__maze_height):
            new_row = [] #new list for each row
            for col in range(self.__maze_height):
                cell_screen_pos = (self.__screen_pos[0]+col*self.__cell_height, self.__screen_pos[1]+row*self.__cell_height) #calculate position of cell on screen.
                new_row.append(Cell(self, cell_array[row][col], (col, row), cell_screen_pos, self.__cell_height)) #instantiating a Cell object for each cell in the cell_array and storing it in a list for each row.
            self.__cells.append(new_row) #appending the row to the full list of cells.
    
    #draw_maze() - calls each cell's draw_cell method before drawing the finish square.
    def draw_maze(self, canvas):
        for row in self.__cells: #go through each row.
            for cell in row: #then each cell in the row.
                cell.draw_cell(canvas) #and call the cell's draw_cell method, to draw it on the canvas.
        
        #draw finish square
        finish_cell_screen_x = self.__screen_pos[0]+(self.__cell_height*self.__finish_coord[0])+1 #define the position of the top left corner of the finish square on the screen.
        finish_cell_screen_y = self.__screen_pos[1]+(self.__cell_height*self.__finish_coord[1])+1
        pygame.draw.rect(canvas, (0,0,255), (finish_cell_screen_x, finish_cell_screen_y, self.__cell_height-2, self.__cell_height-2))
    
    #get_screen_pos() - returns the top left screen coordinate of the maze
    def get_screen_pos(self) -> tuple:
        return self.__screen_pos

    #get_cell() - returns the Cell object for the given position.
    #maze_pos is a tuple representing a cell's coordinate in the maze.
    def get_cell(self, maze_pos: tuple) -> Cell:
        return self.__cells[maze_pos[1]][maze_pos[0]]
    
    #get_cells() - returns the 2D list of Cell objects representing the maze.
    def get_cells(self) -> list:
        return self.__cells
    
    #get_cell_height() - returns the height/width of each cell in pixels.
    def get_cell_height(self) -> int:
        return self.__cell_height
    
    #get_maze_height() - returns the height/width of the maze in terms of cells.
    def get_maze_height(self) -> int:
        return self.__maze_height

    #get_finish_coord() - returns a tuple representing the coord in the maze of the finish square.
    def get_finish_coord(self) -> tuple:
        return self.__finish_coord
    
    #reset_cell_estimates() - calls each cell's reset_estimates() method.
    def reset_cell_estimates(self):
        for row in self.__cells:
            for cell in row:
                cell.reset_estimates()