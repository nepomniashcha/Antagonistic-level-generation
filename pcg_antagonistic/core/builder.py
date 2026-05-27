import math
import random
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
        best_score = -float('inf')
        best_moves = [] # Теперь храним список всех равноценных лучших ходов
        
        empty_cells = current_grid.get_empty_cells_coords()
        
        for x, y in empty_cells:
            current_grid.set_cell_type(x, y, CellType.OBSTACLE) 
            score = self.minimax(current_grid, depth_limit - 1, False)
            current_grid.set_cell_type(x, y, CellType.EMPTY) 
            
            # Если нашли ход ЛУЧШЕ, очищаем список и начинаем заново
            if score > best_score:
                best_score = score
                best_moves = [(x, y)]
            # Если нашли ход ТАКОЙ ЖЕ хороший, добавляем его в копилку
            elif score == best_score:
                best_moves.append((x, y))
                
        # --- TASK 3.4: СТРОГАЯ ПРОВЕРКА ---
        if best_score == -float('inf') or not best_moves:
            return None
            
        # Случайно выбираем один из равноценных лучших ходов
        return random.choice(best_moves)

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
                print(f"Генерация остановлена на шаге {step}: дальнейшая установка препятствий полностью заблокирует путь.")
                break
                
            x, y = best_move
            self.grid.set_cell_type(x, y, CellType.OBSTACLE)
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
        self.grid.set_cell_type(x, y, CellType.OBSTACLE) 
        
        return True