import pygame

class GameWindow:
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)
    COLOR_GRAY = (128, 128, 128)
    COLOR_GREEN = (0, 255, 0)
    COLOR_RED = (255, 0, 0)
    COLOR_BLUE = (0, 0, 255)
    COLOR_LIGHT_BROWN = (144, 238, 144)
    COLOR_DARK_BROWN = (75, 83, 32)
    
    def __init__(self, window_width, window_height, grid_width, grid_height, cell_size, fps=60):
        self.window_width = window_width
        self.window_height = window_height
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size
        self.fps = fps
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Антагоністична генерація рівней")
        self.clock = pygame.time.Clock()

    def clear_screen(self):
        self.screen.fill(self.COLOR_WHITE)

    def update(self):
        pygame.display.flip()
        self.clock.tick(self.fps)

    def quit(self):
        pygame.quit()
    
    def draw_grid(self, grid_data):
        if not grid_data or not grid_data[0]:
            return

        rows = len(grid_data)
        cols = len(grid_data[0])

        for y in range(rows):
            for x in range(cols):
                cell = grid_data[y][x]
                cell_value = str(grid_data[y][x]).upper()

                if "EMPTY" in cell_value:
                    color = self.COLOR_WHITE
                elif "OBSTACLE" in cell_value:
                    color = self.COLOR_BLACK
                elif "START" in cell_value:
                    color = self.COLOR_GREEN
                elif "GOAL" in cell_value:
                    color = self.COLOR_RED
                elif "INTERACTIVE" in cell_value:
                    if cell.weight >= 5.0:
                        color = self.COLOR_DARK_BROWN
                    else:
                        color = self.COLOR_LIGHT_BROWN 
                else:
                    color = self.COLOR_WHITE

                rect = (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.COLOR_GRAY, rect, 1)
    
    def draw_path(self, path_coords):
        if not path_coords:
            return

        for x, y in path_coords:
                    margin = self.cell_size // 4
                    
                    rect = (x * self.cell_size + margin, 
                            y * self.cell_size + margin, 
                            self.cell_size - (margin * 2), 
                            self.cell_size - (margin * 2))

                    pygame.draw.rect(self.screen, self.COLOR_BLUE, rect)

    def handle_events(self):
        actions = {
            "quit": False,
            "next_step": False
        }

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                actions["quit"] = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    actions["next_step"] = True
                elif event.key == pygame.K_ESCAPE:
                    actions["quit"] = True

        return actions