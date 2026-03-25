# Pitfalls

When you fix a bug or discover non-obvious behavior, add an entry here.
Each entry: symptom, cause, fix, commit. 4 lines. Takes 30 seconds.
Saves hours for the next agent.

---

### asciimatics stop_frame=0 means "run forever", not "stop now"
- Symptom: Game wouldn't stop when setting stop_frame to 0
- Cause: In asciimatics, Effect.stop_frame returning 0 means no specific end. Use `raise StopApplication` to exit.
- Fix: Changed quit logic to `raise StopApplication("Player quit")` instead of setting stop_frame
- Commit: 89e6f37

### Egg spam rate too high kills player instantly
- Symptom: Player dies within 1-2 seconds of game starting, impossible to play
- Cause: CHICKEN_SHOOT_CHANCE=0.02 with 32 chickens at 20fps = ~13 eggs/second, unhittable
- Fix: Reduced to 0.003 (~1.4 eggs/sec), reduced rows from 4 to 3, added 60-frame grace period
- Commit: 6d29591

### Scene reset() must reinitialize game state
- Symptom: After dying and returning to title, pressing START shows stale game-over screen
- Cause: asciimatics calls reset() on scene transition, but our reset() was a no-op, so old _game_over=True persisted
- Fix: Made reset() call _init_game() to fully reinitialize
- Commit: 6d29591

### Input buffer causes unwanted actions on scene transitions
- Symptom: Pressing SPACE on title screen also fires a bullet in the game scene
- Cause: Key events are buffered; the SPACE that started the game was also consumed by the game scene
- Fix: Drain input buffer with `while self._screen.get_event() is not None: pass` in _init_game()
- Commit: 6d29591

### CRITICAL: asciimatics default handler steals SPACE and Q keys
- Symptom: Arrow keys, A/D, and SPACE do nothing in-game. SPACE sends player back to title menu.
- Cause: screen.play() calls get_event() and passes events to scene.process_event() THEN to _unhandled_event_default(). Our effects didn't implement process_event(), so ALL keys were "unhandled". The default handler maps SPACE->NextScene (back to title!) and Q->StopApplication.
- Fix: Implement process_event() on both GameScene and TitleScreen to consume keyboard events (return None). Set safe_to_default_unhandled_input=False. Move ALL input handling from _update() to process_event(). Never call get_event() manually inside _update().
- Commit: 4591bf3
