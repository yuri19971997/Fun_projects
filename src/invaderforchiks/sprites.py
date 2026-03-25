"""ASCII art sprite definitions -- single source of truth for all visuals."""

# Player ship (5 wide x 3 tall)
PLAYER_SHIP = [
    "  ^  ",
    " /A\\ ",
    "/___\\",
]
PLAYER_WIDTH = 5
PLAYER_HEIGHT = 3

# Player ship hit (flashing)
PLAYER_HIT = [
    "  *  ",
    " *X* ",
    "*****",
]

# Regular chicken (5 wide x 2 tall)
CHICKEN = [
    " \\o/ ",
    " /_\\ ",
]
CHICKEN_WIDTH = 5
CHICKEN_HEIGHT = 2

# Armored chicken (5 wide x 2 tall) -- takes 2 hits
ARMORED_CHICKEN = [
    " {o} ",
    " [#] ",
]

# Bomber chicken (5 wide x 2 tall) -- shoots more often
BOMBER_CHICKEN = [
    " >o< ",
    " /V\\ ",
]

# Kamikaze chicken (5 wide x 2 tall) -- dives at player
KAMIKAZE_CHICKEN = [
    " \\o/ ",
    "  V  ",
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
POWERUP_LIFE = "< +1 HP>"
POWERUP_SHIELD = "<SHIELD>"
POWERUP_MISSILE = "< BOOM >"

# Explosion frames (5 wide x 3 tall) -- animate through these
EXPLOSION_FRAMES = [
    [
        " .#. ",
        " ### ",
        " '#' ",
    ],
    [
        " *+* ",
        " +X+ ",
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
