# Invader for Chiks -- Project Rules

> **You don't have memory. These files do.** Everything you learn this session
> is lost when it ends. Write to `HANDOFF.md` (current state), `PITFALLS.md`
> (lessons learned), and `CHANGELOG.md` (history). These files are your memory.

Read in order: `HANDOFF.md`, `PITFALLS.md`, this file. For reasoning: `WHY.md`.

---

## What This Is

**One sentence:** A terminal shoot-em-up (TUI) where you defend Earth from waves of invading space chickens, built with Python + asciimatics.

**"Done" definition:**
```bash
uv run invaderforchiks
# Expected: Game launches in terminal, title screen appears, gameplay is playable through 20 waves + 4 bosses
```

---

## Critical Rules

1. Comedy is the identity -- every feature should make the player smile or laugh
2. Gameplay feel first -- tight controls, responsive input, smooth animation before any new features
3. Test game logic (collision, scoring, wave progression) with automated tests. Visual stuff is tested manually.
4. All ASCII art sprites go in `src/invaderforchiks/sprites.py` -- single source of truth
5. Game constants (speeds, damage, spawn rates) go in `src/invaderforchiks/config.py` -- easy to tune

---

## Code Conventions

- Language: Python 3.12+
- Package manager: uv
- TUI framework: asciimatics 1.15+
- Build system: hatchling
- Warnings: zero warnings policy (run with `-W error` in tests)
- Entry point: `src/invaderforchiks/__main__.py`
- Naming: snake_case for everything, ALL_CAPS for game constants

---

## Testing

```bash
uv run pytest
```

### Performance baselines
```
FPS: >= 30 (smooth animation)
Input latency: < 50ms (responsive controls)
Memory: < 50MB (terminal game, should be tiny)
```

---

## Game Design Summary

| Aspect | Decision |
|--------|----------|
| Identity | Full comedy (chickens, eggs, drumsticks, absurd humor) |
| Session | 15-30 min runs |
| Waves | 20 waves + unique boss every 5th wave |
| Lives | Classic 3 lives, extra lives from score milestones |
| Weapons | Linear upgrade path (pea-shooter -> spread -> laser -> rapid -> homing) |
| Progression | Random drops during gameplay |
| Enemies | All chickens (regular, armored, bomber, kamikaze, boss) |
| Scoring | Combo multiplier (rapid kills chain) |
| Visuals | Full ASCII art + 256 color palette + effects |
| HUD | Top bar (score/lives) + bottom bar (weapon/wave/combo) |
| Distribution | PyPI installable + source runnable |

---

## Known Limitations

- Terminal must support 256 colors for best visuals
- Minimum terminal size: 80x24 (standard)
- No sound (terminal limitation -- we fake it with visual humor)
