import pygame
from settings import *
from debug import debug

# This is a complicated couple of classes to create cards over the screen
# Suggest thorough study to understand everything going on.
class Upgrade:
    def __init__(self, player):
            # get a reference to the current display surface
        self.display_surface = pygame.display.get_surface()

            # general setup
        self.player = player
        self.total_attributes = len(player.stats)
                
            # preload stats data from player.py; listify to make subscriptable
        self.attribute_names = list(player.upgrade_cost.keys())  # 'upgrade_cost' has the labels I desire
        self.max_values = list(player.max_stats.values()) 
        self.upgrade_costs = list(player.upgrade_cost.values())
            # Each stat can be upgraded 4 times
        self.upgrade_increment_dict = { 'health': 50, 'energy': 10, 'attack': 4, 'magic': 3, 'speed': 2 }
        self.upgrade_increments = list(self.upgrade_increment_dict.values())

        self.font = pygame.font.Font(HUD_FONT, HUD_FONT_SIZE)

            # screen item dimensions
        self.surface_size = self.display_surface.get_size()
        self.card_width = self.surface_size[0] // 6
        self.card_height = self.surface_size[1] * 0.8
        self.create_items()

            # selection system
        self.selection_index = 0
        self.selection_time = None
        self.selection_cooldown_time = 300  # ms
        self.can_highlight = True

    def input(self):
        keys = pygame.key.get_pressed()

            # We have to wrap in a cooldown timer to avoid key-spamming @ 60x/sec
        if self.can_highlight:
                                # only if we're not all the way to the right
                                # avoid index out of range error
            if keys[right_key] and self.selection_index < self.total_attributes - 1:
                self.selection_index += 1
                self.can_highlight = False      # Avoid 60x/sec key spamming
                self.selection_time = pygame.time.get_ticks()   # start timer                
                                # only if we can still move left
            elif keys[left_key] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_highlight = False 
                self.selection_time = pygame.time.get_ticks()

            if keys[weapon_attack_key]:
                self.can_highlight = False
                self.selection_time = pygame.time.get_ticks()
                self.try_upgrade(self.player)  # No need to pass selection_index
                
    def selection_cooldown(self):
        if not self.can_highlight:
            current_time = pygame.time.get_ticks()  # stop timer
            if current_time - self.selection_time >= self.selection_cooldown_time:
                self.can_highlight = True

    def create_items(self):
        self.item_list = []

        for index, item in enumerate(range(self.total_attributes)):
            # horizontal position

            full_width = self.surface_size[0]
            increment = full_width // self.total_attributes
            left = (index * increment) + (increment - self.card_width) // 2

            # vertical position
            top = self.surface_size[1] * 0.1

            # create the object
            item = Item(left, top, self.card_width, self.card_height, index, self.font)
            self.item_list.append(item)

    ## BROKEN ##
    ## I need to edit player stats but there's like a mix of player.stat and player.stats{dict}
    ## Do I increment self.speed AND self.stats['speed']?
    def try_upgrade(self, player):
        # upgrade data from __init__
        i = self.selection_index
        attribute = self.attribute_names[i]
        upgrade_cost = self.upgrade_costs[i]
        max_value = self.max_values[i]
        increment = self.upgrade_increments[i]

        if upgrade_cost <= player.exp and player.stats[attribute] + increment <= max_value:
            player.exp -= upgrade_cost
            # match attribute:
            #     case:

                # Full heal takes care of vanishing health bar
            if attribute == 'health':
                player.health = player.stats['health']

    def display(self, player):
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):
                # get attributes from player (passed into __init__)
                # First I listify the dict, sort by keys() or values() to make subscriptable
            attribute = self.attribute_names[index]  # We have this already from __init__
            value = list(player.stats.values())[index]
            max_value = self.max_values[index]
            cost = self.upgrade_costs[index]
            item.display(self.display_surface, self.selection_index, attribute, value, max_value, cost)

class Item:
    def __init__(self, left, top, width, height, index, font):
        self.rect = pygame.Rect(left, top, width, height)
            # Copy and transform rect to smaller version for bar
        self.bar_rect = self.rect.copy()        
        self.bar_rect.width *= 0.3
        self.bar_rect.height *= 0.8
        self.bar_rect.center = self.rect.center
        
        self.index = index
        self.font = font

    def display_labels(self, display_surface, attribute, cost, is_selected):
        color = TEXT_COLOR_SELECTED if is_selected else TEXT_COLOR

        # title
        title_surf = self.font.render(attribute, False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))        

        # cost [we int() just in case of weird float like 100.00000000001]
        cost_surf = self.font.render(f"cost: {int(cost)}", False, color)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0,20))

        # draw
        display_surface.blit(title_surf, title_rect)
        display_surface.blit(cost_surf, cost_rect)

    def display_bar(self, display_surface, attribute, value, max_value, is_selected):
        # drawing setup / style choices
        bg_color = BAR_COLOR_SELECTED if is_selected else BAR_COLOR
        bar_color = HEALTH_COLOR if attribute in ['health', 'attack', 'speed'] else ENERGY_COLOR

        pygame.draw.rect(display_surface, bg_color, self.bar_rect)
        pygame.draw.rect(display_surface, HUD_BORDER_COLOR, self.bar_rect, 4)

        # ratio current level to max levels
        ratio = 1 - value / max_value
        top_offset = self.bar_rect.height * ratio  # This amount I add as Vector2(0,y)

        top = self.bar_rect.midtop + pygame.math.Vector2(0,top_offset)
        bottom = self.bar_rect.midbottom
        width = self.bar_rect.width - 8
        pygame.draw.line(display_surface, bar_color, top, bottom, width)

        # pygame.draw.rect(display_surface, bar_color, self.gauge_rect)

    def display(self, display_surface, selection_num, attribute, value, max_value, cost):
        if self.index == selection_num:
            pygame.draw.rect(display_surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(display_surface, HUD_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(display_surface, HUD_BG_COLOR, self.rect)
            pygame.draw.rect(display_surface, HUD_BORDER_COLOR, self.rect, 4)
                                                                # creates a boolean
        self.display_labels(display_surface, attribute, cost, self.index == selection_num)
        self.display_bar(display_surface, attribute, value, max_value, self.index == selection_num)