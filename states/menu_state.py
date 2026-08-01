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
        self.start_surface = body_font.render("[ENTER] Start Game", True, WHITE)
        self.controls_surface = body_font.render("[C] Controls", True, WHITE)
        self.rules_surface = body_font.render("[R] Rules", True, WHITE)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                from states.play_state import PlayState

                self.next_state = PlayState(self.game, level_index=0)
            elif event.key == pygame.K_c:
                from states.controls_state import ControlsState

                self.next_state = ControlsState(self.game)
            elif event.key == pygame.K_r:
                from states.rules_state import RulesState

                self.next_state = RulesState(self.game)

    def draw(self, screen):
        screen.fill(BLACK)
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        screen.blit(self.title_surface, self.title_surface.get_rect(center=(center_x, center_y - 80)))
        screen.blit(self.subtitle_surface, self.subtitle_surface.get_rect(center=(center_x, center_y - 20)))
        screen.blit(self.start_surface, self.start_surface.get_rect(center=(center_x, center_y + 40)))
        screen.blit(self.controls_surface, self.controls_surface.get_rect(center=(center_x, center_y + 80)))
        screen.blit(self.rules_surface, self.rules_surface.get_rect(center=(center_x, center_y + 120)))
