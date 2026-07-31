import pygame

from constants import BLACK, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE
from states.base_state import State


class GameOverState(State):
    def __init__(self, game, won):
        super().__init__(game)
        self.won = won

        title_font = pygame.font.SysFont(None, 48)
        body_font = pygame.font.SysFont(None, 28)

        title = "HULL BREACH SEALED" if won else "OXYGEN DEPLETED"
        subtitle = "You escaped the station." if won else "You didn't make it out in time."

        self.title_surface = title_font.render(title, True, WHITE)
        self.subtitle_surface = body_font.render(subtitle, True, WHITE)
        self.prompt_surface = body_font.render("Press any key to try again", True, WHITE)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.KEYDOWN:
            from states.play_state import PlayState

            self.next_state = PlayState(self.game)

    def draw(self, screen):
        screen.fill(BLACK)
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        screen.blit(self.title_surface, self.title_surface.get_rect(center=(center_x, center_y - 40)))
        screen.blit(self.subtitle_surface, self.subtitle_surface.get_rect(center=(center_x, center_y)))
        screen.blit(self.prompt_surface, self.prompt_surface.get_rect(center=(center_x, center_y + 40)))
