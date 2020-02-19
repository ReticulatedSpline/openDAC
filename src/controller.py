"""gobetween for view & model"""
from enum import IntEnum
from functools import partial
from pynput.keyboard import Listener, KeyCode, Key

from view import View, Display
from model import Library, Player


class Menu(IntEnum):
    """home menu options"""
    PLAYLISTS = 0
    ALBUMS = 1
    ARTISTS = 2
    GENRES = 3
    TRACKS = 4
    QUEUE = 5
    SETTINGS = 6
    EXIT = 7


class Direction(IntEnum):
    """navigational directions"""
    UP = 1
    DOWN = 2
    SELECT = 3
    BACK = 4


def handle_playlist_select(view: View, library: Library):
    display = view.menu_stack[-1]
    playlist = library.playlists[display.index + display.start_index]
    if (playlist.is_dir):
        # TODO: Handle this case
        pass
    else:
        new_dp_path = display.menu_path + '/' + playlist.name
        items = [str(item) for item in playlist.items]
        new_display = Display(new_dp_path, items, 0, 0)
        view.menu_stack.append(new_display)


def handle_select(view: View, library: Library):
    display = view.menu_stack[-1]
    if display.menu_path.startswith('home/playlists'):
        handle_playlist_select(view, library)


def handle_home_select(view: View, library: Library):
    display = view.menu_stack[-1]
    index = display.index + display.start_index
    if index == Menu.EXIT:
        return False
    elif index == Menu.PLAYLISTS:
        path = display.menu_path + '/playlists'
        items = [item.name for item in library.playlists]
        display = Display(path, items, 0, 0)
        view.menu_stack.append(display)
    elif index == Menu.TRACKS:
        path = display.menu_path + '/tracks'
        display = Display(path, library.music, 0, 0)
        view.menu_stack.append(display)
    elif index == Menu.ALBUMS:
        view.notify("Not yet implemented!")
    elif index == Menu.ARTISTS:
        view.notify("Not yet implemented!")
    elif index == Menu.GENRES:
        view.notify("Not yet implemented!")
    elif index == Menu.QUEUE:
        view.notify("Not yet implemented!")
    elif index == Menu.SETTINGS:
        view.notify("Not yet implemented!")
    return True


def navigate(view: View, library: Library, direction: Direction):
    """handle menu scrolling by manipulating display tuples"""
    display = view.menu_stack[-1]
    if direction is Direction.UP:
        view.navigate_up(display)
    elif direction is Direction.DOWN:
        view.navigate_down(display)
    elif direction is Direction.BACK:
        if len(view.menu_stack) > 1:
            view.menu_stack.pop()
    elif direction is Direction.SELECT:
        if display.menu_path.endswith('home'):
            return handle_home_select(view, library)
        else:
            return handle_select(view, library)


def on_press(key: KeyCode, view: View, player: Player, library: Library):
    """Callback for handling user input."""
    if hasattr(key, 'char'):
        if key.char == 'p':
            player.play()
        elif key.char == 'a':
            player.pause()
        elif key.char == 'n':
            player.skip_forward()
        elif key.char == 'l':
            player.skip_back()
        return True
    else:
        action = None
        if key == Key.up:
            return navigate(view, library, Direction.UP)
        elif key == Key.down:
            return navigate(view, library, Direction.DOWN)
        elif key == Key.right:
            return navigate(view, library, Direction.SELECT)
        elif key == Key.left:
            return navigate(view, library, Direction.BACK)


def tick(view: View, player: Player):
    """periodic ui update"""
    metadata = player.get_metadata()
    view.update_ui(metadata)


def start():
    """splits into two threads for ui and pynput"""
    view = View()
    library = Library()
    player = Player(library)
    listener = Listener(on_press=partial(
        on_press, view=view, player=player, library=library))
    listener.start()
    while listener.running:
        tick(view, player)
    del view