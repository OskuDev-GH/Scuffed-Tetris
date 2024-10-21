import pygame
import random

class Block(pygame.sprite.Sprite):
    SHAPES = {
        'I': [[1, 1, 1, 1]],
        'O': [[1, 1], [1, 1]],
        'T': [[0, 1, 0], [1, 1, 1]],
        'L': [[1, 0, 0], [1, 1, 1]],
        'J': [[0, 0, 1], [1, 1, 1]],
        'S': [[0, 1, 1], [1, 1, 0]],
        'Z': [[1, 1, 0], [0, 1, 1]],
    }

    COLORS = {
        'I': (0, 255, 255),   # Cyan
        'O': (255, 255, 0),   # Yellow
        'T': (200, 0, 200),   # Purple
        'L': (255, 165, 0),   # Orange
        'J': (0, 0, 255),     # Blue
        'S': (0, 255, 0),     # Green
        'Z': (255, 0, 0),     # Red 
    }

    def __init__(self, shape_type, x, y, size):
        super().__init__()
        self.shape_type = shape_type
        self.shape = self.SHAPES[shape_type]
        self.size = size
        self.color = self.COLORS[shape_type]  # Set the color based on shape type
        self.grid_x = x
        self.grid_y = y
        self.locked = False  # Default state

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def draw(self, surface, offset_x, offset_y):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(
                        surface,
                        self.color,  # Use the defined color
                        pygame.Rect(
                            (self.grid_x + x) * self.size + offset_x,
                            (self.grid_y + y) * self.size + offset_y,
                            self.size, self.size
                        )
                    )

    def draw_with_outline(self, surface, offset_x, offset_y):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell == 1:
                    # Draw filled block
                    pygame.draw.rect(
                        surface,
                        self.color,  # Use the defined color
                        pygame.Rect(
                            (self.grid_x + x) * self.size + offset_x,
                            (self.grid_y + y) * self.size + offset_y,
                            self.size, self.size
                        )
                    )
                    # Draw outline
                    pygame.draw.rect(
                        surface,
                        (0, 0, 0),  # Black outline color
                        pygame.Rect(
                            (self.grid_x + x) * self.size + offset_x,
                            (self.grid_y + y) * self.size + offset_y,
                            self.size, self.size
                        ),
                        3  # Width of the outline
                    )

    def move(self, dx, dy, grid_width, grid_height):
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        if 0 <= new_x < grid_width and 0 <= new_y < grid_height:
            self.grid_x = new_x
            self.grid_y = new_y

    def can_move(self, dx, dy, grid_width, grid_height, grid_data):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell == 1:
                    new_x = self.grid_x + x + dx
                    new_y = self.grid_y + y + dy
                    if not (0 <= new_x < grid_width and 0 <= new_y < grid_height):
                        return False
                    if grid_data[new_y][new_x] == 1:
                        return False
        return True
