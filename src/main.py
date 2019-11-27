import time
from pynput import keyboard
from functools import partial

from view import View
from player import Player


def on_press(key: keyboard.KeyCode, view: View, player: Player):
    """Handle keypresses. Deprecate for touchscreen eventually."""
    key = str(key).strip('\'')
    if str(key) == 'p':
        view.notify('Playing...')
        player.play()
        return
    elif key == 'a':
        view.notify('Pausing...')
        player.pause()
    elif key == 'n':
        view.notify('Skipping Forward...')
        player.skip_forward()
        return
    elif key == 'l':
        view.notify('Skipping Back...')
        player.skip_back()
        return
    elif key == 'q':
        view.notify('Exiting...')
        del view
        del player
        exit(0)
    view.update_ui(player.get_metadata())


view = View()
player = Player()
with keyboard.Listener(on_press=partial(on_press, view=view, player=player)) as listener:
    listener.join()
