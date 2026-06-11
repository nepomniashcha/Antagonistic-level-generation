import heapq
from typing import List, Tuple, Optional
from core.solver import Solver

class DijkstraSolver(Solver):
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        came_from = {}
        
        cost_so_far = {start: 0}

        while open_set:
            current_cost, current = heapq.heappop(open_set)
            
            if current == goal:
                return self._reconstruct_path(came_from, current)
            
            for neighbor in self.grid.get_neighbors(current):
                move_cost = self.grid.get_cell_weight(neighbor[0], neighbor[1])
                new_cost = cost_so_far[current] + move_cost 

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(open_set, (new_cost, neighbor))
                    came_from[neighbor] = current
                        
        return None

    def _reconstruct_path(self, came_from: dict, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path