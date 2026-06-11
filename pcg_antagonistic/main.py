import sys
import pygame

from core.grid import Grid
from core.solver import Solver
from core.astar import AStarSolver
from core.dijkstra import DijkstraSolver
from core.builder import Builder

from ui.window import GameWindow

def main(n, m):
    GRID_WIDTH = n
    GRID_HEIGHT = m
    grid = Grid(GRID_WIDTH, GRID_HEIGHT)
    
    grid.set_start(0, 0)
    grid.set_goal(GRID_WIDTH - 1, GRID_HEIGHT - 1)
    
    grid.set_interactive_object(3, 3, weight=5.0)
    grid.set_interactive_object(3, 4, weight=5.0)
    grid.set_interactive_object(3, 5, weight=5.0)
    
    grid.set_interactive_object(5, 5, weight=3.0)
    grid.set_interactive_object(6, 5, weight=3.0)
    grid.set_interactive_object(7, 8, weight=3.0)
    grid.set_interactive_object(9, 1, weight=3.0)
    grid.set_interactive_object(2, 3, weight=3.0)
    grid.set_interactive_object(8, 2, weight=3.0)
    grid.set_interactive_object(1, 7, weight=3.0)

    solver = AStarSolver(grid)
    #solver = DijkstraSolver(grid)

    builder = Builder(grid, solver)

    CELL_SIZE = 40
    WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
    WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE
    
    game_window = GameWindow(WINDOW_WIDTH, WINDOW_HEIGHT, GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)
    
    clock = pygame.time.Clock()
    FPS = 30
    
    running = True
    generation_finished = False

    solver.calculate_path()

    while running:
        actions = game_window.handle_events()
        
        if actions["quit"]:
            running = False
            break
        
        if not generation_finished and actions["next_step"]:
            generation_in_progress = builder.generate_step() 
            
            if not generation_in_progress:
                generation_finished = True
                
            solver.calculate_path()
        
        game_window.draw_grid(grid.get_data())
        
        current_path = solver.get_last_path()
        if current_path:
            game_window.draw_path(current_path)
            
        game_window.update()
        clock.tick(FPS)

    game_window.quit()

if __name__ == "__main__":
    n = 10 
    m = 10
            
    main(n, m)