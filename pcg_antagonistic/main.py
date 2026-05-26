import sys
import pygame

# Импорты модулей ядра (Core), содержащих бизнес-логику и агентов
from core.grid import Grid
from core.solver import Solver
from core.astar import AStarSolver
from core.builder import Builder

# Импорт модуля графического интерфейса (UI)
from ui.window import GameWindow

def main():
    # --- 1. Логика инициализации приложения и структур данных ---
    # Задаем размеры дискретной сетки игрового поля
    GRID_WIDTH = 20
    GRID_HEIGHT = 20
    
    # Экземпляризация Grid (Сетка)
    grid = Grid(GRID_WIDTH, GRID_HEIGHT)
    
    # Установка стартовой и целевой точек для агентов
    grid.set_start(0, 0)
    grid.set_goal(GRID_WIDTH - 1, GRID_HEIGHT - 1)

    # --- 2. Экземпляризация Solver (Агент "Гравець" / A*) ---
    # Передаем сетку солверу, чтобы он мог выполнять по ней поиск пути
    # было solver = Solver(grid)
    solver = AStarSolver(grid)

    # --- 3. Экземпляризация Builder (Агент "Конструктор" / Minimax) ---
    # Конструктору нужна сетка для расстановки препятствий и Solver для оценки их влияния (целевая функция)
    builder = Builder(grid, solver)

    # --- 4. Экземпляризация GameWindow (Графический интерфейс) ---
    # Задаем размеры окна в пикселях
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 800
    
    # Инициализируем окно, передавая ему необходимые параметры для отрисовки
    game_window = GameWindow(WINDOW_WIDTH, WINDOW_HEIGHT, GRID_WIDTH, GRID_HEIGHT)

    # --- 5. Налаштування ігрового циклу (Task 5.2) ---
    clock = pygame.time.Clock()
    FPS = 30 # Обмеження кадрів в секунду для плавності візуалізації
    
    running = True
    generation_finished = False

    while running:
        # 5.2.1 Обробка подій (закриття вікна, натискання клавіш)
        running = game_window.handle_events()
        
        # 5.2.2 Оновлення стану генерації (якщо вона ще йде)
        if not generation_finished:
            # Викликаємо один крок алгоритму Конструктора
            # Метод generate_step() повинен повертати True, якщо генерація триває, і False, якщо завершена
            generation_in_progress = builder.generate_step() 
            if not generation_in_progress:
                generation_finished = True
                print("Генерацію рівня завершено.")
                
            # Після зміни сітки Конструктором, просимо Гравця знайти новий оптимальний шлях
            solver.calculate_path()
        
        # 5.2.3 Отримання даних сітки та передача у GameWindow
        # Отримуємо чистий масив стану сітки з Core і передаємо в UI
        game_window.draw_grid(grid.get_data())
        
        # 5.2.4 Передача та відмальовування знайденого шляху
        current_path = solver.get_last_path()
        if current_path:
            game_window.draw_path(current_path)
            
        # 5.2.5 Оновлення екрану
        game_window.update()
        
        # Контроль частоти кадрів
        clock.tick(FPS)

if __name__ == "__main__":
    main()