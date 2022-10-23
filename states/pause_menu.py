from constants import BLACK
from states.state import State


class PauseMenu(State):
    def __init__(self, game):
        super().__init__(game)

    def update(self, delta_time, actions):
        if not actions['pause']:
            self.exit_state()

    def render(self, surface):
        self.prev_state.render(surface)

