import pygame

from constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE
from states.menu_state import MenuState


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = MenuState(self)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                self.state.handle_event(event)

            self.state.update(dt)
            self.state.draw(self.screen)
            pygame.display.flip()

            if self.state.next_state is not None:
                next_state = self.state.next_state
                # Clear it on the outgoing state before switching — a
                # resumed/reused state instance (e.g. PlayState after
                # PauseState hands control back) would otherwise still
                # carry the old transition and immediately bounce right
                # back to it next frame.
                self.state.next_state = None
                self.state = next_state

        pygame.quit()
