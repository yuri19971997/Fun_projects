"""Entry point -- launches the game."""

import argparse

from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from . import config
from .game import GameScene
from .title import TitleScreen


def game_loop(screen, start_wave=1):
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

    game = GameScene(screen, start_wave=start_wave)
    scenes = [
        Scene([TitleScreen(screen)], -1, name="title"),
        Scene([game], -1, name="game"),
    ]

    # Skip title screen if starting at a specific wave
    start = scenes[1] if start_wave > 1 else None
    screen.play(scenes, stop_on_resize=True, repeat=True, start_scene=start)


def main():
    """Entry point."""
    parser = argparse.ArgumentParser(description="Invader for Chiks")
    parser.add_argument("--wave", type=int, default=1,
                        help="Start at wave N (e.g. --wave 5 for first boss)")
    args = parser.parse_args()

    while True:
        try:
            Screen.wrapper(game_loop, arguments=[args.wave])
            break
        except ResizeScreenError:
            continue
        except StopApplication:
            break


if __name__ == "__main__":
    main()
