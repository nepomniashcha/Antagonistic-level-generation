from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from core.grid import Grid

class Solver(ABC):
    def __init__(self, grid):
        self.grid = grid

    @abstractmethod
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        pass

    def calculate_path_cost(self, path: Optional[List[Tuple[int, int]]]) -> float:
        if path is None:
            return float('inf')

        cost = 0.0
        if len(path) <= 1:
            return cost

        for i in range(1, len(path)):
            x, y = path[i]
            
            if hasattr(self.grid, 'get_cell_weight'):
                cell_cost = self.grid.get_cell_weight(x, y)
            else:
                cell_cost = 1.0 
                
            cost += cell_cost

        return cost
    
    def calculate_path(self):
        start_cell = self.grid.get_start()
        goal_cell = self.grid.get_goal()
        
        if start_cell and goal_cell:
            start_pos = (start_cell.x, start_cell.y)
            goal_pos = (goal_cell.x, goal_cell.y)
            self._last_path = self.find_path(start_pos, goal_pos)
        else:
            self._last_path = None

    def get_last_path(self) -> Optional[List[Tuple[int, int]]]:
        return self._last_path