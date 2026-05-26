import math
from core.grid import CellType

class Builder:
    """
    Агент 'Конструктор' (Builder AI), отвечающий за антагонистическую генерацию уровня
    с целью максимизации сложности для агента 'Гравець'.
    """
    
    def __init__(self, grid, solver):
        """
        Инициализирует агента Конструктора.

        Args:
            grid: Экземпляр класса Grid, представляющий текущее состояние игрового поля.
            solver: Экземпляр класса Solver (например, с алгоритмом A* или Дейкстры), 
                    который будет использоваться для валидации прохождения и оценки 
                    стоимости пути.
        """
        self.grid = grid
        self.solver = solver

        # В дальнейшем сюда можно будет добавить дополнительные параметры,
        # например, ограничение глубины для алгоритма Minimax (depth limit).
    
    def evaluate(self, test_grid):
        """
        Функция оценки (Evaluation Function).
        Рассчитывает выгоду от текущего состояния сетки (например, после гипотетической 
        постановки препятствия). Цель Конструктора — максимизировать возвращаемое значение.

        Args:
            test_grid: Состояние сетки Grid для оценки.

        Returns:
            float: Оценка стоимости пути. Если путь заблокирован, возвращает -inf.
        """
        # Запрашиваем у Солвера оптимальный путь для переданного состояния сетки
        # (предполагается, что метод find_path принимает конкретную сетку для анализа)
        # (например, используются геттеры test_grid.get_start()), замени эти строки!
        # start_pos = test_grid.get_start()  
        # goal_pos = test_grid.get_goal()    
        

        # Получаем объекты ячеек старта и финиша
        start_cell = test_grid.get_start()  
        goal_cell = test_grid.get_goal() # Убедитесь, что метод называется так
        
        # Защита от краша: если старта или финиша нет, путь невозможен
        if not start_cell or not goal_cell:
            return -float('inf')
        
        # Превращаем объекты в кортежи координат (x, y)
        start_pos = (start_cell.x, start_cell.y)
        goal_pos = (goal_cell.x, goal_cell.y)


        # 2. Запрашиваем оптимальный путь, передавая КООРДИНАТЫ, а не сетку
        path = self.solver.find_path(start_pos, goal_pos)
        
        # Запрашиваем расчет стоимости/длины маршрута
        cost = self.solver.calculate_path_cost(path)
        
        # Строгая проверка на гарантированное прохождение:
        # Если пути нет или стоимость равна бесконечности, значит препятствие 
        # полностью блокирует уровень. Это недопустимо, поэтому возвращаем максимальный штраф.
        if path is None or cost == float('inf') or cost == math.inf:
            return -float('inf')
            
        # Если путь есть, возвращаем его стоимость (чем больше, тем лучше для Конструктора)
        return cost
    
    def get_best_move(self, current_grid, depth_limit):
        """
        Определяет лучшую координату для постановки препятствия.
        Запускает алгоритм Minimax для каждой доступной пустой ячейки.

        Args:
            current_grid: Текущее состояние сетки.
            depth_limit: Ограничение глубины поиска (сколько препятствий смотрим наперед).

        Returns:
            tuple: Координаты (x, y) для лучшего хода, или None, если ходов нет.
        """
        best_score = -float('inf')
        best_move = None
        
        # Предполагается, что в Grid реализован метод get_empty_cells_coords(),
        # возвращающий список кортежей [(x1, y1), (x2, y2), ...]
        empty_cells = current_grid.get_empty_cells_coords()
        
        for x, y in empty_cells:
            # 1. Симулируем ход Конструктора (MAX)
            current_grid.set_cell_type(x, y, 'OBSTACLE')
            
            # 2. Оцениваем ход с помощью Minimax 
            # (следующий ход формально за Гравцем, поэтому is_maximizing=False)
            score = self.minimax(current_grid, depth_limit - 1, False)
            
            # 3. Откатываем состояние сетки
            current_grid.set_cell_type(x, y, 'EMPTY')
            
            # 4. Выбираем ход с максимальной выгодой
            if score > best_score:
                best_score = score
                best_move = (x, y)
                
        # --- TASK 3.4: СТРОГАЯ ПРОВЕРКА ---
        # Если после перебора всех вариантов best_score остался равен бесконечно малому значению,
        # это означает, что ЛЮБОЕ добавленное препятствие блокирует путь (Solver вернул None или Infinity).
        # Чтобы уровень оставался гарантированно проходным, ход отбрасывается полностью.
        if best_score == -float('inf'):
            return None
            
        return best_move

    def minimax(self, test_grid, depth, is_maximizing, alpha=-float('inf'), beta=float('inf')):
        """
        Рекурсивный алгоритм дерева решений Minimax с ограничением глубины.

        Args:
            test_grid: Состояние сетки для оценки.
            depth: Оставшаяся глубина поиска (depth limit).
            is_maximizing: Флаг текущего агента (True для Конструктора, False для Гравця).
            alpha: Лучшее значение для максимизатора (для отсечения).
            beta: Лучшее значение для минимизатора (для отсечения).

        Returns:
            float: Минимаксная оценка ветки.
        """
        # Базовый случай: достигнуто ограничение глубины (depth limit) 
        # или на сетке больше нет свободных мест для препятствий.
        if depth == 0 or not test_grid.has_empty_cells():
            return self.evaluate(test_grid)

        if is_maximizing:
            # Ветка MAX: Агент "Конструктор" пытается максимизировать путь
            max_eval = -float('inf')
            
            for x, y in test_grid.get_empty_cells_coords():
                test_grid.set_cell_type(x, y, CellType.OBSTACLE) # Делаем гипотетический ход
                
                # Рекурсивно вызываем для следующего агента (MIN)
                eval_score = self.minimax(test_grid, depth - 1, False, alpha, beta)
                
                test_grid.set_cell_type(x, y, CellType.EMPTY) # Откатываем ход
                
                max_eval = max(max_eval, eval_score)
                
                # Альфа-бета отсечение для значительного ускорения поиска
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break # Отсекаем невыгодные ветви
                    
            return max_eval
        else:
            # Ветка MIN: Агент "Гравець" (Solver AI)
            # В нашей модели "Гравець" не меняет карту, а ищет оптимальный путь.
            # Вызов метода evaluate() уже инкапсулирует алгоритм A*, который 
            # находит минимальный путь (выполняет роль минимизатора).
            return self.evaluate(test_grid)
        
    def generate_level(self, steps: int, depth_limit: int = 2) -> int:
        """
        Запускает пошаговую расстановку препятствий Конструктором.
        Агент пытается максимизировать сложность пути для Гравця, 
        сохраняя при этом уровень гарантированно проходным.

        Args:
            steps (int): Максимальное количество препятствий, которое Конструктор попытается поставить.
            depth_limit (int): Ограничение глубины поиска для алгоритма Minimax (по умолчанию 2).

        Returns:
            int: Фактическое количество успешно расставленных препятствий.
        """
        obstacles_placed = 0
        
        for step in range(steps):
            # Запрашиваем лучшую позицию для препятствия у алгоритма Minimax
            best_move = self.get_best_move(self.grid, depth_limit)
            
            # Строгая валидация (Task 3.4): если безопасных ходов больше нет,
            # Конструктор обязан прекратить работу, чтобы уровень остался проходным.
            if best_move is None:
                # В реальном проекте здесь можно использовать модуль logging,
                # но для простоты пока оставим print для отладки.
                print(f"Генерация остановлена на шаге {step}: дальнейшая установка препятствий полностью заблокирует путь.")
                break
                
            x, y = best_move
            
            # Предполагается, что в CellType используется 'OBSTACLE' или CellType.OBSTACLE.
            # Если у тебя Enum, замени строку на CellType.OBSTACLE и добавь нужный импорт.
            self.grid.set_cell_type(x, y, 'OBSTACLE') 
            
            obstacles_placed += 1
            
        return obstacles_placed
    
    def generate_step(self, depth_limit: int = 2) -> bool:
        """
        Выполняет один шаг генерации: находит лучшую позицию и ставит одно препятствие.
        Идеально подходит для вызова внутри игрового цикла Pygame.

        Args:
            depth_limit (int): Ограничение глубины поиска для алгоритма Minimax.

        Returns:
            bool: True, если шаг выполнен (препятствие поставлено). 
                  False, если больше безопасных ходов нет и генерация завершена.
        """
        # Запрашиваем лучшую позицию для препятствия у алгоритма Minimax
        best_move = self.get_best_move(self.grid, depth_limit)
        
        # Строгая валидация: если безопасных ходов больше нет,
        # Конструктор обязан прекратить работу, чтобы уровень остался проходным.
        if best_move is None:
            return False
            
        x, y = best_move
        
        # Устанавливаем препятствие
        self.grid.set_cell_type(x, y, 'OBSTACLE') 
        
        return True