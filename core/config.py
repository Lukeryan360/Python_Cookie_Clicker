#============================================================
# game config
#============================================================

SAVE_FILE = "../save.json"
VERSION = 1.0
TIMEZONE = "America/New_York"
DEBUG = False

#------------------------------------------------------------

WINDOW_NAME = "Cookie Clicker"

#------------------------------------------------------------
# Display
RESOLUTION = 1600, 900 # best in 16:9
FPS = 60

COLOR = {
    "white"     :   (255,255,255),
    "black"     :   (0,0,0),
    "red"       :   (255,0,0),
    "green"     :   (0,255,0),
    "blue"      :   (0,0,255),

    "l_gray"    :   (200, 200, 200),
    "gray"      :   (125, 125, 125),
    "d_gray"    :   (100, 100, 100),
    "l_blue"    :   (100, 100, 150),
    "l_green"   :   (100, 150, 100),
    "bg_blue"   :   (136, 137, 201),
    "cookie"    :   (219, 176, 90),
    "chocolate" :   (66, 50, 32)
    }

SPRITES = {
    "cookie" : "sprites/cookie.png",
    "cursor" : "sprites/cursor.png"
}

# Cookie spring animation - tunable parameters

BOUNCE_AMPLITUDE = 0.12     # max scale change (default: 0.12)
BOUNCE_DECAY = 5.0          # damping factor (default: 5.0)
BOUNCE_FREQUENCY = 12.0     # oscillations per second (default: 12.0)
BOUNCE_DURATION = 1         # seconds (default: 1)

#============================================================
