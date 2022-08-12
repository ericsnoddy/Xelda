import pygame
from settings import *

class UI:
    def __init__(self):
        # General. See settings.py for constants
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(HUD_FONT, HUD_FONT_SIZE)

        # bar setup
        self.healthbar_rect = pygame.Rect( 20,10, HEALTH_BAR_WIDTH, BAR_HEIGHT )
        self.energybar_rect = pygame.Rect( 20, 10 + BAR_HEIGHT + BAR_SEPARATION, ENERGY_BAR_WIDTH, BAR_HEIGHT )

    def show_bar(self, current_amt, max_amt, bg_rect, color):
        # Stat to pixel ratio conversion - Rect() will auto convert float to int
        current_rect = bg_rect.copy()
        current_rect.width = bg_rect.width * (current_amt / max_amt)

        ## draw background bar - comment out for transparent bg
        # pygame.draw.rect(self.display_surface, HUD_BG_COLOR, bg_rect)

        # Draw foreground bar
        pygame.draw.rect(self.display_surface, color, current_rect)

        # Draw border
        # Adding a 4th argument for border width auto removes rect fill (transparency)
        pygame.draw.rect(self.display_surface, HUD_BORDER_COLOR, bg_rect, HUD_BORDER_WIDTH)

    def show_exp(self, exp):
        # int() ensures no floats are input. Anti-alias off.
        txt_surf = self.font.render( f"EXP: {int(exp):,}", False, TEXT_COLOR)

        # Not sure why we don't use game constants WIDTH and HEIGHT instead of get_size()
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        txt_rect = txt_surf.get_rect( bottomright=(x,y) )

        # inflate to add padding; blit the text; add a border
        pygame.draw.rect(self.display_surface, HUD_BG_COLOR, txt_rect.inflate(10,5))
        self.display_surface.blit(txt_surf, txt_rect)
        pygame.draw.rect(self.display_surface, HUD_BORDER_COLOR, txt_rect.inflate(10,5), HUD_BORDER_WIDTH)

    def select_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, HUD_BG_COLOR, bg_rect)
        
        if has_switched:
            pygame.draw.rect(self.display_surface, HUD_BORDER_COLOR_ACTIVE, bg_rect, HUD_BORDER_WIDTH)
        else:
            pygame.draw.rect(self.display_surface, HUD_BORDER_COLOR, bg_rect, HUD_BORDER_WIDTH)

        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        # Placement of selection boxes; trial and error
        wleft = 10 + ITEM_BOX_SIZE
        wtop = self.display_surface.get_size()[1] - 100
        bg_rect = self.select_box(wleft, wtop, has_switched) # Weapon

        # Path is conveniently included in weapon_dict under 'graphic'
        key = list(weapon_dict.keys())[weapon_index]
        fullpng_path = weapon_dict[key]['graphic']

        weapon_surf = pygame.image.load(fullpng_path).convert_alpha()
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        # Placement of selection boxes; trial and error
        mleft = 20
        mtop = self.display_surface.get_size()[1] - (ITEM_BOX_SIZE * 2)
        bg_rect = self.select_box(mleft, mtop, has_switched) # Magic selection

        key = list(magic_dict.keys())[magic_index]
        fullpng_path = magic_dict[key]['graphic']

        magic_surf = pygame.image.load(fullpng_path).convert_alpha()
        magic_rect = magic_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)

    def display_hud(self, player):
        self.show_bar(player.health, player.stats['maxhealth'], self.healthbar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['maxenergy'], self.energybar_rect, ENERGY_COLOR)
        self.show_exp(player.exp)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)

