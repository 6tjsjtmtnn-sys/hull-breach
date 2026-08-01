import pygame

from constants import BLACK, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE
from states.base_state import State

CONTROLS = [
    ("Move left / right", "A / D or Arrow Keys"),
    ("Jump", "Space / W / Up"),
    ("Flip gravity (costs a charge)", "G"),
    ("Pause / resume", "Esc or P"),
]


class ControlsState(State):
    def __init__(self, game):
        super().__init__(game)
        title_font = pygame.font.SysFont(None, 48)
        body_font = pygame.font.SysFont(None, 26)

        self.title_surface = title_font.render("CONTROLS", True, WHITE)
        self.rows = [
            (body_font.render(action, True, WHITE), body_font.render(keys, True, WHITE))
            for action, keys in CONTROLS
        ]
        self.prompt_surface = body_font.render("Press ESC to return", True, WHITE)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from states.menu_state import MenuState

            self.next_state = MenuState(self.game)

    def draw(self, screen):
        screen.fill(BLACK)
        center_x = SCREEN_WIDTH // 2
        screen.blit(self.title_surface, self.title_surface.get_rect(center=(center_x, 90)))

        y = 190
        for action_surface, keys_surface in self.rows:
            screen.blit(action_surface, (center_x - 280, y))
            screen.blit(keys_surface, (center_x + 60, y))
            y += 44

        screen.blit(
            self.prompt_surface, self.prompt_surface.get_rect(center=(center_x, SCREEN_HEIGHT - 60))
        )
