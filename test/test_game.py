"""Tests for game logic -- collision detection, scoring, player mechanics."""

import pytest

from invaderforchiks.player import Player
from invaderforchiks.enemies import Chicken, Formation
from invaderforchiks.projectiles import Bullet, Egg, Explosion, PowerUp
from invaderforchiks.game import GameScene
from invaderforchiks import config


class TestCollision:
    """Test AABB collision detection."""

    def test_overlapping_rects(self):
        assert GameScene._overlaps(0, 0, 5, 5, 3, 3, 5, 5) is True

    def test_non_overlapping_rects(self):
        assert GameScene._overlaps(0, 0, 5, 5, 10, 10, 5, 5) is False

    def test_adjacent_rects_no_overlap(self):
        assert GameScene._overlaps(0, 0, 5, 5, 5, 0, 5, 5) is False

    def test_contained_rect(self):
        assert GameScene._overlaps(0, 0, 10, 10, 2, 2, 3, 3) is True

    def test_single_point_overlap(self):
        assert GameScene._overlaps(0, 0, 1, 1, 0, 0, 1, 1) is True


class TestPlayer:
    """Test player mechanics."""

    def test_initial_state(self):
        p = Player(80, 24)
        assert p.lives == config.PLAYER_START_LIVES
        assert p.weapon_level == 0

    def test_move_left_bounded(self):
        p = Player(80, 24)
        p.x = 0
        p.press_direction(-1)
        p.tick()
        assert p.x == 0

    def test_move_right_bounded(self):
        p = Player(80, 24)
        p.x = 80 - p.width
        p.press_direction(1)
        p.tick()
        assert p.x == 80 - p.width

    def test_velocity_movement(self):
        p = Player(80, 24)
        start_x = p.x
        p.press_direction(1)
        p.tick()
        assert p.x > start_x  # ship moved right

    def test_reaches_max_speed(self):
        """Ship ramps up to max speed after enough frames."""
        p = Player(80, 24)
        for _ in range(10):
            p.press_direction(1)
            p.tick()
        assert p.vx == config.PLAYER_SPEED

    def test_smooth_direction_change(self):
        """Switching directions transitions smoothly -- no stuck-in-place."""
        p = Player(80, 24)
        p.x = 40
        # Build leftward velocity
        for _ in range(5):
            p.press_direction(-1)
            p.tick()
        # Switch to right, keep pressing
        for _ in range(10):
            p.press_direction(1)
            p.tick()
        assert p.vx > 0  # now moving right

    def test_movement_auto_stops(self):
        """Ship stops after decay frames with no key input."""
        p = Player(80, 24)
        p.press_direction(1)
        # Tick well past the initial input window + decel
        for _ in range(20):
            p.tick()
        pos = p.x
        p.tick()
        assert p.x == pos  # stopped

    def test_stop_immediate(self):
        p = Player(80, 24)
        p.press_direction(1)
        p.tick()
        moved_x = p.x
        p.stop()
        p.tick()
        assert p.x == moved_x  # didn't move further

    def test_shield_absorbs_hit(self):
        p = Player(80, 24)
        p.shield_timer = 50
        initial_lives = p.lives
        dead = p.hit()
        assert dead is False
        assert p.lives == initial_lives  # no life lost
        assert p.shield_timer == 0  # shield broke

    def test_shoot_creates_bullet(self):
        p = Player(80, 24)
        bullets = p.try_shoot()
        assert len(bullets) == 1
        assert bullets[0]["dy"] < 0  # moves upward

    def test_shoot_cooldown(self):
        p = Player(80, 24)
        p.try_shoot()
        assert p.try_shoot() == []  # on cooldown

    def test_cooldown_resets(self):
        p = Player(80, 24)
        p.try_shoot()
        for _ in range(config.BULLET_COOLDOWN):
            p.tick()
        bullets = p.try_shoot()
        assert len(bullets) == 1

    def test_hit_reduces_lives(self):
        p = Player(80, 24)
        initial = p.lives
        p.hit()
        assert p.lives == initial - 1

    def test_hit_gives_invincibility(self):
        p = Player(80, 24)
        p.hit()
        assert p.invincible_timer > 0
        dead = p.hit()  # should not take damage
        assert dead is False
        assert p.lives == config.PLAYER_START_LIVES - 1

    def test_death_on_zero_lives(self):
        p = Player(80, 24)
        p.lives = 1
        dead = p.hit()
        assert dead is True
        assert p.lives == 0

    def test_weapon_upgrade(self):
        p = Player(80, 24)
        p.upgrade_weapon()
        assert p.weapon_level == 1

    def test_weapon_upgrade_cap(self):
        p = Player(80, 24)
        for _ in range(20):
            p.upgrade_weapon()
        assert p.weapon_level == config.WEAPON_MAX_LEVEL

    def test_dual_shot_at_level_1(self):
        p = Player(80, 24)
        p.upgrade_weapon()  # level 1
        bullets = p.try_shoot()
        assert len(bullets) == 2

    def test_spread_shot_at_level_2(self):
        p = Player(80, 24)
        p.upgrade_weapon()
        p.upgrade_weapon()  # level 2
        bullets = p.try_shoot()
        assert len(bullets) == 3


class TestChicken:
    """Test chicken enemy mechanics."""

    def test_regular_chicken_one_hit_kill(self):
        c = Chicken(10, 10, "regular")
        assert c.hit() is True
        assert c.alive is False

    def test_armored_chicken_two_hits(self):
        c = Chicken(10, 10, "armored")
        assert c.hit() is False  # first hit
        assert c.alive is True
        assert c.hit() is True   # second hit
        assert c.alive is False

    def test_chicken_points(self):
        r = Chicken(0, 0, "regular")
        a = Chicken(0, 0, "armored")
        b = Chicken(0, 0, "bomber")
        assert r.points == config.CHICKEN_POINTS
        assert a.points == config.CHICKEN_POINTS * 2
        assert b.points == config.CHICKEN_POINTS * 3


class TestFormation:
    """Test chicken formation mechanics."""

    def test_formation_creates_chickens(self):
        f = Formation(1, 80)
        assert len(f.chickens) > 0

    def test_all_dead_when_empty(self):
        f = Formation(1, 80)
        for c in f.chickens:
            c.alive = False
        assert f.all_dead is True

    def test_not_all_dead_with_survivors(self):
        f = Formation(1, 80)
        assert f.all_dead is False


class TestBullet:
    """Test projectile mechanics."""

    def test_bullet_moves_up(self):
        b = Bullet(10, 10, dy=-1)
        b.tick()
        assert b.y == 9

    def test_bullet_dies_off_screen(self):
        b = Bullet(10, 0, dy=-1)
        b.tick()
        assert b.alive is False


class TestEgg:
    """Test enemy projectile."""

    def test_egg_moves_down(self):
        e = Egg(10, 10)
        e.tick(24)
        assert e.y == 11

    def test_egg_dies_off_screen(self):
        e = Egg(10, 23)
        e.tick(24)
        assert e.alive is False


class TestExplosion:
    """Test explosion animation."""

    def test_explosion_eventually_dies(self):
        ex = Explosion(10, 10)
        for _ in range(100):
            ex.tick()
        assert ex.alive is False


class TestPowerUp:
    """Test power-up drops."""

    def test_powerup_falls(self):
        p = PowerUp(10, 10)
        p.tick(24)
        assert p.y == 10 + config.POWERUP_FALL_SPEED

    def test_powerup_dies_off_screen(self):
        p = PowerUp(10, 23)
        p.tick(24)
        assert p.alive is False
