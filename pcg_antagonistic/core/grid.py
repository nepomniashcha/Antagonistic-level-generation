from enum import Enum
from dataclasses import dataclass
from typing import Tuple, List 

class CellType(Enum):
    EMPTY = 0
    OBSTACLE = 1
    START = 2
    GOAL = 3
    INTERACTIVE = 4

@dataclass(unsafe_hash=True)
class Cell:
    x: int
    y: int
    type: CellType = CellType.EMPTY
    weight: float = 1.0

    def is_passable(self) -> bool:
        return self.type != CellType.OBSTACLE
    
    
    def get_cost(self) -> float:
        if self.type == CellType.INTERACTIVE:
            return self.weight
        return 1.0  # для EMPTY, START, GOAL

class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]

    def _is_within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int) -> Cell | None:
        if self._is_within_bounds(x, y):
            return self.grid[x][y]
        return None

    def set_cell_type(self, x: int, y: int, cell_type: CellType) -> None:
        if self._is_within_bounds(x, y):
            self.grid[x][y].type = cell_type
        else:
            raise IndexError(f"Coordinates ({x}, {y}) are out of grid {self.width}x{self.height}.")

    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        neighbors = []
        x, y = pos

        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if self._is_within_bounds(nx, ny):
                neighbor_cell = self.grid[nx][ny]
                
                if neighbor_cell.is_passable():
                    neighbors.append((nx, ny))

        return neighbors

    def set_start(self, x: int, y: int) -> None:
        old_start = self.get_start()
        if old_start:
            old_start.type = CellType.EMPTY
            
        self.set_cell_type(x, y, CellType.START)

    def get_start(self) -> Cell | None:
        for row in self.grid:
            for cell in row:
                if cell.type == CellType.START:
                    return cell
        return None

    def set_goal(self, x: int, y: int) -> None:
        old_goal = self.get_goal()
        if old_goal:
            old_goal.type = CellType.EMPTY
            
        self.set_cell_type(x, y, CellType.GOAL)

    def get_goal(self) -> Cell | None:
        for row in self.grid:
            for cell in row:
                if cell.type == CellType.GOAL:
                    return cell
        return None
    
    def get_cell_weight(self, x: int, y: int) -> float:
        cell = self.get_cell(x, y)
        if cell:
            return cell.get_cost()
        return float('inf')
        
    def set_interactive_object(self, x: int, y: int, weight: float) -> None:
        if self._is_within_bounds(x, y):
            cell = self.grid[x][y]
            cell.type = CellType.INTERACTIVE
            cell.weight = weight
        else:
            raise IndexError(f"Coordinates ({x}, {y}) are out of grid {self.width}x{self.height}.")

    def get_empty_cells_coords(self) -> list[tuple[int, int]]:
        empty_cells = []
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].type == CellType.EMPTY:
                    empty_cells.append((x, y))
        return empty_cells

    def has_empty_cells(self) -> bool:
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].type == CellType.EMPTY:
                    return True
        return False
    
    def get_data(self) -> list[list[Cell]]:
        return [[self.grid[x][y] for x in range(self.width)] for y in range(self.height)]