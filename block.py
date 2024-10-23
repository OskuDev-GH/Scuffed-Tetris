import pygame

class BlockTexture:
    def __init__(self, texture_paths):
        self.textures = [pygame.image.load(path).convert_alpha() for path in texture_paths]
        for path in texture_paths:
            print(path + " loaded!")
        self.current_texture_index = 0
        self.tinted_texture = None

    def toggle_texture(self):
        self.current_texture_index = (self.current_texture_index + 1) % len(self.textures)

    def get_current_texture(self):
        return self.tinted_texture if self.tinted_texture else self.textures[self.current_texture_index]

    def tint(self, color):
        current_texture = self.textures[self.current_texture_index].copy()
        tint_surface = pygame.Surface(current_texture.get_size(), flags=pygame.SRCALPHA)
        tint_surface.fill(color)
        current_texture.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.tinted_texture = current_texture


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

    def __init__(self, shape_type, x, y, size, texture=None):
        super().__init__()
        self.shape_type = shape_type
        self.shape = self.SHAPES[shape_type]
        self.size = size
        self.color = self.COLORS[shape_type]
        self.grid_x = x
        self.grid_y = y
        self.locked = False
        self.use_texture = False  # By default, use color
        self.texture = texture
        self.texture.tint(self.color)

    def toggle_texture(self):
        self.use_texture = not self.use_texture
        if self.use_texture and hasattr(self, 'texture'):
            self.texture.toggle_texture()

    def is_using_texture(self):
        return self.use_texture

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def draw(self, surface, offset_x, offset_y):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell == 1:
                    if self.use_texture and hasattr(self, 'texture'):
                        current_texture = self.texture.get_current_texture()
                        texture_rect = pygame.Rect(
                            (self.grid_x + x) * self.size + offset_x,
                            (self.grid_y + y) * self.size + offset_y,
                            self.size, self.size
                        )
                        surface.blit(pygame.transform.scale(current_texture, (self.size, self.size)), texture_rect)
                    else:
                        pygame.draw.rect(
                            surface,
                            self.color,
                            pygame.Rect(
                                (self.grid_x + x) * self.size + offset_x,
                                (self.grid_y + y) * self.size + offset_y,
                                self.size, self.size
                            )
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
