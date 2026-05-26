from enum import Enum
from dataclasses import dataclass
from typing import Tuple, List 

class CellType(Enum):
    """Перечисление возможных типов ячейки на сетке."""
    EMPTY = 0
    OBSTACLE = 1
    START = 2
    GOAL = 3
    INTERACTIVE = 4

@dataclass(unsafe_hash=True)
class Cell:
    """
    Класс ячейки, хранящий координаты (x, y) и её текущий тип.
    По умолчанию ячейка инициализируется как пустая (EMPTY).
    """
    x: int
    y: int
    type: CellType = CellType.EMPTY

    def is_passable(self) -> bool:
        """Вспомогательный метод: проверяет, можно ли пройти через ячейку."""
        return self.type != CellType.OBSTACLE
    
    
    # def get_cost(self) -> float:
    #     """
    #     Возвращает стоимость перехода в данную ячейку.
    #     Для интерактивных объектов возвращается их индивидуальный вес.
    #     """
    #     if self.type == CellType.INTERACTIVE:
    #         return self.weight
    #     return 1.0  # Базовая стоимость для EMPTY, START, GOAL

class Grid:
    """
    Класс, представляющий игровое поле в виде двумерного массива ячеек.
    """
    def __init__(self, width: int, height: int):
        """
        Инициализирует сетку заданного размера (width, height).
        По умолчанию все ячейки создаются с типом CellType.EMPTY.
        """
        self.width = width
        self.height = height
        # Генерация двумерного массива (список списков) объектов Cell
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]

    def _is_within_bounds(self, x: int, y: int) -> bool:
        """
        Внутренний вспомогательный метод для проверки, 
        находятся ли координаты в пределах сетки.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int) -> Cell | None:
        """
        Возвращает объект ячейки по координатам (x, y).
        Если координаты выходят за границы, возвращает None.
        """
        if self._is_within_bounds(x, y):
            return self.grid[x][y]
        return None

    def set_cell_type(self, x: int, y: int, cell_type: CellType) -> None:
        """
        Устанавливает новый тип (CellType) для ячейки по заданным координатам.
        Вызывает ошибку, если координаты выходят за пределы поля.
        """
        if self._is_within_bounds(x, y):
            self.grid[x][y].type = cell_type
        else:
            raise IndexError(f"Координаты ({x}, {y}) находятся вне границ сетки размером {self.width}x{self.height}.")
    
    # def get_neighbors(self, cell: Cell) -> list[Cell]:
    #     """
    #     Возвращает список соседних доступных (проходимых) ячеек.
    #     В данной реализации диагональные перемещения отключены.
    #     """
    #     neighbors = []
    #     x, y = cell.x, cell.y

    #     # Соседние клетки по вертикали и горизонтали (вверх, вправо, вниз, влево)
    #     directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    #     # Диагональные соседи (закомментированы по условию задачи)
    #     # diagonal_directions = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    #     # directions.extend(diagonal_directions)

    #     for dx, dy in directions:
    #         nx, ny = x + dx, y + dy
            
    #         # Проверяем, не выходит ли сосед за границы поля
    #         if self._is_within_bounds(nx, ny):
    #             neighbor_cell = self.grid[nx][ny]
                
    #             # Добавляем в список только проходимые ячейки (не препятствия)
    #             if neighbor_cell.is_passable():
    #                 neighbors.append(neighbor_cell)

    #     return neighbors



    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Возвращает список координат (x, y) соседних доступных (проходимых) ячеек.
        В данной реализации диагональные перемещения отключены.
        """
        neighbors = []
        x, y = pos # Распаковываем переданный кортеж

        # Соседние клетки по вертикали и горизонтали (вверх, вправо, вниз, влево)
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        # Диагональные соседи (закомментированы по условию задачи)
        # diagonal_directions = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        # directions.extend(diagonal_directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Проверяем, не выходит ли сосед за границы поля
            if self._is_within_bounds(nx, ny):
                neighbor_cell = self.grid[nx][ny]
                
                # Добавляем в список только проходимые ячейки (не препятствия)
                if neighbor_cell.is_passable():
                    # ВАЖНО: Возвращаем кортежи координат, а не объекты Cell!
                    neighbors.append((nx, ny))

        return neighbors

    def set_start(self, x: int, y: int) -> None:
        """Устанавливает точку старта."""
        # Очищаем предыдущий старт, если он был
        old_start = self.get_start()
        if old_start:
            old_start.type = CellType.EMPTY
            
        self.set_cell_type(x, y, CellType.START)

    def get_start(self) -> Cell | None:
        """Ищет и возвращает ячейку старта."""
        for row in self.grid:
            for cell in row:
                if cell.type == CellType.START:
                    return cell
        return None

    def set_goal(self, x: int, y: int) -> None:
        """Устанавливает точку финиша (цель)."""
        # Очищаем предыдущий финиш, если он был
        old_goal = self.get_goal()
        if old_goal:
            old_goal.type = CellType.EMPTY
            
        self.set_cell_type(x, y, CellType.GOAL)

    def get_goal(self) -> Cell | None:
        """Ищет и возвращает ячейку финиша."""
        for row in self.grid:
            for cell in row:
                if cell.type == CellType.GOAL:
                    return cell
        return None
    
    # def set_interactive_object(self, x: int, y: int, weight: float) -> None:
    #     """
    #     Превращает ячейку в интерактивный объект и задает стоимость (вес) её прохождения.
    #     Чем выше вес, тем менее охотно алгоритмы поиска пути будут через неё проходить.
    #     """
    #     if self._is_within_bounds(x, y):
    #         cell = self.grid[x][y]
    #         cell.type = CellType.INTERACTIVE
    #         cell.weight = weight
    #     else:
    #         raise IndexError(f"Координаты ({x}, {y}) находятся вне границ сетки размером {self.width}x{self.height}.")

    def get_empty_cells_coords(self) -> list[tuple[int, int]]:
        """
        Возвращает список координат (x, y) всех пустых ячеек на сетке.
        Используется агентом 'Конструктор' для поиска возможных мест постановки препятствий.
        """
        empty_cells = []
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].type == CellType.EMPTY:
                    empty_cells.append((x, y))
        return empty_cells

    def has_empty_cells(self) -> bool:
        """
        Проверяет, есть ли на сетке хотя бы одна пустая ячейка.
        Полезно для базовых случаев выхода из рекурсии (например, в Minimax).
        """
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].type == CellType.EMPTY:
                    return True
        return False