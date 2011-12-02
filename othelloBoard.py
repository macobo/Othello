# -*- coding: cp1257 -*-
import pygame
import menu
import hoverable

## Font colors
background = (85, 198, 57)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

class OthelloBoard(object):
    """Class for the graphical output to the board and for drawing the board"""
    def __init__(self, size):
        self.windowsize = size
        self.buttonsize = int(size * 0.9 / 8)
        self.start_x = int(self.windowsize * 0.05)
        self.linewidth = self.windowsize / 160
        pygame.init()
        self.screen = pygame.display.set_mode((self.windowsize,
                                               int(self.windowsize * 1.05)))
        pygame.display.set_caption('::Othello::')
        self.screen.fill(background)
        self._load_icons()
        #self.screen.blit(self.back, (0, 0))
        
        self.draw_board()
        #self.newGame.draw(0)
        #pygame.display.flip()

    def draw_board(self):
        for i in xrange(0, 9):
            self.draw_lines(i)
        ## self.draw_score(2, 2)

    def draw_score(self, b, w, blackIsPlayer, extra = [0, 0]):
        """Draws a score indicator below the game board.
        b - score of the player using black
        w - score of the player using white
        blackIsPlayer - 0 means that black is human and white AI and 1 vise-versa
        extra - +score used for hovering buttons showing possible moves. 
            Will be displayed red next to the real score
        
        """
        
        ssize = self.font.render('Mängija: 33+33', True, white).get_width()
        if blackIsPlayer:
            must = self.font.render('Mängija: %d' % b, True, black)
            valge = self.font.render('Arvuti: %d' % w, True, white)
        else:
            must = self.font.render('Arvuti: %d' % b, True, black)
            valge = self.font.render('Mängija: %d' % w, True, white)    
        vs = self.font.render('Mängija: 1', True, white).get_width()
        startx = self.buttonsize * 0.3 + self.start_x
        inversex = self.windowsize - startx - vs
        starty = int(self.windowsize * 0.96)        
        #erase old
        r = pygame.Rect(startx, starty,
                        ssize * 1.05, must.get_height())
        pygame.draw.rect(self.screen, background, r)
        r = pygame.Rect(inversex, starty,
                        ssize * 1.05, valge.get_height())
        pygame.draw.rect(self.screen, background, r)
        #draw new
        if extra[0]:
            mustextra = self.font.render('+%d' % extra[0], True, red)
            self.screen.blit(mustextra, (startx + must.get_width(), starty))
        self.screen.blit(must, (startx, starty))
        if extra[1]:
            valgeextra = self.font.render('+%d' % extra[1], True, red)
            self.screen.blit(valgeextra, (inversex + valge.get_width(), starty))
        self.screen.blit(valge, (inversex, starty))
        
    def draw_lines(self, i):
        start_x = self.start_x - self.linewidth / 2
        end_x = self.start_x + 8 * self.buttonsize
        pygame.draw.line(self.screen,
                         (0,0,0),
                         (start_x + i * self.buttonsize, start_x),
                         (start_x + i * self.buttonsize, end_x),
                         self.linewidth)
        pygame.draw.line(self.screen,
                         (0,0,0),
                         (start_x, start_x + i * self.buttonsize),
                         (end_x, start_x + i * self.buttonsize),
                         self.linewidth)

    def draw_button(self, x, y, color):
        """Draws a normal button of color (0 is black) at board[x][y]"""
        x, y = self.get_pos(x, y)
        self.screen.blit(self.button[color], (x + self.buttonsize * 0.05 + self.linewidth / 2,
                                              y + self.buttonsize * 0.05 + self.linewidth / 2))

    def draw_trans(self, x, y, color):
        """Draws a bit transparent button - used for hovering tips for possible moves"""
        x, y = self.get_pos(x, y)
        self.screen.blit(self.trans[color], (x + self.buttonsize * 0.05 + self.linewidth / 2,
                                              y + self.buttonsize * 0.05 + self.linewidth / 2))
    
    def draw_red(self, x, y, color):
        """Draws a red game button - used for showing impossible moves"""
        x, y = self.get_pos(x, y)
        self.screen.blit(self.red[color], (x + self.buttonsize * 0.05 + self.linewidth / 2,
                                              y + self.buttonsize * 0.05 + self.linewidth / 2))

    def clear_button(self, x, y):
        x, y = self.get_pos(x, y)
        r = pygame.Rect(x + self.linewidth/2,
                        y + self.linewidth / 2,
                        self.buttonsize - self.linewidth,
                        self.buttonsize - self.linewidth)
        pygame.draw.rect(self.screen, background, r)


    def _load_icons(self):
        self.orig_button = [pygame.image.load("Pics/black.png").convert_alpha(),
                       pygame.image.load("Pics/white.png").convert_alpha()]
        self.orig_trans = [pygame.image.load("Pics/black2.png").convert_alpha(),
                       pygame.image.load("Pics/white2.png").convert_alpha()]
        self.orig_red = [pygame.image.load("Pics/black3.png").convert_alpha(),
                       pygame.image.load("Pics/white3.png").convert_alpha()]
        
        self.button = [pygame.transform.smoothscale(x, (int(self.buttonsize * 0.9),
                                                      int(self.buttonsize * 0.9)))
                       for x in self.orig_button]
        self.trans = [pygame.transform.smoothscale(x, (int(self.buttonsize * 0.9),
                                                      int(self.buttonsize * 0.9)))
                       for x in self.orig_trans]
        self.font = pygame.font.SysFont('jokerman', 20)
        self.red =   [pygame.transform.smoothscale(x, (int(self.buttonsize * 0.9),
                                                      int(self.buttonsize * 0.9)))
                       for x in self.orig_red]
        uus1 = self.font.render('Uus mäng', True, white)
        uus2 = self.font.render('Uus mäng', True, red)
        x = self.windowsize / 2 - uus1.get_width() / 2
        y = int(self.windowsize * 0.96)
        #print 'hoverable'
        self.newGame = hoverable.Hoverable((x, y), pygame.locals.HAT_CENTERED, uus1, uus2)
        

    def get_pos(self, x, y):
        return (self.start_x + x * self.buttonsize,
                self.start_x + y * self.buttonsize)

    def get_square(self, x, y):
        """Returns square number of x and y coordinates on screen. If location is
            not on a square, returns (-1, -1)

        """
        xd, xm = divmod(x - self.start_x, self.buttonsize)
        yd, ym = divmod(y - self.start_x, self.buttonsize)
        if (xm + self.linewidth / 2) % self.buttonsize <= self.linewidth:
            return -1, -1
        if (ym + self.linewidth / 2) % self.buttonsize <= self.linewidth:
            return -1, -1
        #print (xd, xm), (yd, ym)
        return xd, yd
                       
if __name__ == "__main__":
    import time
    game = OthelloBoard(500)
    game.draw_button(3, 4, 0)
    game.draw_button(4, 3, 0)
    game.draw_button(3, 3, 1)
    game.draw_button(4, 4, 1)
    game.draw_button(0, 0, 0)
    pygame.display.flip()
    time.sleep(2)
    d = menu.Menu()
    d.show_menu('Valge võitis!')
    pygame.display.flip()
    time.sleep(1)
#    game.clear_button(4, 4)
    pygame.display.flip()
    time.sleep(5)
    pygame.quit()
