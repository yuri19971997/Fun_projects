# HANDOFF.md -- Current state of the project

> **New here?** Read in order: this file, then `PITFALLS.md`, then `AGENTS.md`. For reasoning: `WHY.md`.

Last updated: 2026-03-29. If anything here contradicts reality, fix this file.

---

## What is this?

**Invader for Chiks** is a terminal-based shoot-em-up (TUI) where you defend Earth from waves of invading space chickens. Built with Python + asciimatics. Combines Space Invaders mechanics with Chicken Invaders humor. Full comedy tone -- chickens, eggs, drumsticks, absurd humor.

## Before you write any code

```bash
cd ~/projects/invaderForChiks
uv sync                      # Install dependencies
uv run pytest                # Run tests (37 tests, all should pass)
uv run invaderforchiks       # Launch the game
uv run invaderforchiks --wave 5   # Skip to boss fight for testing
```

---

## What works (verified 2026-03-29)

### Core gameplay
- Title screen with animated menu (arrow keys / WASD + SPACE/ENTER)
- Player ship with instant direction changes + smooth deceleration on release
- Two-tier input window: INITIAL=8 (400ms) for new direction, REPEAT=2 (100ms) for held key
- SPACE keeps momentum alive (keep_moving) so shooting doesn't stop the ship
- 6 fully differentiated weapon levels:
  - Level 0: Pea Shooter (1 bullet)
  - Level 1: Dual Shot (2 parallel)
  - Level 2: Spread Shot (3-way fan)
  - Level 3: Rapid Fire (3-way + 2x fire rate)
  - Level 4: Laser Beam (5-way wide + 2x fire rate)
  - Level 5: Homing Eggs (5-way + max fire rate + faster bullets)
- Chicken formation that marches Space Invaders-style and shoots eggs
- 4 chicken types: regular, armored (2 hits), bomber (shoots more), kamikaze
- **4 boss fights** on waves 5, 10, 15, 20 with unique attacks:
  - Rooster General (30HP, 3-way spread, enrages at 50%)
  - Egg Mother (50HP, cluster bombs, wider clusters at 50%)
  - Colonel Cluck (70HP, rapid singles + egg walls, faster at 50%)
  - Supreme Hen (100HP, sinusoidal movement, spreads + rain + bursts)
  - All bosses have HP bar + name display, drop 3 power-ups on death
  - Boss eggs support diagonal movement (dx parameter)
- AABB collision detection (bullets->chickens/bosses, eggs->player, player->powerups)
- Scoring with combo multiplier (chain kills within 30 frames)
- Power-up drops with visual icons:
  - `▄█▀═══▸` orange -- weapon upgrade (gun silhouette)
  - `♥ LIFE ♥` green -- extra life (hearts)
  - `(█╋█)` cyan -- shield (shield icon)
  - `▄▀★▀▄` red -- boom, kills 3 random chickens (explosion icon)
- 20-wave structure with difficulty scaling per wave
- Grace period (60 frames) at start of each wave -- no enemy fire during banner
- Game over screen with score + restart (SPACE) or quit (Q)
- Extra lives from score milestones (every 5000 points)
- `--wave N` flag to start at any wave (skips title screen)

### Visual
- **Pixel-art sprites** using Unicode block characters (█▀▄▐▌) with per-character 256-color rendering
- Player ship: tapered fighter silhouette (cyan weapon, green hull, yellow engines)
- 4 chicken types: distinct block-char silhouettes with type-specific colors
- 4 boss sprites: large (13-17 wide), color-coded (red/white/silver/gold)
- Twinkling starfield background (7 star types, 2% twinkle rate per frame)
- HUD: top bar (score/♥ lives/wave), bottom bar (weapon name/shield/combo)
- Shield: ship glows cyan + HUD shows [SHIELD ACTIVE]
- Explosion: 3-frame \\|/--*-- starburst animation

### Technical
- Python 3.12+ with asciimatics 1.15
- Package installable via `uv run invaderforchiks` or `python -m invaderforchiks`
- 37 automated tests covering collision, player mechanics, enemy types, projectiles, power-ups, shield, movement, direction changes
- Rich sprite format: list of (chars, colors) per row for per-character coloring

### Controls
| Key | Action |
|-----|--------|
| A/D or Left/Right | Move (instant direction change, auto-stops on release) |
| S or Down | Instant stop |
| Space | Shoot (hold for rapid fire) |
| P | Pause |
| Q | Quit |

---

## Architecture

```
src/invaderforchiks/
  __init__.py       # Package init, version
  __main__.py       # Entry point: argparse (--wave), Screen.wrapper -> scene management
  game.py           # GameScene(Effect): process_event for input, _update for logic, _render for display
  title.py          # TitleScreen(Effect): animated menu with scene transitions
  player.py         # Player class: instant vx on keypress, two-tier input window, 6 weapon levels
  enemies.py        # Chicken + Formation + Boss: 4 chicken types, 4 boss types with unique attacks
  projectiles.py    # Bullet, Egg (with dx for diagonal), Explosion (animated), PowerUp
  hud.py            # render_top_bar, render_bottom_bar, render_wave_banner, render_game_over
  config.py         # ALL tunable constants (speeds, rates, colors, sizes)
  sprites.py        # ALL sprites: rich format (block chars + per-char colors), plain fallbacks
  starfield.py      # Twinkling star background for space ambiance
```

### Key architecture decisions
- **Input via process_event()** -- NOT get_event() in _update(). See PITFALLS.md.
- **safe_to_default_unhandled_input = False** on both effects
- **frame_update_count = 1** forces screen refresh every frame
- **Instant vx on keypress** -- press_direction() sets vx directly for zero-delay direction changes
- **Two-tier input window** -- INITIAL (400ms) for new direction, REPEAT (100ms) for held key
- **keep_moving()** refreshes timer to REPEAT on SPACE so shooting doesn't stop the ship
- **Boss duck-types as Formation** -- same interface (alive_chickens, all_dead, tick, render) so game loop needs minimal changes
- **Rich sprite format** -- (chars_string, color_list) per row for per-character 256-color rendering
- **Config.py is the single tuning file** -- all gameplay numbers in one place

---

## Build & deploy

```bash
uv sync                              # Install dependencies
uv run invaderforchiks               # Run the game
uv run invaderforchiks --wave 5      # Jump to first boss
uv run pytest                        # Run tests (37 should pass)
uv build                             # Build distributable package
```

---

## Known limitations

- No high score persistence (scores lost on quit)
- No sound (terminal limitation)
- No endless mode yet (only 20-wave story mode)
- Terminal must support 256 colors and Unicode block chars; minimum 80x24

## Future work (priority order)

1. **High score persistence** -- Save top scores to ~/.invaderforchiks/scores.json
2. **Endless mode** -- Unlocked after completing wave 20
3. **More wave patterns** -- V-formations, spiral entry, dive attacks
4. **Screen shake / flash effects** on big explosions
5. **Overheat mechanic** -- Hold fire too long and weapon overheats temporarily
6. **Boss polish** -- More dramatic death animations, phase transition effects

---

## How to resume this project

Copy this prompt to start a new agent session:

```
We are working on ~/projects/invaderForChiks -- a TUI Space Invaders game with chickens.

Read these files in order:
- ~/projects/invaderForChiks/HANDOFF.md (current state, architecture, what works, what's next)
- ~/projects/invaderForChiks/PITFALLS.md (critical bugs we already solved)
- ~/projects/invaderForChiks/AGENTS.md (project rules and game design decisions)

Then run:
- uv run pytest (should be 37 passing)
- uv run invaderforchiks (confirm it launches)

After reading, tell me what you understand about where we are and what's next.
Then we continue from the "Future work" list in HANDOFF.md.
```
