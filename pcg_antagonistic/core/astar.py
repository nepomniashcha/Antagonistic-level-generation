import heapq
from typing import List, Tuple, Optional
from core.solver import Solver

class AStarSolver(Solver):
    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        came_from = {}

        g_score = {start: 0}
        f_score = {start: self._heuristic(start, goal)}
        
        open_set_hash = {start}

        while open_set:
            current_f, current = heapq.heappop(open_set)
            open_set_hash.remove(current)
            
            if current == goal:
                return self._reconstruct_path(came_from, current)

            for neighbor in self.grid.get_neighbors(current):
                move_cost = self.grid.get_cell_weight(neighbor[0], neighbor[1])
                tentative_g_score = g_score[current] + move_cost 
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self._heuristic(neighbor, goal)
                    
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)
                        
        return None

    def _reconstruct_path(self, came_from: dict, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path