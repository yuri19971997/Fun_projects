"""Entry point -- launches the game."""

from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from . import config
from .game import GameScene
from .title import TitleScreen


def game_loop(screen):
    """Run title screen then game, handling transitions via NextScene."""
    # Check minimum terminal size
    if screen.width < config.MIN_WIDTH or screen.height < config.MIN_HEIGHT:
        screen.clear()
        msg = f"Terminal too small! Need {config.MIN_WIDTH}x{config.MIN_HEIGHT}, got {screen.width}x{screen.height}"
        screen.print_at(msg, 0, 0, colour=Screen.COLOUR_RED)
        screen.print_at("Resize your terminal and restart.", 0, 1)
        screen.refresh()
        screen.wait_for_input(10)
        return

    scenes = [
        Scene([TitleScreen(screen)], -1, name="title"),
        Scene([GameScene(screen)], -1, name="game"),
    ]

    screen.play(scenes, stop_on_resize=True, repeat=True)


def main():
    """Entry point."""
    while True:
        try:
            Screen.wrapper(game_loop)
            break
        except ResizeScreenError:
            continue
        except StopApplication:
            break


if __name__ == "__main__":
    main()
