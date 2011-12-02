# -*- coding: cp1257 -*-
import pygame
from pygame.locals import *
import hoverable
import time

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

class Menu(object):
    def __init__(self):
        self.victoryFont = pygame.font.SysFont('jokerman', 50)
        #self.victoryFont = pygame.font.Font('Pics\jokerman.ttf', 50)
        self.dimmer = Dimmer()
        self.normalFont = pygame.font.SysFont('jokerman', 25)
        #self.normalFont = pygame.font.Font('Pics\jokerman.ttf', 25)
       
    def show_tooltip(self, message, durnation = 1.5):
        """Shows a tooltip on dimmed background for durnation seconds"""
        screen = pygame.display.get_surface()
        w, h = screen.get_size()
        self.dimmer.darken()
        rendered = self.victoryFont.render(message, True, red)
        w = w / 2 - rendered.get_width() / 2
        h = h / 2 - rendered.get_height() / 2
        screen.blit(rendered, (w, h))
        pygame.display.flip()
        time.sleep(durnation)
        self.dimmer.restore()
        pygame.display.flip()
        
    def show_menu(self, message):
        """Shows a menu with the message and two buttons to choose which
        player starts next
        
        """
        #print message
        screen = pygame.display.get_surface()
        w, h = screen.get_size()
        self.dimmer.darken()
        #print the text
        vmessage = self.victoryFont.render(message, True, red)
        screen.blit(vmessage, (w / 2 - vmessage.get_width() / 2, h / 4))
        compButtons = [self.normalFont.render('Arvuti alustab', True, color)
                       for color in [white, red]]
        wb = compButtons[0].get_width() / 2
        comp = hoverable.Hoverable((w / 4 - wb, 0.6 * h), 0, *compButtons)
        comp.draw(0)
        normButtons = [self.normalFont.render('Mängija alustab', True, color)
                       for color in [white, red]]
        wb = normButtons[0].get_width() / 2
        norm = hoverable.Hoverable((3 * w / 4 - wb, 0.6 * h), 0, *normButtons)
        norm.draw(0)
        pygame.display.flip()
        normActive = compActive = False
        #loop until player chooses a button
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:  
                    pygame.quit()
                elif event.type == MOUSEMOTION:
                    hover = pygame.mouse.get_pos()
                    if comp.hovering(hover):
                        comp.draw(1)
                        compActive = True
                    elif compActive:
                        comp.draw(0)
                        compActive = False
                    if norm.hovering(hover):
                        norm.draw(1)
                        normActive = True
                    elif normActive:
                        norm.draw(0)
                        normActive = False
                    pygame.display.flip()
                elif event.type == MOUSEBUTTONDOWN:
                    click = pygame.mouse.get_pos()
                    if comp.hovering(click):
                        self.dimmer.restore()
                        return 1
                    if norm.hovering(click):
                        self.dimmer.restore()
                        return 0
        
        

class Dimmer(object):
    """Dimmer class by Tobias Thelen, modified for my own needs.
    See http://www.pygame.org/pcr/screen_dimmer/index.php
    
    """
    scale_factor = 1.1 # to add blur
    darken_factor = 220
    filter = (0,0,0)
    def darken(self):
        screen = pygame.display.get_surface()
        w, h = screen.get_size()
        self.buffer = pygame.Surface((w, h))
        self.buffer.blit(screen, (0,0)) # to restore later
        darken=pygame.Surface((w, h))
        darken.fill(self.filter)
        darken.set_alpha(self.darken_factor)
        # safe old clipping rectangle...
        #old_clip = screen.get_clip()
        # ..blit over entire screen...
        x, y = int(h / self.scale_factor), int(w / self.scale_factor)
        d = pygame.transform.smoothscale(self.buffer, (x, y))
        d = pygame.transform.smoothscale(d, (w, h))
        screen.blit(d, (0,0))
        screen.blit(darken, (0,0))
        # ... and restore clipping
        #screen.set_clip(old_clip)                                                
        
    def restore(self):
        pygame.display.get_surface().blit(self.buffer,(0,0))
        pygame.display.flip()
        self.buffer = None
    
