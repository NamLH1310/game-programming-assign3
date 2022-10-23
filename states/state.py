from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self, game, prev_state=None):
        """
        param game: game instance
        :type game: main.Game
        :param prev_state: previous game state
        :type prev_state: State | None
        """
        self.game = game
        self.prev_state = prev_state

    @abstractmethod
    def update(self, delta_time, actions):
        """
        :param delta_time: delta time
        :type delta_time: float
        :param actions: actions dictionary from game instance
        :type actions: dict[str | pygame_gui.elements.UIButton | None]
        :return: None
        """
        pass

    @abstractmethod
    def render(self, surface):
        """
        :param surface: pygame surface
        :type surface: pygame.Surface
        :return: None
        """
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()
