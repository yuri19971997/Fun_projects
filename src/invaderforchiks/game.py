"""Core game scene -- ties everything together."""

import random

from asciimatics.effects import Effect
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import StopApplication
from asciimatics.screen import Screen

from . import config, hud, sprites
from .enemies import Formation
from .player import Player
from .projectiles import Bullet, Egg, Explosion, PowerUp


class GameScene(Effect):
    """Main gameplay effect -- handles the full game loop."""

    # Prevent asciimatics default handler from stealing our keys
    safe_to_default_unhandled_input = False

    def __init__(self, screen):
        super().__init__(screen)
        self._game_over = False
        self._paused = False
        self._wave_banner_timer = 0
        self._init_game()

    def _init_game(self):
        """Initialize/reset all game state."""
        w = self._screen.width
        h = self._screen.height
        self.player = Player(w, h)
        self.bullets = []
        self.eggs = []
        self.explosions = []
        self.powerups = []
        self.score = 0
        self.wave = 1
        self.combo = 0
        self.combo_timer = 0
        self.formation = Formation(self.wave, w, y_offset=3)
        self._game_over = False
        self._wave_banner_timer = 60  # grace period: no enemy fire during banner

    def reset(self):
        """Called on scene transition -- reinitialize the game."""
        self._init_game()

    @property
    def stop_frame(self):
        return 0  # 0 = run forever in asciimatics

    @property
    def frame_update_count(self):
        # Force screen refresh every frame for smooth animation
        return 1

    def process_event(self, event):
        """Handle keyboard input. Return None to consume, event to pass through."""
        if not isinstance(event, KeyboardEvent):
            return event

        key = event.key_code

        if self._game_over:
            if key == ord(" "):
                self._init_game()
                return None
            elif key in (ord("q"), ord("Q")):
                raise StopApplication("Player quit")
            return None  # consume all keys on game over screen

        if key in (ord("q"), ord("Q")):
            raise StopApplication("Player quit")
        elif key in (ord("p"), ord("P")):
            self._paused = not self._paused
            return None
        elif not self._paused:
            if key in (Screen.KEY_LEFT, ord("a"), ord("A")):
                self.player.set_direction(-1)
                return None
            elif key in (Screen.KEY_RIGHT, ord("d"), ord("D")):
                self.player.set_direction(1)
                return None
            elif key in (Screen.KEY_DOWN, ord("s"), ord("S")):
                self.player.set_direction(0)
                return None
            elif key == ord(" "):
                # Direct fire: each SPACE press = one shot attempt
                new_bullets = self.player.try_shoot()
                for b in new_bullets:
                    self.bullets.append(Bullet(b["x"], b["y"], b["dx"], b["dy"], b["char"]))
                return None

        return None  # consume all keys during gameplay

    def _update_state(self, frame_no):
        if self._paused or self._game_over:
            return

        self.player.tick()

        # Wave banner countdown
        if self._wave_banner_timer > 0:
            self._wave_banner_timer -= 1

        # Move bullets
        for b in self.bullets:
            b.tick()
        self.bullets = [b for b in self.bullets if b.alive]

        # Move eggs
        for e in self.eggs:
            e.tick(self._screen.height - 2)
        self.eggs = [e for e in self.eggs if e.alive]

        # Move powerups
        for p in self.powerups:
            p.tick(self._screen.height - 2)
        self.powerups = [p for p in self.powerups if p.alive]

        # Tick explosions
        for ex in self.explosions:
            ex.tick()
        self.explosions = [ex for ex in self.explosions if ex.alive]

        # Formation movement + egg spawning (no eggs during grace period)
        if self._wave_banner_timer <= 0:
            new_eggs = self.formation.tick(frame_no)
            for e in new_eggs:
                self.eggs.append(Egg(e["x"], e["y"], e["dy"]))

        # Combo decay
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo = 0

        # Check if wave is cleared
        if self.formation.all_dead and self._wave_banner_timer <= 0:
            self._next_wave()

    def _next_wave(self):
        if self.wave >= config.TOTAL_WAVES:
            self._game_over = True
            return
        self.wave += 1
        self.formation = Formation(self.wave, self._screen.width, y_offset=3)
        self._wave_banner_timer = 60  # grace period
        self.eggs.clear()

    def _check_collisions(self):
        if self._paused or self._game_over:
            return

        # Bullets hitting chickens
        for b in self.bullets[:]:
            if not b.alive:
                continue
            for c in self.formation.alive_chickens:
                if self._overlaps(b.x, b.y, b.width, b.height,
                                  c.x, c.y, c.width, c.height):
                    b.alive = False
                    killed = c.hit()
                    if killed:
                        # Score with combo
                        self.combo += 1
                        self.combo_timer = config.COMBO_WINDOW
                        multiplier = min(self.combo, config.COMBO_MULTIPLIER_CAP)
                        self.score += c.points * multiplier

                        # Explosion
                        self.explosions.append(Explosion(c.x + c.width // 2, c.y))

                        # Power-up drop
                        if random.random() < config.POWERUP_DROP_CHANCE:
                            ptype = random.choice(config.POWERUP_TYPES)
                            self.powerups.append(PowerUp(c.x + 1, c.y, ptype))

                        # Extra life check
                        if self.score > 0 and self.score % config.EXTRA_LIFE_SCORE < c.points * multiplier:
                            self.player.lives += 1
                    break

        # Eggs hitting player
        px, py, pw, ph = self.player.x, self.player.y, sprites.PLAYER_WIDTH, sprites.PLAYER_HEIGHT
        for e in self.eggs[:]:
            if not e.alive:
                continue
            if self._overlaps(e.x, e.y, e.width, e.height, px, py, pw, ph):
                e.alive = False
                dead = self.player.hit()
                self.explosions.append(Explosion(self.player.x + pw // 2, self.player.y))
                if dead:
                    self._game_over = True
                    return

        # Chickens reaching player level
        for c in self.formation.alive_chickens:
            if c.y + c.height >= self.player.y:
                self._game_over = True
                return

        # Player collecting powerups
        for p in self.powerups[:]:
            if not p.alive:
                continue
            if self._overlaps(p.x, p.y, p.width, p.height, px, py, pw, ph):
                p.alive = False
                self._apply_powerup(p.ptype)

    def _apply_powerup(self, ptype):
        if ptype == "weapon_up":
            self.player.upgrade_weapon()
        elif ptype == "extra_life":
            self.player.lives += 1
        elif ptype == "shield":
            self.player.invincible_timer = 60  # 3 seconds
        elif ptype == "missile":
            # Kill random 3 chickens
            alive = self.formation.alive_chickens
            targets = random.sample(alive, min(3, len(alive)))
            for t in targets:
                t.alive = False
                self.score += t.points
                self.explosions.append(Explosion(t.x + t.width // 2, t.y))

    @staticmethod
    def _overlaps(x1, y1, w1, h1, x2, y2, w2, h2):
        return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2

    def _render(self, frame_no):
        self._screen.clear_buffer(7, 0, 0)

        if self._game_over:
            hud.render_game_over(self._screen, self.score)
            self._screen.refresh()
            return

        # HUD
        weapon_name = config.WEAPON_NAMES[self.player.weapon_level]
        hud.render_top_bar(self._screen, self.score, self.player.lives, self.wave)
        hud.render_bottom_bar(self._screen, weapon_name, self.combo, self.combo_timer)

        # Wave banner
        if self._wave_banner_timer > 0:
            hud.render_wave_banner(self._screen, self.wave, frame_no)

        # Game objects
        self.formation.render(self._screen)
        for b in self.bullets:
            b.render(self._screen)
        for e in self.eggs:
            e.render(self._screen)
        for ex in self.explosions:
            ex.render(self._screen)
        for p in self.powerups:
            p.render(self._screen)
        self.player.render(self._screen, frame_no)

        # Pause overlay
        if self._paused:
            text = "=== PAUSED ==="
            x = (self._screen.width - len(text)) // 2
            y = self._screen.height // 2
            self._screen.print_at(text, x, y, colour=config.COLOR_HUD, attr=Screen.A_BOLD)

        self._screen.refresh()

    def _update(self, frame_no):
        self._update_state(frame_no)
        self._check_collisions()
        self._render(frame_no)
