"""Title screen -- the first thing players see."""

from asciimatics.effects import Effect
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene, StopApplication
from asciimatics.screen import Screen

from . import config, sprites


class TitleScreen(Effect):
    """Animated title screen with menu."""

    # Prevent asciimatics default handler from stealing our keys
    safe_to_default_unhandled_input = False

    def __init__(self, screen):
        super().__init__(screen)
        self._selected = 0

    def reset(self):
        self._selected = 0

    @property
    def stop_frame(self):
        return 0  # run forever

    @property
    def frame_update_count(self):
        # Refresh every frame for title animation
        return 1

    def process_event(self, event):
        """Handle menu navigation. Return None to consume events."""
        if not isinstance(event, KeyboardEvent):
            return event

        key = event.key_code
        if key in (Screen.KEY_UP, ord("w"), ord("W")):
            self._selected = max(0, self._selected - 1)
        elif key in (Screen.KEY_DOWN, ord("s"), ord("S")):
            self._selected = min(len(sprites.MENU_OPTIONS) - 1, self._selected + 1)
        elif key in (ord("\n"), ord("\r"), ord(" ")):
            if self._selected == 0:
                raise NextScene("game")
            elif self._selected == 2:
                raise StopApplication("Quit from menu")
        elif key in (ord("q"), ord("Q")):
            raise StopApplication("Quit from menu")

        return None  # consume all keyboard events

    def _update(self, frame_no):
        # Render only -- input is handled by process_event
        self._screen.clear_buffer(7, 0, 0)
        w = self._screen.width
        h = self._screen.height

        # Title art
        title_y = h // 4 - len(sprites.TITLE_ART) // 2
        for i, line in enumerate(sprites.TITLE_ART):
            x = (w - len(line)) // 2
            color = config.COLOR_TITLE if frame_no % 10 < 7 else config.COLOR_CHICKEN
            self._screen.print_at(line, max(0, x), max(1, title_y + i),
                                  colour=color, attr=Screen.A_BOLD)

        # Subtitle
        sub_y = title_y + len(sprites.TITLE_ART) + 2
        sx = (w - len(sprites.SUBTITLE)) // 2
        self._screen.print_at(sprites.SUBTITLE, max(0, sx), sub_y,
                              colour=config.COLOR_HUD)

        # Chicken decoration
        chicken_y = sub_y + 2
        for i, line in enumerate(sprites.CHICKEN):
            cx1 = w // 4 - sprites.CHICKEN_WIDTH // 2
            cx2 = 3 * w // 4 - sprites.CHICKEN_WIDTH // 2
            self._screen.print_at(line, cx1, chicken_y + i, colour=config.COLOR_CHICKEN)
            self._screen.print_at(line, cx2, chicken_y + i, colour=config.COLOR_CHICKEN)

        # Menu options
        menu_y = h // 2 + 2
        for i, option in enumerate(sprites.MENU_OPTIONS):
            x = (w - len(option)) // 2
            if i == self._selected:
                color = config.COLOR_SCORE
                attr = Screen.A_BOLD
                self._screen.print_at(">", x - 2, menu_y + i * 2, colour=color, attr=attr)
            else:
                color = config.COLOR_HUD
                attr = Screen.A_NORMAL
            self._screen.print_at(option, x, menu_y + i * 2, colour=color, attr=attr)

        # Footer
        footer = "Arrow keys / WASD to navigate, SPACE/ENTER to select"
        fx = (w - len(footer)) // 2
        self._screen.print_at(footer, max(0, fx), h - 2, colour=240)

        self._screen.refresh()
