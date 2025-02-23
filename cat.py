import pygame

class Cat:
    def __init__(self, difficulty="Easy", virtual_width=1280, virtual_height=720):  # Updated defaults
        self.rect = pygame.Rect(virtual_width // 2, virtual_height // 2, 50, 50)
        self.lives = 3
        self.score = 0
        self.difficulty = difficulty
        self.speed = 5
    
    def move(self, keys, mouse_pos=None):
        if self.difficulty == "Hard" and mouse_pos is not None:
            target_x, target_y = mouse_pos
            self.rect.centerx = target_x
            self.rect.centery = target_y
            self.rect.clamp_ip(pygame.Rect(0, 0, 1280, 720))  # Updated to 1280x720
        else:
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left > 0:
                self.rect.x -= self.speed
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right < 1280:
                self.rect.x += self.speed
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top > 0:
                self.rect.y -= self.speed
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom < 720:
                self.rect.y += self.speed
    
    def draw(self, surface, cat_img):
        surface.blit(cat_img, self.rect)