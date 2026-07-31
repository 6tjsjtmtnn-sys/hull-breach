import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, WHITE
from states.base_state import State


class PauseState(State):
    def __init__(self, game, paused_state):
        super().__init__(game)
        self.paused_state = paused_state

        title_font = pygame.font.SysFont(None, 48)
        body_font = pygame.font.SysFont(None, 24)
        self.title_surface = title_font.render("PAUSED", True, WHITE)
        self.prompt_surface = body_font.render("Press ESC or P to resume", True, WHITE)

        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 160))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_p):
            self.next_state = self.paused_state

    def draw(self, screen):
        self.paused_state.draw(screen)
        screen.blit(self.overlay, (0, 0))
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        screen.blit(self.title_surface, self.title_surface.get_rect(center=(center_x, center_y - 20)))
        screen.blit(self.prompt_surface, self.prompt_surface.get_rect(center=(center_x, center_y + 20)))
