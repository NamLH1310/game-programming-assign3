from states.state import State


class Battle(State):
    def __init__(self, game):
        super().__init__(game)

    def update(self, delta_time, actions):
        pass

    def render(self, surface):
        pass
