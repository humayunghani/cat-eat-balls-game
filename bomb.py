import pygame
import random
import math

class Bomb:
    def __init__(self, speed_multiplier=1.0, difficulty="Easy", cat=None, virtual_width=1280, virtual_height=720, difficulty_levels=None):  # Updated defaults
        if difficulty_levels is None:
            difficulty_levels = {
                "Easy": {"BOMB_SPEED_MULTIPLIER": 1.0},
                "Medium": {"BOMB_SPEED_MULTIPLIER": 1.1},
                "Hard": {"BOMB_SPEED_MULTIPLIER": 1.3}
            }
        if cat is not None:
            cat_center_x = cat.rect.centerx
            cat_center_y = cat.rect.centery
            max_distance = max(
                math.sqrt((cat_center_x - 0)**2 + (cat_center_y - 0)**2),
                math.sqrt((cat_center_x - virtual_width)**2 + (cat_center_y - 0)**2),
                math.sqrt((cat_center_x - 0)**2 + (cat_center_y - virtual_height)**2),
                math.sqrt((cat_center_x - virtual_width)**2 + (cat_center_y - virtual_height)**2)
            )
            min_distance = max_distance * 0.6
            
            while True:
                x = random.randint(0, virtual_width - 30)
                y = random.randint(0, virtual_height - 30)
                distance = math.sqrt((x - cat_center_x)**2 + (y - cat_center_y)**2)
                if distance >= min_distance:
                    break
        else:
            x = random.randint(0, virtual_width - 30)
            y = random.randint(0, virtual_height - 30)
        
        self.rect = pygame.Rect(x, y, 30, 30)
        
        if difficulty == "Easy":
            base_speed = 1
        else:
            base_speed = random.uniform(1, 3) * difficulty_levels[difficulty]["BOMB_SPEED_MULTIPLIER"]
        
        self.dx = random.choice([-1, 1]) * base_speed * speed_multiplier
        self.dy = random.choice([-1, 1]) * base_speed * speed_multiplier
    
    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.left <= 0 or self.rect.right >= 1280:
            self.dx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= 720:
            self.dy *= -1
    
    def draw(self, surface, bomb_img):
        surface.blit(bomb_img, self.rect)
    
    def check_collision(self, cat):
        return self.rect.colliderect(cat.rect)