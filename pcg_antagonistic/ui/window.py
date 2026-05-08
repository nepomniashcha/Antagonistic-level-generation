import pygame

class GameWindow:
    # Константы цветов (RGB)
    COLOR_WHITE = (255, 255, 255)      # Пустые ячейки / Фон
    COLOR_BLACK = (0, 0, 0)            # Препятствия
    COLOR_GRAY = (128, 128, 128)       # Линии сетки
    COLOR_GREEN = (0, 255, 0)          # Точка старта
    COLOR_RED = (255, 0, 0)            # Точка финиша
    COLOR_BLUE = (0, 0, 255)           # Оптимальный путь
    
    def __init__(self, window_width, window_height, grid_width, grid_height, fps=60):
        """
        Инициализация окна игры, настройка размеров и FPS.
        """
        self.window_width = window_width
        self.window_height = window_height
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.fps = fps
        
        # Вычисление размера одной ячейки (в пикселях) для отрисовки
        self.cell_width = window_width // grid_width
        self.cell_height = window_height // grid_height
        
        # Инициализация Pygame
        pygame.init()
        # Создание окна
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Антагонистическая генерация уровней")
        # Таймер для контроля частоты кадров
        self.clock = pygame.time.Clock()

    def clear_screen(self):
        """
        Очистка экрана (заливка фоновым цветом).
        """
        self.screen.fill(self.COLOR_WHITE)

    def update(self):
        """
        Обновление экрана и контроль FPS. Вызывается каждую итерацию игрового цикла.
        """
        pygame.display.flip()
        self.clock.tick(self.fps)

    def quit(self):
        """
        Корректное завершение работы Pygame.
        """
        pygame.quit()
    
    def draw_grid(self, grid_data):
        """
        Отрисовка сетки на экране.
        
        :param grid_data: Двумерный массив (список списков), полученный из Core.
                          Ожидается, что элементы содержат информацию о типе ячейки
                          (например, Enum CellType или строковые значения).
        """
        # Проверка на пустые данные
        if not grid_data or not grid_data[0]:
            return

        rows = len(grid_data)
        cols = len(grid_data[0])

        # Динамическое вычисление размеров одной ячейки на основе размера окна
        cell_width = self.width // cols
        cell_height = self.height // rows

        for y in range(rows):
            for x in range(cols):
                # Получаем строковое представление типа ячейки для универсальности
                cell_value = str(grid_data[y][x]).upper()

                # Цветовое кодирование согласно требованиям
                if "EMPTY" in cell_value:
                    color = self.COLOR_WHITE
                elif "OBSTACLE" in cell_value:
                    color = self.COLOR_BLACK  # Черный для препятствий
                elif "START" in cell_value:
                    color = self.COLOR_GREEN
                elif "GOAL" in cell_value:
                    color = self.COLOR_RED
                else:
                    color = self.COLOR_WHITE  # Цвет по умолчанию, если тип не распознан

                # Вычисление координат для текущего квадрата
                rect = (x * cell_width, y * cell_height, cell_width, cell_height)

                # Отрисовка заливки ячейки
                pygame.draw.rect(self.screen, color, rect)

                # Отрисовка контура ячейки (серая линия сетки для визуального разделения)
                pygame.draw.rect(self.screen, self.COLOR_GRAY, rect, 1)
    
    def draw_path(self, path_coords, cols, rows):
        """
        Отрисовка оптимального пути поверх сгенерированного уровня.
        
        :param path_coords: Список кортежей с координатами пути [(x1, y1), (x2, y2), ...].
        :param cols: Общее количество столбцов в сетке (для вычисления размера ячейки).
        :param rows: Общее количество строк в сетке (для вычисления размера ячейки).
        """
        # Если путь не найден или пуст, ничего не рисуем
        if not path_coords:
            return

        # Вычисляем размеры ячейки (аналогично методу draw_grid)
        cell_width = self.width // cols
        cell_height = self.height // rows

        for x, y in path_coords:
            # Вычисляем позицию квадрата на экране
            # Предполагается, что координаты передаются в формате (x, y), где x - столбец, y - строка
            rect = (x * cell_width, y * cell_height, cell_width, cell_height)

            # Закрашиваем ячейку цветом пути (COLOR_BLUE был задан в Task 4.1)
            pygame.draw.rect(self.screen, self.COLOR_BLUE, rect)

            # Отрисовываем серый контур ячейки поверх пути для сохранения визуальной структуры сетки
            pygame.draw.rect(self.screen, self.COLOR_GRAY, rect, 1)

    def handle_events(self):
        """
        Обработка событий пользователя (закрытие окна, нажатие клавиш).
        
        Возвращает:
            dict: Словарь с флагами действий, которые необходимо обработать 
                  в главном цикле игры (main.py).
        """
        actions = {
            "quit": False,
            "next_step": False
        }

        for event in pygame.event.get():
            # Обработка стандартного закрытия окна (нажатие на крестик)
            if event.type == pygame.QUIT:
                actions["quit"] = True
            
            # Обработка событий клавиатуры
            elif event.type == pygame.KEYDOWN:
                # Нажатие клавиши 'Space' (Пробел) для выполнения следующего шага генерации
                if event.key == pygame.K_SPACE:
                    actions["next_step"] = True
                
                # Опционально: Нажатие 'Escape' для быстрого выхода из приложения
                elif event.key == pygame.K_ESCAPE:
                    actions["quit"] = True

        return actions