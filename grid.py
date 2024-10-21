import pygame

class Grid:
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.color_grid = [[(0, 0, 0) for _ in range(self.width)] for _ in range(self.height)]

    def draw(self, surface):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 1:
                    block_color = self.get_block_color(x, y)
                    pygame.draw.rect(
                        surface,
                        block_color,
                        pygame.Rect(x * self.block_size, y * self.block_size, self.block_size, self.block_size)
                    )
                else:
                    pygame.draw.rect(
                        surface,
                        (50, 50, 50),
                        pygame.Rect(x * self.block_size, y * self.block_size, self.block_size, self.block_size),
                        1
                    )

    def add_block_to_grid(self, block):
        for y, row in enumerate(block.shape):
            for x, cell in enumerate(row):
                if cell == 1:
                    grid_x = block.grid_x + x
                    grid_y = block.grid_y + y
                    if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
                        self.grid[grid_y][grid_x] = 1
                        self.color_grid[grid_y][grid_x] = block.color

    def get_block_color(self, x, y):
        return self.color_grid[y][x]

    def clear_lines(self):
        lines_cleared = 0
        new_grid = [row for row in self.grid if sum(row) < self.width]
        lines_cleared = self.height - len(new_grid)
        while len(new_grid) < self.height:
            new_grid.insert(0, [0] * self.width)
        self.grid = new_grid
        return lines_cleared

    def is_valid_position(self, block):
        for y, row in enumerate(block.shape):
            for x, cell in enumerate(row):
                if cell == 1:
                    grid_x = block.grid_x + x
                    grid_y = block.grid_y + y
                    if not (0 <= grid_x < self.width and 0 <= grid_y < self.height):
                        return False
                    if self.grid[grid_y][grid_x] == 1:
                        return False
        return True
