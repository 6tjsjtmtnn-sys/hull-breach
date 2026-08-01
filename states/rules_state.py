import pygame

from constants import BLACK, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE
from states.base_state import State

RULES = [
    "Reach the exit sign on each level to move on to the next.",
    "Your oxygen drains over time - refill it with blue oxygen pickups.",
    "Touching a drone or spikes costs oxygen and knocks you back.",
    "Collect green diamonds for a gravity-flip charge, then press G to flip.",
    "Run out of oxygen and it's game over.",
]


class RulesState(State):
    def __init__(self, game):
        super().__init__(game)
        title_font = pygame.font.SysFont(None, 48)
        body_font = pygame.font.SysFont(None, 26)

        self.title_surface = title_font.render("RULES", True, WHITE)
        self.lines = [body_font.render(f"- {rule}", True, WHITE) for rule in RULES]
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
        for line in self.lines:
            screen.blit(line, (center_x - 300, y))
            y += 44

        screen.blit(
            self.prompt_surface, self.prompt_surface.get_rect(center=(center_x, SCREEN_HEIGHT - 60))
        )
