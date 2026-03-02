from Maze import Maze
from Entity import Player
import pygame

class LevelHandler:
    def __init__(self, parent, canvas, level_id: int) -> None:
        self.parent = parent
        self.canvas = canvas
        self.level_id = level_id

        #would load maze info from file here, just using test data for now.
        maze_info = {
            "height": 10,
            "width": 10,
            "player": [4, 0],
            "finish": [5, 9],
            "enemies": [[7, 8],[4, 5],[2, 3],[7, 3]],
            "maze": [
                [[True, True, False, False],[False, True, False, False],[False, True, False, True],[False, True, True, True],[True, True, False, False],[False, True, False, True],[False, True, False, True],[False, True, True, False],[True, True, False, True],[False, True, True, False]],
                [[True, False, True, False],[True, False, False, True],[False, True, False, True],[False, True, True, False],[True, False, False, True],[False, True, True, False],[True, True, False, False],[False, False, True, True],[True, True, False, False],[False, False, True, False]],
                [[True, False, False, True],[False, True, False, False],[False, True, True, False],[True, False, True, False],[True, True, False, False],[False, False, True, True],[True, False, False, True],[False, True, False, True],[False, False, True, True],[True, False, True, False]],
                [[True, True, False, False],[False, False, True, True],[True, False, True, True],[True, False, False, True],[False, False, True, True],[True, True, False, False],[False, True, False, True],[False, True, False, True],[False, True, True, True],[True, False, True, False]],
                [[True, False, False, True],[False, True, False, False],[False, True, True, False],[True, True, False, False],[False, True, True, False],[True, False, False, True],[False, True, False, False],[False, True, False, True],[False, True, False, True],[False, False, True, True]],
                [[True, True, False, False],[False, False, True, True],[True, False, False, True],[False, False, True, True],[True, False, True, False],[True, True, False, False],[False, False, True, True],[True, True, False, True],[False, True, False, True],[False, True, True, False]],
                [[True, False, True, False],[True, True, False, True],[False, True, False, True],[False, True, False, True],[False, False, True, True],[True, False, False, True],[False, True, False, True],[False, True, False, True],[False, True, True, False],[True, False, True, False]],
                [[True, False, True, False],[True, True, False, False],[False, True, False, True],[False, True, True, False],[True, True, False, False],[False, True, True, False],[True, True, True, False],[True, True, False, False],[False, False, False, True],[False, False, True, True]],
                [[True, False, True, False],[True, False, True, False],[True, True, False, False],[False, False, True, True],[True, False, True, False],[True, False, True, False],[True, False, True, False],[True, False, False, False],[False, True, True, False],[True, True, True, False]],
                [[True, False, False, True],[False, False, True, True],[True, False, False, True],[False, True, False, True],[False, False, True, True],[True, False, True, True],[True, False, False, True],[False, False, True, True],[True, False, False, True],[False, False, True, True]]
                ]
        }

        self.CELL_HEIGHT = self.parent.MAZE_HEIGHT//maze_info["height"] #calculates cell height based on maze height.
        self.maze = Maze(self, maze_info["maze"], maze_info["height"], self.CELL_HEIGHT, self.parent.MAZE_SCREEN_POS)
        self.player = Player(self, 1, maze_info["player"], self.CELL_HEIGHT)
    
    def level_loop(self):
        exit = False
        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #if user clicks close button, set exit to True to escape game loop, closing program.
                    exit = True
                    self.parent.save_and_quit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_l, pygame.K_LEFT):
                        self.player.enter_move((-1,0))
                    elif event.key in (pygame.K_w, pygame.K_UP):
                        self.player.enter_move((0,-1))
                    elif event.key in (pygame.K_d, pygame.K_RIGHT):
                        self.player.enter_move((1,0))
                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        self.player.enter_move((0,1))
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.player.move_player()
            self.maze.draw_maze(self.canvas)
            self.player.draw_entity(self.canvas)
            pygame.display.update() #updates the window with any changes. None at the moment.

    def process_inputs(self):
        pass

    def user_move(self):
        pass

    def enemy_move(self):
        pass

    def pause(self):
        pass

    def game_over(self):
        pass

    def game_win(self):
        pass