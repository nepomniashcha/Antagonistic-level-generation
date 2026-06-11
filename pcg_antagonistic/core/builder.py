import math
import random
from core.grid import CellType

class Builder:
    def __init__(self, grid, solver):
        self.grid = grid
        self.solver = solver
    
    def evaluate(self, test_grid):
        start_cell = test_grid.get_start()  
        goal_cell = test_grid.get_goal()
        
        if not start_cell or not goal_cell:
            return -float('inf')
        
        start_pos = (start_cell.x, start_cell.y)
        goal_pos = (goal_cell.x, goal_cell.y)

        path = self.solver.find_path(start_pos, goal_pos)
        cost = self.solver.calculate_path_cost(path)
        
        if path is None or cost == float('inf') or cost == math.inf:
            return -float('inf')
            
        return cost
    
    def get_best_move(self, current_grid, depth_limit):
        best_score = -float('inf')
        best_moves = []
        
        empty_cells = current_grid.get_empty_cells_coords()
        
        for x, y in empty_cells:
            current_grid.set_cell_type(x, y, CellType.OBSTACLE) 
            score = self.minimax(current_grid, depth_limit - 1, False)
            current_grid.set_cell_type(x, y, CellType.EMPTY) 
            
            if score > best_score:
                best_score = score
                best_moves = [(x, y)]
            elif score == best_score:
                best_moves.append((x, y))
                
        if best_score == -float('inf') or not best_moves:
            return None
            
        return random.choice(best_moves)

    def minimax(self, test_grid, depth, is_maximizing, alpha=-float('inf'), beta=float('inf')):
        if depth == 0 or not test_grid.has_empty_cells():
            return self.evaluate(test_grid)

        if is_maximizing:
            max_eval = -float('inf')
            
            for x, y in test_grid.get_empty_cells_coords():
                test_grid.set_cell_type(x, y, CellType.OBSTACLE)
                eval_score = self.minimax(test_grid, depth - 1, False, alpha, beta)
                test_grid.set_cell_type(x, y, CellType.EMPTY) 
                max_eval = max(max_eval, eval_score)
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break 
                    
            return max_eval
        else:
            return self.evaluate(test_grid)
        
    def generate_level(self, steps: int, depth_limit: int = 2) -> int:
        obstacles_placed = 0
        
        for step in range(steps):
            best_move = self.get_best_move(self.grid, depth_limit)
            
            if best_move is None:
                break
                
            x, y = best_move
            self.grid.set_cell_type(x, y, CellType.OBSTACLE)
            obstacles_placed += 1
            
        return obstacles_placed
    
    def generate_step(self, depth_limit: int = 2) -> bool:
        best_move = self.get_best_move(self.grid, depth_limit)
        
        if best_move is None:
            return False
            
        x, y = best_move
        self.grid.set_cell_type(x, y, CellType.OBSTACLE) 
        
        return True