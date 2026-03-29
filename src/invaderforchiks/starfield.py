"""Starfield background -- twinkling stars for outer-space ambiance."""

import random

# Star layers: (character, 256-color index, spawn weight)
# Ordered dimmest to brightest.  Weights control relative frequency.
_STAR_POOL = [
    (".", 236, 35),   # barely visible specks
    (".", 240, 25),   # dim dots
    ("+", 245, 15),   # small stars
    ("+", 250, 10),   # bright small stars
    ("*", 255,  8),   # bright white stars
    ("*", 226,  4),   # rare yellow giants
    (".", 244,  3),   # bluish dim (variety)
]

_CHARS, _COLORS, _WEIGHTS = zip(*_STAR_POOL)

# What fraction of screen cells are stars
DENSITY = 0.015


class Starfield:
    """Pre-generated star positions with per-frame twinkling."""

    def __init__(self, width, height, y_min=0, y_max=None, seed=None):
        self.width = width
        self.height = height
        self.y_min = y_min
        self.y_max = y_max if y_max is not None else height
        self._rng = random.Random(seed)
        self.stars = []          # [(x, y, char, color), ...]
        self._generate()

    def _generate(self):
        total = self.width * (self.y_max - self.y_min)
        count = max(1, int(total * DENSITY))
        for _ in range(count):
            x = self._rng.randint(0, self.width - 1)
            y = self._rng.randint(self.y_min, self.y_max - 1)
            idx = self._rng.choices(range(len(_STAR_POOL)), weights=_WEIGHTS, k=1)[0]
            self.stars.append([x, y, _CHARS[idx], _COLORS[idx]])

    def render(self, screen, frame_no=0):
        """Draw stars onto screen.  Call before any game objects."""
        for star in self.stars:
            x, y, char, color = star
            # Twinkle: 2% chance per star per frame to flicker
            if frame_no and self._rng.random() < 0.02:
                # Swap between dim/bright momentarily
                star[3] = 236 if color > 240 else 250
            else:
                # Restore original would be complex; just keep current
                pass
            screen.print_at(char, x, y, colour=star[3])
