# Changelog

One paragraph per milestone. Most recent first. See `git log` for full history.

---

### Boss fights + visual overhaul + movement rework (2026-03-29)
Major session: implemented full boss fight system (4 bosses with unique attacks, HP bars, enrage at 50%), pixel-art visual overhaul (Unicode block characters with per-character 256-color rendering for ship, all 4 chicken types, all 4 bosses), twinkling starfield background, all 6 weapon levels differentiated (rapid fire, 5-way spread, max fire rate), power-up icons (gun silhouette, hearts, shield icon, explosion icon), movement rework (instant direction changes via direct vx setting, two-tier input window, keep_moving for SPACE, ACCEL=SPEED=2 for zero ramp delay), diagonal egg support for boss attacks, `--wave N` flag for testing. 37 tests passing.

### Controls refinement v3 (2026-03-25)
Fixed infinite sliding: movement now auto-stops after 3 frames of no key input. Sped up chickens (2x faster marching, ~3x more eggs). Added shield visual indicator -- ship sprite changes to cyan bubble, HUD shows `[SHIELD ACTIVE]`. Shield absorbs one hit then breaks. 35 tests passing.

### Controls refinement v2 (2026-03-25)
Reduced movement speed (3->1) for precise aiming. Changed shooting from auto-fire toggle back to direct SPACE-per-shot (terminal key repeat handles sustained fire). Power-ups redesigned with clear labels (`<GUN UP>`, `< +1 HP>`, `<SHIELD>`, `< BOOM >`) and distinct per-type colors (orange/green/cyan/red).

### Controls overhaul -- velocity-based movement + auto-fire (2026-03-25)
Replaced tap-per-move with velocity-based movement (press once, ship keeps moving). Added auto-fire toggle. Increased player speed and fire rate. Dramatically improved responsiveness.

### Input handling fix -- process_event (2026-03-25)
Fixed critical bug: SPACE sent player back to title menu instead of shooting. Root cause: asciimatics default handler intercepts unhandled SPACE as NextScene. Fix: implement process_event() on all effects, consume all keyboard events, set safe_to_default_unhandled_input=False. Added A/D and W/S as alternative controls.

### Gameplay balance and bug fixes (2026-03-25)
Reduced egg spam rate (0.02 -> 0.003), reduced formation to 3 rows, added 60-frame grace period at wave start. Fixed scene reset() to reinitialize game state. Fixed input buffer drain on scene transition.

### Initial project setup: Phase 1 MVP (2026-03-25)
Project scaffolded from agent-project-template. Full game architecture: config, sprites, player, enemies, projectiles, HUD, game scene, title screen. 4 chicken types, 6 weapon levels, combo scoring, power-up drops, 20-wave structure, collision detection. 31 tests passing. Research phase: analyzed Space Invaders design principles, Chicken Invaders mechanics, TUI game frameworks (chose asciimatics), arcade game design theory.
