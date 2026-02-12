# input_controller.py
from evdev import UInput, ecodes as e

class InputController:
    def __init__(self, key_bindings):
        self.key_bindings = key_bindings

        cap_events = {
            e.EV_KEY: list(key_bindings.values())
        }

        self.ui = UInput(cap_events, name="hand-controller")

        self.states = {
            name: False for name in key_bindings
        }

    def update(self, actions):
        """
        actions = {
            "left": bool,
            "right": bool,
            "down": bool,
            "jump": bool
        }
        """

        for name, active in actions.items():
            key = self.key_bindings[name]

            if active and not self.states[name]:
                self.ui.write(e.EV_KEY, key, 1)
                self.ui.syn()
                self.states[name] = True

            elif not active and self.states[name]:
                self.ui.write(e.EV_KEY, key, 0)
                self.ui.syn()
                self.states[name] = False

    def close(self):
        self.ui.close()
