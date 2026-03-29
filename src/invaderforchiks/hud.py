"""HUD -- heads-up display rendering (top bar + bottom bar)."""

from asciimatics.screen import Screen

from . import config


def render_top_bar(screen, score, lives, wave):
    """Top bar: score (left), wave (center), lives (right)."""
    y = 0
    width = screen.width

    # Score on left
    score_text = f" SCORE: {score} "
    screen.print_at(score_text, 0, y, colour=config.COLOR_SCORE, attr=Screen.A_BOLD)

    # Wave in center
    wave_text = f" WAVE {wave}/{config.TOTAL_WAVES} "
    cx = (width - len(wave_text)) // 2
    screen.print_at(wave_text, cx, y, colour=config.COLOR_HUD, attr=Screen.A_BOLD)

    # Lives on right
    lives_text = f" LIVES: {'\u2665 ' * lives}"
    rx = width - len(lives_text)
    screen.print_at(lives_text, max(0, rx), y, colour=196, attr=Screen.A_BOLD)

    # Separator line
    screen.print_at("-" * width, 0, 1, colour=240)


def render_bottom_bar(screen, weapon_name, combo, combo_timer, shield_active=False):
    """Bottom bar: weapon (left), shield indicator, combo (right)."""
    y = screen.height - 1
    width = screen.width

    # Weapon info on left
    weapon_text = f" {weapon_name} "
    screen.print_at(weapon_text, 0, y, colour=config.COLOR_POWERUP, attr=Screen.A_BOLD)

    # Shield indicator in center-left
    if shield_active:
        shield_text = " [SHIELD ACTIVE] "
        sx = len(weapon_text) + 1
        screen.print_at(shield_text, sx, y, colour=config.COLOR_POWERUP_SHIELD, attr=Screen.A_BOLD)

    # Combo on right (only show if active)
    if combo > 1:
        combo_text = f" COMBO x{combo}! "
        rx = width - len(combo_text)
        # Flash color based on combo level
        color = config.COLOR_COMBO if combo_timer % 4 < 2 else config.COLOR_SCORE
        screen.print_at(combo_text, max(0, rx), y, colour=color, attr=Screen.A_BOLD)

    # Separator line
    screen.print_at("-" * width, 0, y - 1, colour=240)


def render_wave_banner(screen, wave, frame_no):
    """Big wave announcement in the center of screen."""
    if wave % config.BOSS_EVERY == 0:
        text = f"=== BOSS FIGHT: WAVE {wave} ==="
        color = config.COLOR_BOSS
    else:
        text = f"--- WAVE {wave} ---"
        color = config.COLOR_HUD

    x = (screen.width - len(text)) // 2
    y = screen.height // 2

    # Blink effect
    if frame_no % 6 < 4:
        screen.print_at(text, x, y, colour=color, attr=Screen.A_BOLD)


def render_game_over(screen, score):
    """Game over screen."""
    from . import sprites as sp

    cx = screen.width // 2
    cy = screen.height // 2 - 3

    for i, line in enumerate(sp.GAME_OVER_ART):
        x = cx - len(line) // 2
        screen.print_at(line, max(0, x), cy + i, colour=config.COLOR_COMBO, attr=Screen.A_BOLD)

    score_text = f"Final Score: {score}"
    screen.print_at(score_text, cx - len(score_text) // 2, cy + len(sp.GAME_OVER_ART) + 2,
                    colour=config.COLOR_SCORE, attr=Screen.A_BOLD)

    hint = "Press SPACE to play again or Q to quit"
    screen.print_at(hint, cx - len(hint) // 2, cy + len(sp.GAME_OVER_ART) + 4,
                    colour=config.COLOR_HUD)
