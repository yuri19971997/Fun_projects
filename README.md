# Invader for Chicks

The galaxy is being seasoned, and Earth is on the menu.
You are the only thing standing between humanity and a tide of intergalactic poultry.


**Terminal shoot-em-up**

## Install & Play

```bash
# From source
git clone <repo-url>
cd invaderForChiks
uv sync
uv run invaderforchiks

# Or install from PyPI (coming soon)
uv tool install invaderforchiks
invaderforchiks
```

## Controls

| Key | Action |
|-----|--------|
| Left/Right arrows | Move ship |
| Space | Shoot |
| P | Pause |
| Q | Quit |

## Features

- 20 waves of chicken mayhem + 4 unique boss fights
- Full ASCII art with 256-color visuals
- Combo scoring system -- chain kills for multipliers
- Weapon upgrade path from pea-shooter to homing missiles
- Random power-up drops (drumsticks, shields, extra lives)
- Classic 3-lives system
- 15-30 minute gameplay sessions

## Requirements

- Python 3.12+
- Terminal with 256-color support (most modern terminals)
- Minimum 80x24 terminal size

## Development

```bash
uv sync           # Install dependencies
uv run pytest     # Run tests
uv run invaderforchiks  # Play!
```

See `AGENTS.md` for project conventions and `HANDOFF.md` for current state.
