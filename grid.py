import pygame

class Grid:
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.color_grid = [[(0, 0, 0) for _ in range(self.width)] for _ in range(self.height)]
        self.texture_grid = [[None for _ in range(self.width)] for _ in range(self.height)]  # Added texture grid

    def draw(self, surface):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 1:
                    if self.texture_grid[y][x]:
                        # Draw the texture
                        texture = self.texture_grid[y][x]
                        surface.blit(texture, (x * self.block_size, y * self.block_size))
                    else:
                        # Draw the block color
                        block_color = self.get_block_color(x, y)
                        pygame.draw.rect(
                            surface,
                            block_color,
                            pygame.Rect(x * self.block_size, y * self.block_size, self.block_size, self.block_size)
                        )
                else:
                    # Draw grid lines or background
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
                        if block.use_texture and hasattr(block, 'texture'):
                            # Store the scaled texture in the texture grid
                            current_texture = block.texture.get_current_texture()
                            scaled_texture = pygame.transform.scale(current_texture, (self.block_size, self.block_size))
                            self.texture_grid[grid_y][grid_x] = scaled_texture
                        else:
                            self.texture_grid[grid_y][grid_x] = None

    def get_block_color(self, x, y):
        return self.color_grid[y][x]

    def clear_lines(self):
        lines_cleared = 0
        new_grid = []
        new_color_grid = []
        new_texture_grid = []
        for y in range(self.height):
            if sum(self.grid[y]) < self.width:
                new_grid.append(self.grid[y])
                new_color_grid.append(self.color_grid[y])
                new_texture_grid.append(self.texture_grid[y])
            else:
                lines_cleared += 1
        while len(new_grid) < self.height:
            new_grid.insert(0, [0] * self.width)
            new_color_grid.insert(0, [(0, 0, 0)] * self.width)
            new_texture_grid.insert(0, [None] * self.width)
        self.grid = new_grid
        self.color_grid = new_color_grid
        self.texture_grid = new_texture_grid
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
