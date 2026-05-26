import heapq
from typing import List, Tuple, Optional
from core.solver import Solver

class AStarSolver(Solver):
    """
    Агент 'Гравець', реализующий алгоритм поиска пути A* (A-Star).
    Наследуется от базового класса Solver.
    """

    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """
        Эвристическая функция: Манхэттенское расстояние.
        Оптимально для сетки, где движение разрешено только по вертикали и горизонтали.
        
        Формула: h(n) = |x1 - x2| + |y1 - y2|
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Основной метод поиска оптимального пути.
        """
        # Очередь с приоритетом для хранения открытых узлов (f_score, (x, y))
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        # Словарь для восстановления итогового пути
        came_from = {}
        
        # g_score: стоимость пути от старта до текущего узла
        g_score = {start: 0}
        
        # f_score: g_score + эвристика (примерная общая стоимость)
        f_score = {start: self._heuristic(start, goal)}
        
        # Множество для быстрого поиска элементов в очереди
        open_set_hash = {start}

        while open_set:
            # Извлекаем узел с наименьшим f_score
            current_f, current = heapq.heappop(open_set)
            open_set_hash.remove(current)
            
            # Если достигли цели, восстанавливаем и возвращаем путь
            if current == goal:
                return self._reconstruct_path(came_from, current)
            
            # Получаем соседей через интерфейс Grid (Task 1.3)
            # for neighbor in self.grid.get_neighbors(current):
            #     # Предполагаем, что базовый шаг стоит 1. 
            #     # Если реализован Task 1.4 (веса ячеек), здесь нужно брать вес из grid.
            #     tentative_g_score = g_score[current] + 1 
                
            #     # Если нашли более короткий путь до соседа
            #     if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
            #         came_from[neighbor] = current
            #         g_score[neighbor] = tentative_g_score
            #         f_score[neighbor] = tentative_g_score + self._heuristic(neighbor, goal)
                    
            #         if neighbor not in open_set_hash:
            #             heapq.heappush(open_set, (f_score[neighbor], neighbor))
            #             open_set_hash.add(neighbor)
            # Получаем соседей (объекты Cell)
            for cell_neighbor in self.grid.get_neighbors(current):
                
                # ПРЕВРАЩАЕМ ОБЪЕКТ В КОРТЕЖ КООРДИНАТ
                neighbor = (cell_neighbor.x, cell_neighbor.y)
                
                # Дальше ваш код остается абсолютно без изменений!
                tentative_g_score = g_score[current] + 1 
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self._heuristic(neighbor, goal)
                    
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)
                        
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
