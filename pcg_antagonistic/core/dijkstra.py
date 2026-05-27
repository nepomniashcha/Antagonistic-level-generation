import heapq
from typing import List, Tuple, Optional
from core.solver import Solver

class DijkstraSolver(Solver):
    """
    Агент 'Гравець', реализующий классический алгоритм Дейкстры.
    Наследуется от базового класса Solver.
    Не использует эвристику для поиска пути.
    """

    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Основной метод поиска оптимального пути алгоритмом Дейкстры.
        """
        # Очередь с приоритетом для хранения открытых узлов (cost, (x, y))
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        # Словарь для восстановления итогового пути
        came_from = {}
        
        # Словарь накопленной стоимости пути от старта до конкретного узла
        cost_so_far = {start: 0}

        while open_set:
            # Извлекаем узел с наименьшей накопленной стоимостью
            current_cost, current = heapq.heappop(open_set)
            
            # Если достигли цели, восстанавливаем и возвращаем путь
            if current == goal:
                return self._reconstruct_path(came_from, current)
            
            # Получаем соседние доступные ячейки через интерфейс Grid (Task 1.3)
            for neighbor in self.grid.get_neighbors(current):
                # В базовом варианте стоимость перехода равна 1.
                # Если в Task 1.4 реализованы веса ячеек, здесь нужно брать вес из grid.
                new_cost = cost_so_far[current] + 1 
                
                # Если сосед еще не посещен или найден более дешевый путь к нему
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    # Добавляем в очередь с приоритетом (эвристики нет, приоритет = new_cost)
                    heapq.heappush(open_set, (new_cost, neighbor))
                    came_from[neighbor] = current
                        
        # Если очередь пуста, а цель не достигнута — пути не существует
        return None

    def _reconstruct_path(self, came_from: dict, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Вспомогательный метод для восстановления пути от финиша к старту.
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse() # Разворачиваем, чтобы путь шел от старта к цели
        return path