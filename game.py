import pygame

from constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE
from states.play_state import PlayState


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = PlayState(self)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                self.state.handle_event(event)

            self.state.update(dt)
            self.state.draw(self.screen)
            pygame.display.flip()

            if self.state.next_state is not None:
                self.state = self.state.next_state

        pygame.quit()
