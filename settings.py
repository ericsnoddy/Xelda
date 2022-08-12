from os import path

"""
SPACE: Weapon attack
LCTRL: Magic attack
Q: Cycle weapon
"""

# game setup
WIDTH    = 1280	
HEIGHT   = 720
FPS      = 60
TILESIZE = 64

# HUD
BAR_HEIGHT = 25
HEALTH_BAR_WIDTH = 375
ENERGY_BAR_WIDTH = 260
HUD_BORDER_WIDTH = 3
BAR_SEPARATION = 10
ITEM_BOX_SIZE = 80
HUD_FONT = path.join("graphics", "font", "joystix.ttf")
HUD_FONT_SIZE = 18

# General colors
WATER_COLOR = "#71DDEE"
HUD_BG_COLOR = "#222222"
HUD_BORDER_COLOR = "#111111"
TEXT_COLOR = "#EEEEEE"

HUD_BORDER_COLOR_ACTIVE = 'gold'
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'

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
    'flame': { 'strength': 5, 'cost': 20, 'graphic': path.join("graphics", "particles", "flame", "flame.png")},
    'heal': { 'strength': 20, 'cost': 10, 'graphic': path.join("graphics", "particles", "heal", "heal.png")}
}
enemy_dict = {
	'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound': path.join("audio", "attack", "slash.wav"), 'speed': 3, 'recoil': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound': path.join("audio", "attack", "claw.wav"),'speed': 2, 'recoil': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound': path.join("audio", "attack", "fireball.wav"), 'speed': 4, 'recoil': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound': path.join("audio", "attack", "slash.wav"), 'speed': 3, 'recoil': 3, 'attack_radius': 50, 'notice_radius': 300}
}
