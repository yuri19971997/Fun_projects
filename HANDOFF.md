# HANDOFF.md -- Current state of the project

> **New here?** Read in order: this file, then `PITFALLS.md`, then `AGENTS.md`. For reasoning: `WHY.md`.

Last updated: 2026-03-25. If anything here contradicts reality, fix this file.

---

## What is this?

Invader for Chiks is a terminal-based shoot-em-up where you defend Earth from waves of invading space chickens. Built with Python + asciimatics, it combines Space Invaders mechanics with Chicken Invaders humor in a TUI.

## Before you write any code

```bash
# Pre-flight checks:
cd ~/projects/invaderForChiks
uv sync                      # Install dependencies
uv run pytest                # Run tests
uv run invaderforchiks       # Launch the game
```

---

## What works (verified 2026-03-25)

- Project scaffolding (pyproject.toml, package structure, git, hooks)
- Asciimatics dependency installed
- Template docs in place (AGENTS.md, HANDOFF.md, PITFALLS.md, CHANGELOG.md)

---

## Build & deploy

```bash
uv sync                       # Install dependencies
uv run invaderforchiks         # Run the game
uv run pytest                  # Run tests
uv build                       # Build distributable package
```

---

## Architecture

```
src/invaderforchiks/
  __init__.py       # Package init
  __main__.py       # Entry point (main function)
  game.py           # Core game scene and loop
  player.py         # Player ship sprite and logic
  enemies.py        # Chicken enemy types and formations
  projectiles.py    # Bullets, eggs, missiles
  powerups.py       # Drop items and weapon upgrades
  hud.py            # Score, lives, weapon, combo display
  config.py         # Game constants (speeds, damage, timing)
  sprites.py        # All ASCII art definitions
  title.py          # Title screen / menu
```

---

## Known limitations

- Phase 1 MVP: only basic gameplay (no bosses, no power-ups yet)

## Future work

1. Phase 1: MVP -- game loop, player ship, chicken formation, collision, scoring, game over
2. Phase 2: Core Fun -- multiple wave patterns, egg projectiles, power-up drops, difficulty escalation
3. Phase 3: Polish -- ASCII art, colors, boss fights, title screen, high scores
4. Phase 4: Delight -- weapon upgrades, combo system, overheat, endless mode

---

## How to resume this project

Copy this prompt to start a new agent session:

```
Read HANDOFF.md and PITFALLS.md. Run the tests. For each future work
item (in priority order):
1. Investigate -- read the relevant code, understand the current state
2. Plan -- break into tasks with function names, pass conditions, and
   dependency order. Write them to the todo list.
3. Implement -- one task at a time. Test after each. Commit after each.
4. Update HANDOFF.md. Add PITFALLS.md entries for any bugs found.

If you discover improvements not on the list, apply the same 4 steps.
If you hit friction, fix the process not just the symptom.
Keep going until the todo list is empty.
```
