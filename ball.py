import pygame
import random
import math

class Ball:
    def __init__(self, colors, virtual_width=1280, virtual_height=720):  # Remove default colors
        self.x = random.randint(20, virtual_width - 20)
        self.y = random.randint(20, virtual_height - 20)
        self.color = random.choice(colors)  # Use passed colors array
        self.radius = 20
        self.dx = random.choice([-1, 1]) * random.uniform(1, 3)
        self.dy = random.choice([-1, 1]) * random.uniform(1, 3)
        self.original_dx = self.dx
        self.original_dy = self.dy
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x - self.radius <= 0 or self.x + self.radius >= 1280:
            self.dx *= -1
        if self.y - self.radius <= 0 or self.y + self.radius >= 720:
            self.dy *= -1
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
    
    def check_collision(self, cat):
        ball_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                              self.radius * 2, self.radius * 2)
        return ball_rect.colliderect(cat.rect)

class RainbowBall(Ball):
    def __init__(self, cat, virtual_width=1280, virtual_height=720, colors=[(211, 211, 211), (0, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (150, 150, 150)]):
        cat_center_x = cat.rect.centerx
        cat_center_y = cat.rect.centery
        max_distance = max(
            math.sqrt((cat_center_x - 0)**2 + (cat_center_y - 0)**2),
            math.sqrt((cat_center_x - virtual_width)**2 + (cat_center_y - 0)**2),
            math.sqrt((cat_center_x - 0)**2 + (cat_center_y - virtual_height)**2),
            math.sqrt((cat_center_x - virtual_width)**2 + (cat_center_y - virtual_height)**2)
        )
        min_distance = max_distance * 0.9
        
        while True:
            self.x = random.randint(20, virtual_width - 20)
            self.y = random.randint(20, virtual_height - 20)
            distance = math.sqrt((self.x - cat_center_x)**2 + (self.y - cat_center_y)**2)
            if distance >= min_distance:
                break
        
        self.color = random.choice(colors)
        self.radius = 25
        self.dx = random.choice([-1, 1]) * random.uniform(1, 3) * 0.75
        self.dy = random.choice([-1, 1]) * random.uniform(1, 3) * 0.75
        self.original_dx = self.dx
        self.original_dy = self.dy
        self.colors = colors
        self.slice_count = len(colors)
        self.color_indices = list(range(self.slice_count))
        self.last_color_changes = [pygame.time.get_ticks() / 1000] * self.slice_count
        self.spawn_time = pygame.time.get_ticks() / 1000
    
    def move(self):
        super().move()
    
    def draw(self, surface):
        current_time = pygame.time.get_ticks() / 1000
        for i in range(self.slice_count):
            if current_time - self.last_color_changes[i] >= 0.1:
                self.color_indices[i] = (self.color_indices[i] + 1) % len(self.colors)
                self.last_color_changes[i] = current_time
            start_angle = i * (2 * math.pi / self.slice_count)
            end_angle = (i + 1) * (2 * math.pi / self.slice_count)
            pygame.draw.arc(surface, self.colors[self.color_indices[i]], 
                            (int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2), 
                            start_angle, end_angle, self.radius)
    
    def get_lifetime(self):
        return pygame.time.get_ticks() / 1000 - self.spawn_time