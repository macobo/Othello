import pygame
import sys
from pygame.locals import *

class Hoverable(object):
    """Useful utility class by Karl-Aksel Puulmann (Dec 2011)
        A pygame "object" which is centered around a position and has several states to be
        blitted.
        
        Usage: hoverable/resizable buttons in games
    """
    def __init__(self, pos, anchor = HAT_CENTERED, *states):
        """Inits the Hoverable. Takes 3 arguments:
            pos - where it should blit the state 0
            anchor - how should it position if redrawing
                    resizes
            states - the things needed to alternate between (blittable objects)
            """
        self.x, self.y = pos
        self.drawn = None
        self.states = states
        #0 - left, 0.5 middle, 1 - right
        if anchor in (HAT_LEFT, HAT_LEFTDOWN, HAT_LEFTUP):
            self.xmult = 0
        elif anchor in (HAT_CENTERED, HAT_DOWN, HAT_UP):
            self.xmult = 0.5
        elif anchor in (HAT_RIGHT, HAT_RIGHTDOWN, HAT_RIGHTUP):
            self.xmult = 1
        #0 - up, 0.5 middle, 1 - down
        if anchor in (HAT_UP, HAT_LEFTUP, HAT_RIGHTUP):
            self.ymult = 0
        elif anchor in (HAT_CENTERED, HAT_LEFT, HAT_RIGHT):
            self.ymult = 0.5
        elif anchor in (HAT_DOWN, HAT_LEFTDOWN, HAT_RIGHTDOWN):
            self.ymult = 1

        hasBack = states[0].get_size()
        for s in states:
            if s.get_size() != hasBack:
                hasBack = False
        if hasBack:
            #print hasBack, pos
            self.back = pygame.Surface(hasBack)
            r = pygame.Rect(pos[0], pos[1], hasBack[0], hasBack[1])
            self.back.blit(pygame.display.get_surface(), (0, 0), r)
        else:
            self.back = None
        
    def _measure(self, i):
        j = self.states[0].get_rect()
        k = self.states[i].get_rect()
        width = k.w
        height = k.h
        dw = int((j.w - k.w) * self.xmult)
        dh = int((j.h - k.h) * self.ymult)
        return dw, dh, width, height
            
    def corners(self, i = None):
        """Returns the current four corners of the Hoverable:
    (topwidth, topheight, bottomwidth, bottomheight"""
        if i == None:
            i = self.drawn
        dw, dh, width, height = self._measure(i)
        return (self.x + dw,
                self.y + dh,
                self.x + width + dw,
                self.y + height + dh)

    def draw(self, i, back = None):
        """Draws state i.
            Todo: exception when i > len(states)
            """
        self.drawn = i
        x, y, a, b = self.corners(i)
        if self.back is not None:
            pygame.display.get_surface().blit(self.back, (x, y))
        pygame.display.get_surface().blit(self.states[i], (x,y))

    def hovering(self, pos):
        """returns True if hovering over the currently drawn Hoverable"""
        x, y = pos
        x1,y1,x2,y2 = self.corners(self.drawn)
        return x1 < x < x2 and y1 < y < y2
    
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((660, 330))
    font = pygame.font.Font('Pics\jokerman.ttf', 30)
    font2 = pygame.font.Font('Pics\jokerman.ttf', 30)
    orig = font.render('Original', True, (255,255,255))
    active =  font2.render('Active', True, (255, 0, 0))
    d = [HAT_CENTERED, HAT_DOWN, HAT_UP, \
         HAT_LEFT, HAT_LEFTDOWN, HAT_LEFTUP, \
         HAT_RIGHT, HAT_RIGHTDOWN, HAT_RIGHTUP]
    hoverable = [Hoverable((30+(i%3)*200, 30+(i/3)*100), d[i], orig, active)
                               for i in xrange (len(d))]
    for i in hoverable:
        i.draw(0)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE or event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == MOUSEMOTION:
                screen.fill((0,0,0))
                pos = pygame.mouse.get_pos()
                for hov in hoverable:
                    if hov.hovering(pos):
                        hov.draw(1)
                    else:
                        hov.draw(0)
                pygame.display.flip()
