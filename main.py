import pygame
import random
from block import *
from grid import *
from soundplayer import *
from savedata import *

pygame.init()

block_size = 48
grid_width = 10
grid_height = 20

screen = pygame.display.set_mode((grid_width * block_size, grid_height * block_size))
pygame.display.set_caption("Screri Tetris")

clock = pygame.time.Clock()

textures = True

grid = Grid(grid_width, grid_height, block_size)
block = BlockTexture(["resources/textures/block.png"])  # "resources/textures/smile.png"
texture = block

block = Block(random.choice(list(Block.SHAPES.keys())), 4, 0, block_size, texture)
if textures:
    block.toggle_texture()

save_data = SaveData()

best_score = save_data.load()
score = 0

diff = 1

DIFFICULTY = [
    'EASY',  # 0
    'NORMAL',  # 1
    'HARD',  # 2
    'INSANE',  # 3
]

fall_time = 500
last_fall_time = pygame.time.get_ticks()

move_delay = 150
last_move_time = 0

rotation_pressed = False
game_over = False

gui_scale = block_size / 100

huge_font = pygame.font.SysFont(None, int(gui_scale * 72 * 2))
big_font = pygame.font.SysFont(None, int(gui_scale * 56 * 2))
medium_font = pygame.font.SysFont(None, int(gui_scale * 48 * 2))
small_font = pygame.font.SysFont(None, int(gui_scale * 24 * 2))

title_text = big_font.render(f"Screri Tetris", True, (255, 255, 255))
title_rect = title_text.get_rect(center=(grid_width * block_size // 2, grid_height * block_size // 4))

play_text = medium_font.render(f"Press space to play...", True, (255, 255, 255))
play_rect = play_text.get_rect(center=(grid_width * block_size // 2, grid_height * block_size // 3))

main_menu = True
while main_menu:
    color = (0, 0, 0)

    fall_time = 500 + ((len(DIFFICULTY) - diff) - 1) * 75

    if diff == 0:
        color = (0, 255, 0)
    elif diff == 1:
        color = (255, 255, 0)
    elif diff == 2:
        color = (255, 0, 0)
    elif diff == 3:
        color = (255, 0, 255)

    difficulty_text = medium_font.render(f"<{DIFFICULTY[diff]}>", True, color)
    difficulty_rect = difficulty_text.get_rect(center=(grid_width * block_size // 2, grid_height * block_size // 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                diff -= 1
                if diff < 0:
                    diff = len(DIFFICULTY) - 1

            if event.key == pygame.K_RIGHT:
                diff += 1
                if diff >= len(DIFFICULTY):
                    diff = 0

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                main_menu = False

    screen.fill((0, 0, 0))
    screen.blit(title_text, title_rect)
    screen.blit(play_text, play_rect)
    screen.blit(difficulty_text, difficulty_rect)
    pygame.display.flip()

    clock.tick(60)

game_over_text = big_font.render("Game Over!", True, (255, 0, 0))
score_text = medium_font.render(f"Score: {score}", True, (255, 255, 255))
instruction_text = medium_font.render(f"Press ESC to close...", True, (255, 255, 255))
pause_text = huge_font.render(f"Paused", True, (165, 100, 255))

text_rect = game_over_text.get_rect(center=(grid_width * block_size // 2, grid_height * block_size // 4))
score_rect = score_text.get_rect(center=(grid_width * block_size // 2, grid_height * block_size // 3))
instruction_rect = instruction_text.get_rect(center=(grid_width * block_size // 2, grid_height * block_size // 2))
pause_rect = pause_text.get_rect(center=(grid_width * block_size // 2, grid_height * block_size // 2))

sound_player = None

try:
    sound_player = SoundPlayer("resources/audio/song.mp3")
    sound_player.set_volume(0.5)
    sound_player.play()
except:
    print("Error loading audio file. Check file path! (resources/audio/song.mp3)")

running = True
paused = False
while running:
    if score > best_score:
        save_data.save(score)

    if sound_player and not sound_player.is_playing():
        sound_player.play()

    if fall_time > 250 - diff * 15:
        fall_time = 500 - (score // 100) * (2 * ((diff + 1) * 1.5))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_t:
                textures = not textures

            if event.key == pygame.K_UP and not rotation_pressed and not paused:
                block.rotate()
                if not grid.is_valid_position(block):
                    block.rotate()
                    block.rotate()
                    block.rotate()
                rotation_pressed = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                paused = not paused

                if sound_player:
                    if paused:
                        sound_player.pause()
                    else:
                        sound_player.resume()

            if not paused:
                if event.key == pygame.K_UP:
                    rotation_pressed = False

    if game_over:
        screen.fill((0, 0, 0))

        screen.blit(game_over_text, text_rect)
        screen.blit(score_text, score_rect)
        screen.blit(instruction_text, instruction_rect)

        pygame.display.flip()
        continue

    screen.fill((0, 0, 0))
    current_time = pygame.time.get_ticks()

    if current_time - last_fall_time > fall_time and not paused:
        if block.can_move(0, 1, grid_width, grid_height, grid.grid):
            block.move(0, 1, grid_width, grid_height)
        else:
            if block.grid_y < 1:
                game_over = True
            else:
                grid.add_block_to_grid(block)
                score += grid.clear_lines() * 100
                block = Block(random.choice(list(Block.SHAPES.keys())), 4, 0, block_size, texture)
                if textures:
                    block.toggle_texture()
        last_fall_time = current_time

    if not game_over:
        keys = pygame.key.get_pressed()

        if not paused:
            if keys[pygame.K_LEFT] and current_time - last_move_time > move_delay:
                if block.can_move(-1, 0, grid_width, grid_height, grid.grid):
                    block.move(-1, 0, grid_width, grid_height)
                last_move_time = current_time
            if keys[pygame.K_RIGHT] and current_time - last_move_time > move_delay:
                if block.can_move(1, 0, grid_width, grid_height, grid.grid):
                    block.move(1, 0, grid_width, grid_height)
                last_move_time = current_time
            if keys[pygame.K_DOWN]:
                if block.can_move(0, 1, grid_width, grid_height, grid.grid):
                    block.move(0, 1, grid_width, grid_height)

    grid.draw(screen)
    block.draw(screen, 0, 0)

    score_text = medium_font.render(f"Score: {score}", True, (255, 255, 255))
    best_score_text = medium_font.render(f"Best Score: {best_score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(best_score_text, (10, gui_scale * 80))

    if paused:
        screen.blit(pause_text, pause_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
