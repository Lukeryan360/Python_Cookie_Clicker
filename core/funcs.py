import os, json, math
from datetime import datetime
from zoneinfo import ZoneInfo

import pygame

import core.config as cc

#============================================================
# functions and objects
#============================================================
# Gamestate saving

def generate_save_file():
    now = datetime.now(ZoneInfo(cc.TIMEZONE)).isoformat()
    return {
        "meta": {
            "version": cc.VERSION,
            "date_created": now,
            "last_saved": None
        },
        "cookies": 0,
        "generators": {
            "Cursor": {
                "owned": 0,
                "level": 1
            },
            "Grandma": {
                "owned": 0,
                "level": 1
            },
            "Farm": {
                "owned": 0,
                "level": 1
            },
            "Mine": {
                "owned": 0,
                "level": 1
            },
            "Factory": {
                "owned": 0,
                "level": 1
            },
            "Bank": {
                "owned": 0,
                "level": 1
            },
            "Temple": {
                "owned": 0,
                "level": 1
            },
        },
        "upgrades" : {
            "click": {
                "level": 1,
            },
        },
        "stats": {
            "total_cookies_earned": 0,
            "total_clicks": 0
        }
    }

def save(game_state):
    game_state["meta"]["last_saved"] = datetime.now(ZoneInfo(cc.TIMEZONE)).isoformat()

    with open(cc.SAVE_FILE, "w") as f:
        json.dump(game_state, f, indent=4)

def _merge_with_default(loaded, default): # future-proofing
    for key, value in default.items():
        if key not in loaded:
            loaded[key] = value
        elif isinstance(value, dict):
            loaded[key] = _merge_with_default(loaded[key], value)
    return loaded

def load():
    if not os.path.exists(cc.SAVE_FILE):
        return generate_save_file()

    with open(cc.SAVE_FILE, "r") as f:
        loaded = json.load(f)

    return _merge_with_default(loaded, generate_save_file())

#============================================================
# Assets

#-- Text boxes
def draw_text(text, font_size=48, font_color="white", center=(0, 0)):
    from run import SCREEN
    font = pygame.font.SysFont(None, font_size)

    cx, cy = center

    text_surface = font.render(text, True, cc.COLOR[font_color])
    x = cx - text_surface.get_width() // 2
    y = cy - text_surface.get_height() // 2

    SCREEN.blit(text_surface, (x, y))

#============================================================

# Helper functions

def calculate_cps():
    from run import generators
    global CPS
    cps = 0.0
    for generator in generators:
        cps += generator.total_cps()
    return cps

def custom_format(n: float, decimals=1) -> str:
    abs_n = abs(n)
    if abs_n < 1_000_000:
        return f"{n:,.0f}"
    elif abs_n < 1_000_000_000:
        return f"{n / 1_000_000:.{decimals}f} Million"
    elif abs_n < 1_000_000_000_000:
        return f"{n / 1_000_000_000:.{decimals}f} Billion"
    elif abs_n < 1_000_000_000_000_000:
        return f"{n / 1_000_000_000_000:.{decimals}f} Trillion"
    elif abs_n < 1_000_000_000_000_000_000:
        return f"{n / 1_000_000_000_000_000:.{decimals}f} Quadrillion"
    else:
        return f"{n:2e}"

def custom_format_2(n: float, decimals=1) -> str:
    """
        Formats a large number with K (thousands), M (millions), or B (billions) abbreviations.
        """
    n = float(n)
    if abs(n) >= 1e12:
        return f"{n / 1e12:.{decimals}f}T"
    elif abs(n) >= 1e9:
        return f"{n / 1e9:.{decimals}f}B"
    elif abs(n) >= 1e6:
        return f"{n / 1e6:.{decimals}f}M"
    elif abs(n) >= 1e3:
        return f"{n / 1e3:.{decimals}f}K"
    else:
        return f"{n:.{decimals}f}"

#------------------------------------------------------------

# Dev tools

def cheat_cookies():
    from run import game_state
    if game_state["stats"]["total_cookies_earned"] <= 100:
        return 100
    else:
        cheated_cookies = 10 ** round(math.log10(game_state["stats"]["total_cookies_earned"]) - 1)
        print("Cheated Cookies:", cheated_cookies)
        return cheated_cookies


#============================================================