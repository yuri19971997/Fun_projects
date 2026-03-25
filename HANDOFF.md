# HANDOFF.md -- Current state of the project

> **New here?** Read in order: this file, then `PITFALLS.md`, then `AGENTS.md`. For reasoning: `WHY.md`.

Last updated: 2026-03-25. If anything here contradicts reality, fix this file.

---

## What is this?

**Invader for Chiks** is a terminal-based shoot-em-up (TUI) where you defend Earth from waves of invading space chickens. Built with Python + asciimatics. Combines Space Invaders mechanics with Chicken Invaders humor. Full comedy tone -- chickens, eggs, drumsticks, absurd humor.

## Before you write any code

```bash
cd ~/projects/invaderForChiks
uv sync                      # Install dependencies
uv run pytest                # Run tests (35 tests, all should pass)
uv run invaderforchiks       # Launch the game
```

---

## What works (verified 2026-03-25)

### Core gameplay
- Title screen with animated menu (arrow keys / WASD + SPACE/ENTER)
- Player ship with velocity-based movement + auto-stop decay (no infinite sliding)
- Direct shooting: each SPACE press = one shot, hold SPACE for rapid fire via terminal key repeat
- 3 weapon levels: Pea Shooter, Dual Shot, Spread Shot (+ 3 more defined but not fully differentiated)
- Chicken formation that marches Space Invaders-style and shoots eggs
- 4 chicken types: regular, armored (2 hits), bomber (shoots more), kamikaze
- AABB collision detection (bullets->chickens, eggs->player, player->powerups)
- Scoring with combo multiplier (chain kills within 30 frames)
- Power-up drops with clear labels and distinct colors:
  - `<GUN UP>` orange -- weapon upgrade
  - `< +1 HP>` green -- extra life
  - `<SHIELD>` cyan -- absorbs one hit, shows visual on ship + HUD
  - `< BOOM >` red -- kills 3 random chickens
- 20-wave structure with difficulty scaling per wave
- Grace period (60 frames) at start of each wave -- no enemy fire during banner
- Game over screen with score + restart (SPACE) or quit (Q)
- Extra lives from score milestones (every 5000 points)

### Visual
- Full ASCII art sprites for ship, chickens (4 types), bosses (4 defined), explosions (3-frame animation)
- 256-color palette with distinct colors per element
- Shield indicator: ship sprite changes to cyan bubble `(^)/(/ \)/(_____)` + HUD shows `[SHIELD ACTIVE]`
- HUD: top bar (score/lives/wave), bottom bar (weapon name/shield/combo), separator lines

### Technical
- Python 3.12+ with asciimatics 1.15
- Package installable via `uv run invaderforchiks` or `python -m invaderforchiks`
- 35 automated tests covering collision, player mechanics, enemy types, projectiles, power-ups, shield, movement decay
- Project docs from agent-project-template (AGENTS.md, HANDOFF.md, PITFALLS.md, CHANGELOG.md, WHY.md)
- Git hooks configured, 7 commits on master

### Controls
| Key | Action |
|-----|--------|
| A/D or Left/Right | Move (auto-stops when you stop pressing) |
| S or Down | Instant stop |
| Space | Shoot (hold for rapid fire) |
| P | Pause |
| Q | Quit |

---

## Architecture

```
src/invaderforchiks/
  __init__.py       # Package init, version
  __main__.py       # Entry point: Screen.wrapper -> scene management (title + game)
  game.py           # GameScene(Effect): process_event for input, _update for logic, _render for display
  title.py          # TitleScreen(Effect): animated menu with scene transitions
  player.py         # Player class: velocity movement with decay, shooting, shield, weapon levels
  enemies.py        # Chicken + Formation: 4 types, grid movement, egg spawning
  projectiles.py    # Bullet, Egg, Explosion (animated), PowerUp (typed + colored)
  hud.py            # render_top_bar, render_bottom_bar, render_wave_banner, render_game_over
  config.py         # ALL tunable constants (speeds, rates, colors, sizes)
  sprites.py        # ALL ASCII art (ship, chickens, bosses, explosions, power-ups, title art)
```

### Key architecture decisions
- **Input via process_event()** -- NOT get_event() in _update(). asciimatics' play() loop consumes events before _update runs. process_event() returns None to prevent default handler from stealing SPACE/Q keys.
- **safe_to_default_unhandled_input = False** on both effects to disable asciimatics' default key handler
- **frame_update_count = 1** forces screen refresh every frame for smooth animation
- **Movement decay timer** (3 frames) simulates key-release in terminal where key-up events don't exist
- **Config.py is the single tuning file** -- all gameplay numbers in one place

---

## Build & deploy

```bash
uv sync                       # Install dependencies
uv run invaderforchiks         # Run the game
uv run pytest                  # Run tests
uv build                       # Build distributable package
```

---

## Known limitations

- Weapon levels 3-5 (Rapid Fire, Laser Beam, Homing Eggs) not yet differentiated in shooting mechanics -- they all use the spread shot pattern
- Boss fights not implemented (bosses defined in sprites.py but no boss gameplay logic)
- No high score persistence (scores lost on quit)
- No sound (terminal limitation)
- No endless mode yet (only 20-wave story mode)
- Terminal must support 256 colors; minimum 80x24

## Future work (priority order)

1. **Differentiate weapon levels 3-5** -- Rapid Fire (lower cooldown), Laser Beam (piercing), Homing Eggs (auto-aim)
2. **Boss fights** -- Unique behavior for waves 5, 10, 15, 20 using existing boss sprites
3. **High score persistence** -- Save top scores to ~/.invaderforchiks/scores.json
4. **Endless mode** -- Unlocked after completing wave 20
5. **More wave patterns** -- V-formations, spiral entry, dive attacks
6. **Screen shake / flash effects** on big explosions
7. **Overheat mechanic** -- Hold fire too long and weapon overheats temporarily

---

## How to resume this project

Copy this prompt to start a new agent session:

```
Read HANDOFF.md and PITFALLS.md in ~/projects/invaderForChiks.
Run `uv run pytest` to verify tests pass.
Run `uv run invaderforchiks` briefly to confirm the game launches.

For each future work item (in priority order):
1. Investigate -- read the relevant code, understand the current state
2. Plan -- break into tasks with pass conditions. Write them to the todo list.
3. Implement -- one task at a time. Test after each. Commit after each.
4. Update HANDOFF.md. Add PITFALLS.md entries for any bugs found.

Key files to read first: config.py (all tuning), game.py (main loop),
player.py (controls), enemies.py (chicken behavior).

CRITICAL: Input handling MUST use process_event(), never get_event().
See PITFALLS.md for why.
```
