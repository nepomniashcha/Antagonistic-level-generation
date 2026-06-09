import sys
import pygame

from core.grid import Grid
from core.solver import Solver
from core.astar import AStarSolver
from core.dijkstra import DijkstraSolver
from core.builder import Builder

from ui.window import GameWindow

def main(n, m):
    # --- 1. Логика инициализации приложения и структур данных ---
    # Задаем размеры дискретной сетки игрового поля
    GRID_WIDTH = n
    GRID_HEIGHT = m
    
    # Экземпляризация Grid (Сетка)
    grid = Grid(GRID_WIDTH, GRID_HEIGHT)
    
    # Установка стартовой и целевой точек для агентов
    grid.set_start(0, 0)
    grid.set_goal(GRID_WIDTH - 1, GRID_HEIGHT - 1)

    # Обычная пустая клетка стоит 1.0.
    # Давайте добавим "болото" со стоимостью 5.0 на пути алгоритма.
    
    grid.set_interactive_object(3, 3, weight=5.0)
    grid.set_interactive_object(3, 4, weight=5.0)
    grid.set_interactive_object(3, 5, weight=5.0)
    
    # А здесь добавим "густой лес" со стоимостью 3.0
    grid.set_interactive_object(5, 5, weight=3.0)
    grid.set_interactive_object(6, 5, weight=3.0)
    grid.set_interactive_object(7, 8, weight=3.0)
    grid.set_interactive_object(9, 1, weight=3.0)
    grid.set_interactive_object(2, 3, weight=3.0)
    grid.set_interactive_object(8, 2, weight=3.0)
    grid.set_interactive_object(1, 7, weight=3.0)

    # --- 2. Экземпляризация Solver (Агент "Гравець" / A*) ---
    # Передаем сетку солверу, чтобы он мог выполнять по ней поиск пути
    # было solver = Solver(grid)
    solver = AStarSolver(grid)
    #solver = DijkstraSolver(grid)

    # --- 3. Экземпляризация Builder (Агент "Конструктор" / Minimax) ---
    # Конструктору нужна сетка для расстановки препятствий и Solver для оценки их влияния (целевая функция)
    builder = Builder(grid, solver)

    # --- 4. Экземпляризация GameWindow (Графический интерфейс) ---
    # Задаем размеры окна в пикселях
    CELL_SIZE = 40 # Ви можете змінити це значення (наприклад, 30, 50)
    
    # Розміри вікна тепер обчислюються автоматично на основі кількості комірок
    WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
    WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE
    
    # Инициализируем окно, передавая ему необходимые параметры для отрисовки
    game_window = GameWindow(WINDOW_WIDTH, WINDOW_HEIGHT, GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)
    
    # --- 5. Налаштування ігрового циклу (Task 5.2) ---
    clock = pygame.time.Clock()
    FPS = 30
    
    running = True
    generation_finished = False

    # Первоначальный поиск пути для старта
    solver.calculate_path()

    while running:
        # 5.2.1 Обробка подій
        # ПРАВИЛЬНО ИЗВЛЕКАЕМ СЛОВАРЬ
        actions = game_window.handle_events()
        
        if actions["quit"]:
            running = False
            break
        
        # 5.2.2 Оновлення стану генерації
        # Запускаем генерацию ТОЛЬКО если нажат ПРОБЕЛ (или если хотите автоматически, уберите and actions["next_step"])
        if not generation_finished and actions["next_step"]:
            generation_in_progress = builder.generate_step() 
            
            if not generation_in_progress:
                generation_finished = True
                print("Генерацію рівня завершено. Уровень полностью застроен.")
                
            # Після зміни сітки Конструктором, просимо Гравця знайти новий оптимальний шлях
            solver.calculate_path()
        
        # 5.2.3 Отримання даних сітки та передача у GameWindow
        game_window.draw_grid(grid.get_data())
        
        # 5.2.4 Передача та відмальовування знайденого шляху
        current_path = solver.get_last_path()
        if current_path:
            game_window.draw_path(current_path)
            
        # 5.2.5 Оновлення екрану
        game_window.update()
        
        # Контроль частоти кадрів
        clock.tick(FPS)

    game_window.quit() # Корректное закрытие окна

if __name__ == "__main__":
    n = 10 
    m = 10
            
    main(n, m)