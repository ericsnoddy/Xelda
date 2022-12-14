from pygame.locals import *
from os import path

# Edit player controls
# For a list of pygame key constants see http://www.pygame.org/docs/ref/key.html#pygame.key.get_pressed
up_key = K_UP
down_key = K_DOWN
left_key = K_LEFT
right_key = K_RIGHT
weapon_attack_key = K_SPACE
magic_cast_key = K_LCTRL
cycle_weapon_key = K_e
cycle_magic_key = K_q
pause_and_upgrade_key = K_TAB

# Soundtrack
BG_MUSIC = path.join("audio", "main.ogg")

# game setup
WIDTH    = 1280	
HEIGHT   = 720
FPS      = 60
TILESIZE = 64

# volume
BG_MUSIC_VOL = 0.2
SFX_VOL = 0.4
SWORD_VOL = 0.2

# HUD
BAR_HEIGHT = 25
HEALTH_BAR_WIDTH = 375
ENERGY_BAR_WIDTH = 260
HUD_BORDER_WIDTH = 3
BAR_SEPARATION = 10
ITEM_BOX_SIZE = 80
HUD_FONT = path.join("graphics", "font", "joystix.ttf")
HUD_FONT_SIZE = 18

# Hitbox offset. These tweaks make it easier to navigate the world
HITBOX_Y_OFFSET = {
    'player': -26,
    'object': -55,
    'flora': -12,
    'invisible': 0
}

# General colors
OCEAN_COLOR = "#71DDEE"
HUD_BG_COLOR = "#222222"
HUD_BORDER_COLOR = "#111111"
TEXT_COLOR = "#EEEEEE"

HUD_BORDER_COLOR_ACTIVE = 'gold'
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'

# Upgrade menu
TEXT_COLOR_SELECTED = "#111111"
BAR_COLOR = "#EEEEEE"
BAR_COLOR_SELECTED = "#111111"
UPGRADE_BG_COLOR_SELECTED = "#EEEEEE"

# GAME OVER provided by PNGTree
GAME_OVER = path.join("graphics", "font", "game_over.png")

# Other data is here when importing is more convenient than passing through Classes and functions
# Acts like global data once imported
weapon_dict = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': path.join("graphics", "weapons", "sword", "full.png")},
    'lance': {'cooldown': 400, 'damage': 30, 'graphic': path.join("graphics", "weapons", "lance", "full.png")},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic': path.join("graphics", "weapons", "axe", "full.png")},
    'rapier': {'cooldown': 50, 'damage': 8, 'graphic': path.join("graphics", "weapons", "rapier", "full.png")},
    'sai': {'cooldown': 80, 'damage': 10, 'graphic': path.join("graphics", "weapons", "sai", "full.png")}
}
magic_dict = {
    'flame': { 'strength': 7, 'cost': 20, 'graphic': path.join("graphics", "particles", "flame", "flame.png")},
    'heal': { 'strength': 20, 'cost': 10, 'graphic': path.join("graphics", "particles", "heal", "heal.png")}
}
enemy_dict = {
	'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound': path.join("audio", "attack", "slash.wav"), 'speed': 3, 'recoil': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound': path.join("audio", "attack", "claw.wav"),'speed': 2, 'recoil': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound': path.join("audio", "attack", "fireball.wav"), 'speed': 4, 'recoil': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound': path.join("audio", "attack", "slash.wav"), 'speed': 3, 'recoil': 3, 'attack_radius': 50, 'notice_radius': 300}
}

