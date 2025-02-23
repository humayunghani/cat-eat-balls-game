import pygame

class UI:
    def __init__(self, virtual_width=1280, virtual_height=720):
        self.virtual_width = virtual_width
        self.virtual_height = virtual_height
        # Load the how-to-play icon
        self.how_to_play_icon = pygame.image.load("how_to_play_icon.png").convert_alpha()
        self.how_to_play_icon = pygame.transform.scale(self.how_to_play_icon, (100, 100))

    def draw_hud(self, surface, cat):
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f"Lives: {cat.lives}", True, (0, 0, 0))
        score_text = font.render(f"Score: {cat.score}", True, (0, 0, 0))
        surface.blit(lives_text, (10, 10))
        surface.blit(score_text, (10, 50))

    def draw_start_screen(self, surface, selected_difficulty):
        surface.fill((211, 211, 211))
        font = pygame.font.Font(None, 42)
        buttons = {}
        levels = ["Easy", "Medium", "Hard"]
        
        gap = 40
        total_width = sum(font.size(level)[0] for level in levels) + gap * (len(levels) - 1) + 60
        start_x = (self.virtual_width - total_width) // 2
        y_pos = self.virtual_height // 3
        
        current_x = start_x
        for level in levels:
            text = font.render(level, True, (0, 0, 0))
            button_rect = text.get_rect(center=(current_x + text.get_width() // 2, y_pos))
            button_color = (255, 255, 0) if level == selected_difficulty else (0, 255, 0)
            pygame.draw.rect(surface, button_color, button_rect.inflate(20, 20))
            surface.blit(text, button_rect)
            buttons[level] = button_rect
            current_x += text.get_width() + gap
        
        start_text = font.render("START", True, (0, 0, 0))
        quit_text = font.render("QUIT", True, (0, 0, 0))
        
        start_rect = start_text.get_rect(center=(self.virtual_width // 3, y_pos + 150))
        quit_rect = quit_text.get_rect(center=(self.virtual_width * 2 // 3, y_pos + 150))
        how_to_play_rect = self.how_to_play_icon.get_rect(center=(self.virtual_width // 2, y_pos + 250))
        
        pygame.draw.rect(surface, (0, 255, 0), start_rect.inflate(20, 20))
        surface.blit(start_text, start_rect)
        buttons["START"] = start_rect
        
        pygame.draw.rect(surface, (255, 0, 0), quit_rect.inflate(20, 20))
        surface.blit(quit_text, quit_rect)
        buttons["QUIT"] = quit_rect
        
        surface.blit(self.how_to_play_icon, how_to_play_rect)
        buttons["HOW_TO_PLAY"] = how_to_play_rect
        
        return buttons

    def draw_how_to_play(self, surface):
        surface.fill((211, 211, 211))
        font_large = pygame.font.Font(None, 50)
        font_small = pygame.font.Font(None, 36)
        
        title = font_large.render("How to Play", True, (0, 0, 0))
        instructions = [
            "Move the cat with W,A,S,D or arrow keys.",
            "On Hard mode, use the mouse to move.",
            "Eat colored balls to score points.",
            "Avoid bombs or lose lives!",
            "Eat 5 balls of the same color in a row to spawn a Rainbow Ball.",
            "Eat the Rainbow Ball for 50 points and 5 extra balls that rush to you!",
            "Toggle 'F' key to play in full screen.",  # New instruction
            "Press the 'Esc' key during play to pause the Game.",  # New instruction
            "Press ESC to go back."
        ]
        
        title_rect = title.get_rect(center=(self.virtual_width // 2, 100))
        surface.blit(title, title_rect)
        
        for i, line in enumerate(instructions):
            text = font_small.render(line, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.virtual_width // 2, 200 + i * 50))
            surface.blit(text, text_rect)

    def draw_pause_screen(self, surface):
        font = pygame.font.Font(None, 100)
        pause_text = font.render("Paused", True, (150, 150, 150))
        resume_text = pygame.font.Font(None, 36).render("Press Esc to Resume", True, (0, 0, 0))
        restart_text = pygame.font.Font(None, 36).render("Press R to Restart", True, (0, 0, 0))
        quit_text = pygame.font.Font(None, 36).render("Press Q to Quit", True, (0, 0, 0))
        surface.blit(pause_text, (self.virtual_width // 2 - pause_text.get_width() // 2, self.virtual_height // 2 - 50))
        surface.blit(resume_text, (self.virtual_width // 2 - resume_text.get_width() // 2, self.virtual_height // 2 + 50))
        surface.blit(restart_text, (self.virtual_width // 2 - restart_text.get_width() // 2, self.virtual_height // 2 + 100))
        surface.blit(quit_text, (self.virtual_width // 2 - quit_text.get_width() // 2, self.virtual_height // 2 + 150))