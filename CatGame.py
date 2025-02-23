import pygame
import random
from cat import Cat
from ball import Ball, RainbowBall
from bomb import Bomb
from ui import UI

pygame.init()

# Constants
VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 1280, 720
WIN_SCORE = 200
BOMB_INCREASE_THRESHOLD = 10

# GAME Background Color
LIGHT_GREY = (211, 211, 211)

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (150, 150, 150)
COLORS = [RED, BLUE, GREEN, YELLOW, GRAY]

# Setup
screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Cat Eat Balls Game")
virtual_screen = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
ui = UI(VIRTUAL_WIDTH, VIRTUAL_HEIGHT)

# Assets
try:
    cat_img = pygame.image.load("cat.png").convert_alpha()
    cat_img = pygame.transform.scale(cat_img, (50, 50))
    bomb_img = pygame.image.load("bomb.png").convert_alpha()
    bomb_img = pygame.transform.scale(bomb_img, (30, 30))
    explosion_sound = pygame.mixer.Sound("explosion.mp3")
    eat_sound = pygame.mixer.Sound("eat_sound.mp3")
    lost_game_sound = pygame.mixer.Sound("lost_game.mp3")
    rainbow_spawn_sound = pygame.mixer.Sound("rainbowball_spawned.mp3")
    rainbow_eat_sound = pygame.mixer.Sound("rainbowball_eaten.mp3")
    pygame.mixer.music.load("game-music-loop-6.mp3")
except pygame.error as e:
    print(f"Error loading assets: {e}")
    pygame.quit()
    exit()

def reset_game(difficulty, cat=None):
    if cat is None:
        cat = Cat(difficulty=difficulty)
    balls = [Ball(colors=COLORS) for _ in range(5)]
    bombs = [Bomb(difficulty=difficulty, cat=cat) for _ in range(3)]
    pygame.mixer.music.play(-1)
    return cat, balls, bombs, difficulty

def scale_screen(fullscreen, screen, virtual_screen):
    if fullscreen:
        screen_width, screen_height = pygame.display.get_surface().get_size()
        scale = min(screen_width / VIRTUAL_WIDTH, screen_height / VIRTUAL_HEIGHT)
        scaled_width = int(VIRTUAL_WIDTH * scale)
        scaled_height = int(VIRTUAL_HEIGHT * scale)
        scaled_surface = pygame.transform.scale(virtual_screen, (scaled_width, scaled_height))
        screen.fill(LIGHT_GREY)
        x_offset = (screen_width - scaled_width) // 2
        y_offset = (screen_height - scaled_height) // 2
        screen.blit(scaled_surface, (x_offset, y_offset))
    else:
        screen.blit(virtual_screen, (0, 0))

def scale_mouse_pos(mouse_pos, fullscreen):
    if fullscreen:
        screen_width, screen_height = pygame.display.get_surface().get_size()
        scale = min(screen_width / VIRTUAL_WIDTH, screen_height / VIRTUAL_HEIGHT)
        x_offset = (screen_width - VIRTUAL_WIDTH * scale) // 2
        y_offset = (screen_height - VIRTUAL_HEIGHT * scale) // 2
        scaled_x = (mouse_pos[0] - x_offset) / scale
        scaled_y = (mouse_pos[1] - y_offset) / scale
        return (int(scaled_x), int(scaled_y))
    return mouse_pos

# Game setup
clock = pygame.time.Clock()
cat, balls, bombs = None, None, None
rainbow_ball = None
current_difficulty = "Easy"
running = True
game_started = False
game_over = False
lost_sound_played = False
paused = False
fullscreen = False
consecutive_colors = []
attracting = False
attracted_count = 0
pre_attraction_ball_count = 0
showing_instructions = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_started and not paused:
                mouse_pos = scale_mouse_pos(event.pos, fullscreen)
                for level, rect in difficulty_buttons.items():
                    if rect.collidepoint(mouse_pos):
                        if level == "START":
                            cat, balls, bombs, current_difficulty = reset_game(current_difficulty)
                            game_started = True
                            game_over = False
                            lost_sound_played = False
                            consecutive_colors = []
                            rainbow_ball = None
                            attracting = False
                            attracted_count = 0
                            pre_attraction_ball_count = 0
                            if current_difficulty == "Hard":
                                pygame.mouse.set_visible(False)
                        elif level == "QUIT":
                            running = False
                        elif level == "HOW_TO_PLAY":
                            showing_instructions = True
                        else:
                            current_difficulty = level
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if game_over or paused:
                    cat, balls, bombs, current_difficulty = reset_game(current_difficulty)
                    game_started = False
                    game_over = False
                    paused = False
                    lost_sound_played = False
                    pygame.mouse.set_visible(True)
                    consecutive_colors = []
                    rainbow_ball = None
                    attracting = False
                    attracted_count = 0
                    pre_attraction_ball_count = 0
            elif event.key == pygame.K_ESCAPE:
                if showing_instructions:
                    showing_instructions = False
                elif game_started and not game_over:
                    paused = not paused
                    if current_difficulty == "Hard":
                        pygame.mouse.set_visible(paused)
            elif event.key == pygame.K_q and paused:
                running = False
            elif event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)

    virtual_screen.fill(LIGHT_GREY)

    if not game_started:
        if showing_instructions:
            ui.draw_how_to_play(virtual_screen)
        else:
            difficulty_buttons = ui.draw_start_screen(virtual_screen, current_difficulty)
            pygame.mouse.set_visible(True)
    else:
        if paused:
            ui.draw_hud(virtual_screen, cat)
            ui.draw_pause_screen(virtual_screen)
        elif not game_over:
            keys = pygame.key.get_pressed()
            mouse_pos = scale_mouse_pos(pygame.mouse.get_pos(), fullscreen) if current_difficulty == "Hard" else None
            
            cat.move(keys, mouse_pos)
            cat.draw(virtual_screen, cat_img)
            
            if rainbow_ball:
                if not paused and rainbow_ball.get_lifetime() >= 5:
                    rainbow_ball = None
            
            for ball in balls[:]:
                if attracting:
                    dx = cat.rect.centerx - ball.x
                    dy = cat.rect.centery - ball.y
                    distance = max(1, (dx**2 + dy**2)**0.5)
                    speed_factor = 10 * max(abs(ball.original_dx), abs(ball.original_dy))
                    ball.x += speed_factor * (dx / distance)
                    ball.y += speed_factor * (dy / distance)
                elif not paused:
                    ball.move()
                ball.draw(virtual_screen)
                if ball.check_collision(cat):
                    eat_sound.play()
                    if not attracting:
                        consecutive_colors.append(ball.color)
                        if len(consecutive_colors) > 5:
                            consecutive_colors.pop(0)
                        if (len(consecutive_colors) == 5 and 
                            all(c == consecutive_colors[0] for c in consecutive_colors) and 
                            rainbow_ball is None):
                            rainbow_ball = RainbowBall(cat=cat)
                            rainbow_spawn_sound.play()
                        balls.remove(ball)
                        cat.score += 1
                        balls.append(Ball(colors=COLORS))
                    else:
                        balls.remove(ball)
                        cat.score += 1
                        attracted_count += 1
                        if not balls:
                            attracting = False
                            for _ in range(pre_attraction_ball_count):
                                balls.append(Ball(colors=COLORS))
                            attracted_count = 0
                            pre_attraction_ball_count = 0
                            for bomb in bombs:
                                bomb.dx = bomb.original_dx if hasattr(bomb, 'original_dx') else random.choice([-1, 1]) * random.uniform(1, 3) * (1 if current_difficulty == "Easy" else Bomb(difficulty=current_difficulty).dx)
                                bomb.dy = bomb.original_dy if hasattr(bomb, 'original_dy') else random.choice([-1, 1]) * random.uniform(1, 3) * (1 if current_difficulty == "Easy" else Bomb(difficulty=current_difficulty).dy)
                    if cat.score % BOMB_INCREASE_THRESHOLD == 0 and not attracting:
                        bombs.append(Bomb(speed_multiplier=1 + cat.score/50, difficulty=current_difficulty, cat=cat))
                    if cat.score >= WIN_SCORE:
                        game_over = True
                        pygame.mixer.music.stop()
                        if current_difficulty == "Hard":
                            pygame.mouse.set_visible(True)
            
            if rainbow_ball:
                if not paused:
                    rainbow_ball.move()
                rainbow_ball.draw(virtual_screen)
                if rainbow_ball.check_collision(cat):
                    rainbow_eat_sound.play()
                    consecutive_colors = []
                    pre_attraction_ball_count = len(balls)
                    cat.score += 50
                    for _ in range(5):
                        balls.append(Ball(colors=COLORS))
                    rainbow_ball = None
                    attracting = True
                    for bomb in bombs:
                        bomb.dx, bomb.dy = 0, 0
            
            for bomb in bombs[:]:
                if not paused and not attracting:
                    bomb.move()
                bomb.draw(virtual_screen, bomb_img)
                if bomb.check_collision(cat):
                    explosion_sound.play()
                    cat.lives -= 1
                    bombs.remove(bomb)
                    bombs.append(Bomb(speed_multiplier=1 + cat.score/50, difficulty=current_difficulty, cat=cat))
                    if cat.lives <= 0:
                        game_over = True
                        pygame.mixer.music.stop()
                        if not lost_sound_played:
                            lost_game_sound.play()
                            lost_sound_played = True
                        if current_difficulty == "Hard":
                            pygame.mouse.set_visible(True)
        
        ui.draw_hud(virtual_screen, cat)
        
        if game_over:
            font = pygame.font.Font(None, 100)
            text = "You Win!" if cat.score >= WIN_SCORE else "Game Over!"
            color = YELLOW if cat.score >= WIN_SCORE else RED
            end_text = font.render(text, True, color)
            restart_text = pygame.font.Font(None, 36).render("Press R to Restart", True, BLACK)
            virtual_screen.blit(end_text, (VIRTUAL_WIDTH // 2 - end_text.get_width() // 2, VIRTUAL_HEIGHT // 2 - 50))
            virtual_screen.blit(restart_text, (VIRTUAL_WIDTH // 2 - restart_text.get_width() // 2, VIRTUAL_HEIGHT // 2 + 50))

    scale_screen(fullscreen, screen, virtual_screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()