import pygame

from constants import BLACK, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE
from states.base_state import State


class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        title_font = pygame.font.SysFont(None, 64)
        body_font = pygame.font.SysFont(None, 28)
        self.title_surface = title_font.render("HULL BREACH", True, WHITE)
        self.subtitle_surface = body_font.render(
            "Escape the station before your oxygen runs out.", True, WHITE
        )
        self.prompt_surface = body_font.render("Press any key to start", True, WHITE)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.KEYDOWN:
            from states.play_state import PlayState

            self.next_state = PlayState(self.game, level_index=0)

    def draw(self, screen):
        screen.fill(BLACK)
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        screen.blit(self.title_surface, self.title_surface.get_rect(center=(center_x, center_y - 60)))
        screen.blit(self.subtitle_surface, self.subtitle_surface.get_rect(center=(center_x, center_y)))
        screen.blit(self.prompt_surface, self.prompt_surface.get_rect(center=(center_x, center_y + 40)))
