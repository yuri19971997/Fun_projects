"""ASCII art sprite definitions -- single source of truth for all visuals.

Rich sprites use Unicode block characters (█▀▄▐▌) with per-character
foreground colors for a pixel-art look.  Format: list of (chars, colors)
tuples per row.  A color of 0 means transparent (skip).
"""

# ── Block character aliases ──────────────────────────────────────────
_F = "\u2588"  # █ full block
_U = "\u2580"  # ▀ upper half
_L = "\u2584"  # ▄ lower half
_R = "\u2590"  # ▐ right half
_K = "\u258c"  # ▌ left half

# ── Color palette shortcuts ──────────────────────────────────────────
_  = 0      # transparent
CY = 51     # cyan
WH = 255    # white
GR = 46     # bright green
GD = 34     # dark green
YL = 226    # yellow
RD = 196    # red
OG = 208    # orange
BG = 82     # brighter green
SH = 87     # shield cyan
OR = 209    # orange-red (chicken)
DG = 240    # dark gray (armor)
LG = 250    # light gray (armor)
MG = 201    # magenta (kamikaze)
BM = 213    # bright magenta

# ── Player ship (5 wide x 3 tall) ───────────────────────────────────
# Rich format: list of (char_string, color_list) per row
PLAYER_SHIP_RICH = [
    (f"  {_U}  ", [_, _, CY, _, _]),
    (f" {_R}{_F}{_K} ", [_, GD, GR, GD, _]),
    (f"{_U}{_F}{_F}{_F}{_U}", [YL, GD, BG, GD, YL]),
]

PLAYER_HIT_RICH = [
    (f"  {_U}  ", [_, _, WH, _, _]),
    (f" {_R}{_F}{_K} ", [_, OG, RD, OG, _]),
    (f"{_U}{_F}{_F}{_F}{_U}", [YL, OG, RD, OG, YL]),
]

PLAYER_SHIELD_RICH = [
    (f"  {_U}  ", [_, _, WH, _, _]),
    (f" {_R}{_F}{_K} ", [_, SH, CY, SH, _]),
    (f"{_U}{_F}{_F}{_F}{_U}", [WH, SH, CY, SH, WH]),
]

# Plain-text fallbacks (kept for title screen decorations / tests)
PLAYER_SHIP = [
    "  ^  ",
    " /#\\ ",
    "<===>",
]
PLAYER_WIDTH = 5
PLAYER_HEIGHT = 3

PLAYER_HIT = [
    "  *  ",
    " *X* ",
    "*===*",
]

PLAYER_SHIELD = [
    " (^) ",
    "(/#\\)",
    "(===)",
]

# Regular chicken (5 wide x 2 tall) -- wings spread, beak up
CHICKEN = [
    "\\(^)/",
    " /~\\ ",
]
CHICKEN_WIDTH = 5
CHICKEN_HEIGHT = 2

# Armored chicken (5 wide x 2 tall) -- takes 2 hits, heavy plating
ARMORED_CHICKEN = [
    "={O}=",
    " [#] ",
]

# Bomber chicken (5 wide x 2 tall) -- shoots more often, aggressive
BOMBER_CHICKEN = [
    ">(o)<",
    " /*\\ ",
]

# Kamikaze chicken (5 wide x 2 tall) -- dives at player, wings down
KAMIKAZE_CHICKEN = [
    "v(x)v",
    "  V  ",
]

# ── Rich chicken sprites (block-char pixel art) ─────────────────────
# Regular: round bird with red comb, orange body, yellow feet
CHICKEN_RICH = [
    (f" {_L}{_F}{_L} ", [_, OR, RD, OR, _]),
    (f" {_U} {_U} ",    [_, YL, _, YL, _]),
]

# Armored: metallic plating, full-width, heavy
ARMORED_CHICKEN_RICH = [
    (f"{_R}{_F}{_F}{_F}{_K}", [DG, LG, WH, LG, DG]),
    (f" {_U}{_F}{_U} ",       [_, LG, DG, LG, _]),
]

# Bomber: angry red body, orange pointed wings
BOMBER_CHICKEN_RICH = [
    (f"{_L}{_R}{_F}{_K}{_L}", [OG, RD, RD, RD, OG]),
    (f" {_U}{_L}{_U} ",       [_, OG, RD, OG, _]),
]

# Kamikaze: diving V-shape, magenta/hot-pink
KAMIKAZE_CHICKEN_RICH = [
    (f"{_U}{_L}{_F}{_L}{_U}", [MG, MG, BM, MG, MG]),
    (f"  {_U}  ",              [_, _, MG, _, _]),
]

# Egg projectile (going down)
EGG = "o"
EGG_WIDTH = 1
EGG_HEIGHT = 1

# Player bullet (going up)
BULLET = "|"
BULLET_WIDTH = 1
BULLET_HEIGHT = 1

# Spread bullet
SPREAD_BULLET_L = "/"
SPREAD_BULLET_R = "\\"

# Power-up icons -- wide labels with clear meaning
POWERUP_WEAPON = "<GUN UP>"
POWERUP_LIFE = "\u2665 LIFE \u2665"
POWERUP_SHIELD = "<SHIELD>"
POWERUP_MISSILE = "< BOOM >"

# Explosion frames (5 wide x 3 tall) -- animate through these
EXPLOSION_FRAMES = [
    [
        " \\|/ ",
        "--*--",
        " /|\\ ",
    ],
    [
        " *+* ",
        "+ . +",
        " *+* ",
    ],
    [
        "  .  ",
        " . . ",
        "  .  ",
    ],
]

# Boss: Rooster General (wave 5) -- 11 wide x 5 tall
BOSS_ROOSTER = [
    "   \\\\|//   ",
    "   (o o)   ",
    "  /|> <|\\  ",
    " / |===| \\ ",
    "/__|___|__\\",
]
BOSS_ROOSTER_WIDTH = 11
BOSS_ROOSTER_HEIGHT = 5

# Boss: Egg Mother (wave 10) -- 11 wide x 5 tall
BOSS_EGG_MOTHER = [
    "  ___XXX___",
    " /  o  o  \\",
    "|  (====)  |",
    " \\ ooooo / ",
    "  \\_____/  ",
]

# Boss: Colonel Cluck (wave 15) -- 11 wide x 5 tall
BOSS_COLONEL = [
    "  [=====]  ",
    "  \\(o o)/  ",
    "   |>w<|   ",
    "  /|===|\\  ",
    " /_|___|_\\ ",
]

# Boss: Supreme Hen (wave 20) -- 13 wide x 6 tall
BOSS_SUPREME = [
    "  ****|****  ",
    " * \\(o_o)/ * ",
    " *  |===|  * ",
    " * /|   |\\ * ",
    " */_|___|_\\* ",
    "  *********  ",
]
BOSS_SUPREME_WIDTH = 13
BOSS_SUPREME_HEIGHT = 6

# Title screen art
TITLE_ART = [
    " ___ _   ___   _____ ___  ___ ___    ___ ___  ___    ___ _  _ ___ _  _____ ",
    "|_ _| \\ | \\ \\ / / _ \\   \\| __| _ \\  | __/ _ \\| _ \\  / __| || |_ _| |/ / __|",
    " | ||  \\| |\\ V /|   / |) | _||   /  | _| (_) |   / | (__| __ || || ' <\\__ \\",
    "|___|_|\\__| |_| |_|_\\___/|___|_|_\\  |_| \\___/|_|_\\  \\___|_||_|___|_|\\_\\___/",
]

SUBTITLE = "Defend Earth from the Poultry Menace!"

MENU_OPTIONS = [
    ">> START GAME <<",
    "   HIGH SCORES   ",
    "     QUIT        ",
]

GAME_OVER_ART = [
    "  ____    _    __  __ _____    _____     _______ ____  ",
    " / ___|  / \\  |  \\/  | ____|  / _ \\ \\   / / ____|  _ \\ ",
    "| |  _  / _ \\ | |\\/| |  _|   | | | \\ \\ / /|  _| | |_) |",
    "| |_| |/ ___ \\| |  | | |___  | |_| |\\ V / | |___|  _ < ",
    " \\____/_/   \\_\\_|  |_|_____|  \\___/  \\_/  |_____|_| \\_\\",
]

YOU_WIN_ART = [
    "__   _____  _   _  __        _____ _   _ _ ",
    "\\ \\ / / _ \\| | | | \\ \\      / /_ _| \\ | | |",
    " \\ V / | | | | | |  \\ \\ /\\ / / | ||  \\| | |",
    "  | || |_| | |_| |   \\ V  V /  | || |\\  |_|",
    "  |_| \\___/ \\___/     \\_/\\_/  |___|_| \\_(_)",
]
