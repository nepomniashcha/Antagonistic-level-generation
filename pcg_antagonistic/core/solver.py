from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from core.grid import Grid

class Solver(ABC):
    """
    Абстрактный базовый класс для агента 'Гравець' (Solver AI).
    Определяет интерфейс для алгоритмов поиска пути на дискретной сетке.
    """

    def __init__(self, grid):
        """
        Инициализация агента поиска пути.

        Args:
            grid (Grid): Объект сетки игрового поля, содержащий данные 
                         о препятствиях, стоимости ячеек и их типах.
        """
        self.grid = grid

    @abstractmethod
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Абстрактный метод поиска оптимального пути.
        Должен быть переопределен в классах-наследниках (A*, Dijkstra).

        Args:
            start: Координаты точки старта в формате (x, y).
            goal: Координаты целевой точки в формате (x, y).

        Returns:
            Список координат [(x1, y1), (x2, y2), ...], представляющий найденный путь.
            Если путь не найден, должен возвращать None.
        """
        pass

    def calculate_path_cost(self, path: Optional[List[Tuple[int, int]]]) -> float:
        """
        Анализ пути: возвращает числовую оценку сложности/длины найденного маршрута.

        Args:
            path: Найденный путь (список координат) или None.

        Returns:
            Числовая оценка стоимости пути (float). 
            Если пути нет, возвращается бесконечность (Infinity) float('inf').
        """
        # Если пути не существует, возвращаем Infinity, как указано в задании
        if path is None:
            return float('inf')

        cost = 0.0
        # Если путь состоит только из стартовой точки (старт совпадает с целью), сложность равна 0
        if len(path) <= 1:
            return cost

        # Проходим по всем координатам пути, начиная со второго шага (индекс 1),
        # так как мы уже стоим на стартовой ячейке и не платим за вход в нее.
        for i in range(1, len(path)):
            x, y = path[i]
            
            # Если в классе Grid (Task 1.4) реализован метод получения веса ячейки, используем его.
            # В противном случае базовая стоимость шага равна 1.0.
            if hasattr(self.grid, 'get_cell_weight'):
                cell_cost = self.grid.get_cell_weight(x, y)
            else:
                cell_cost = 1.0 
                
            cost += cell_cost

        return cost
    
    def calculate_path(self):
        """Обертка для вызова поиска пути с текущими настройками старта и финиша"""
        start = self.grid.get_start()
        goal = self.grid.get_goal()
        self._last_path = self.find_path(start, goal)
        pass 

    def get_last_path(self) -> Optional[List[Tuple[int, int]]]:
        """Возвращает последний найденный путь"""
        return self._last_path