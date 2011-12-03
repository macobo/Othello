# -*- coding: cp1257 -*-
"""
Othello game by Karl-Aksel Puulmann (oxymaccy@gmail.com)
Dec 2011

Feel free to use the code in any way, but make sure to drop 
me an email if you build something interesting. :)

"""

import pygame
import menu
import controller
import othelloBoard
import bot
from pygame.locals import *

class othello(object):
    """Main class, controlling pretty much everything"""
    def __init__(self, screen_size = 500):
        self.board = othelloBoard.OthelloBoard(screen_size)
        self.board.draw_button(3, 4, 0)
        self.board.draw_button(4, 3, 0)
        self.board.draw_button(3, 3, 1)
        self.board.draw_button(4, 4, 1)
        self.menu = menu.Menu()
        self.gameRunning = False
        self.newButtonActive = False
        
    def init_game(self):
        self.game = controller.OthelloGame()
        for x in xrange(8):
            for y in xrange(8):
                self.board.clear_button(x, y)
        self.board.draw_button(3, 4, 0)
        self.board.draw_button(4, 3, 0)
        self.board.draw_button(3, 3, 1)
        self.board.draw_button(4, 4, 1)
        b, w = self.game.get_score()
        self.board.draw_score(b, w, self.bot_turn)
        self.board.newGame.draw(0)
        pygame.display.flip()        
    
    def play_game(self, bot_turn):
        #initialize board
        self.bot_turn = bot_turn
        self.init_game()
        self.prevHover = self.putturn = None
        self.putback = []
        self.gameRunning = True
        abot = bot.Bot(bot_turn)
        turn = 0
        while self.gameRunning:
            ## players can't move
            if not self.game.can_move(turn):
                if not self.game.can_move(1 - turn):
                    self.gameRunning = False ## Noone can move anymore - game over
                ## else - show tooltip for a while notifying the user
                elif turn == bot_turn:
                    self.menu.show_tooltip("Arvuti passib") 
                else:
                    self.menu.show_tooltip("Mängija passib")
                turn = 1 - turn
                continue
            if turn == bot_turn:
                move = abot.get_move()
                if move is not None:
                    ## mark and draw the move
                    x, y = move
                    for a, b in self.game.list_flips(x, y, turn):
                        self.board.clear_button(a, b)
                        self.board.draw_button(a, b, turn)
                        self.game.place(a, b, turn)
                    self.board.draw_button(x, y, turn)
                    self.game.place(x, y, turn)
                    abot.check_board(self.game.board) ## Test if the bot has correct data
                else:
                    print 'Computer passes!?!'
                    assert False, "Bot passes with a move" ## can't happen : previous if clause.
                b, w = self.game.get_score()
                self.board.draw_score(b, w, self.bot_turn)
                turn = 1 - turn
                pygame.display.flip()
                continue #skip over the rest
            ## Human turn?
            click, hover = self.event_handle()
            if click is not None:
                x, y = self.board.get_square(*click)
                if 0 <= x < 8 and 0 <= y < 8:
                    #find out if the move was legal
                    converts = self.game.list_flips(x, y, turn)
                    if converts:
                        #move was legal
                        #remove previous hoverings
                        if self.prevHover is not None:
                            self.board.clear_button(*self.prevHover)
                            for a, b in self.putback:
                                self.board.clear_button(a, b)
                                self.board.draw_button(a, b, self.putturn)
                            self.putback = []
                            self.prevHover = self.putturn = None
                        #draw new buttons
                        for c, r in converts:
                            self.board.clear_button(c, r)
                            self.board.draw_button(c, r, turn)
                            self.game.place(c, r, turn)
                        self.board.draw_button(x, y, turn)
                        self.game.place(x, y, turn)
                        abot.make_move(x, y, converts, turn)
                        #switch turn
                        turn = 1 - turn
                        b, w = self.game.get_score()
                        self.board.draw_score(b, w, self.bot_turn)
                        pygame.display.flip()
                        
            elif hover is not None:
                self.hover(hover, turn)
                pygame.display.flip()

        ##Show new game menu with corrent message about who won
        s = self.game.get_score()
        if s[bot_turn] > s[1 - bot_turn]:
            message = 'Arvuti võitis!'
        elif s[bot_turn] < s[1 - bot_turn]:
            message = 'Mängija võitis!'
        else:
            message = 'Viik!'
        return self.menu.show_menu(message)
        

    def event_handle(self):
        pygame.time.wait(10) #avoid lagging when moving the mouse around alot
        click = hover = None
        for event in pygame.event.get():
            if event.type == QUIT:  
                pygame.quit()
            elif event.type == MOUSEMOTION:
                hover = pygame.mouse.get_pos()
                if self.board.newGame.hovering(hover):
                    self.board.newGame.draw(1, othelloBoard.background)
                    self.newButtonActive = True
                elif self.newButtonActive:
                    self.board.newGame.draw(0, othelloBoard.background)
                    self.newButtonActive = False
            elif event.type == MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                if self.board.newGame.hovering(click):
                    self.gameRunning = False
        return click, hover

    def hover(self, where, turn):
        if self.prevHover is not None:
            ## remove previous hovering and plus score indicators
            self.board.clear_button(*self.prevHover)
            self.prevHover = None
            b, w = self.game.get_score()
            self.board.draw_score(b, w, self.bot_turn, [0, 0])
        for a, b in self.putback:
            self.board.clear_button(a, b)
            self.board.draw_button(a, b, self.putturn)
        self.putturn = None
        self.putback = []
        x, y = self.board.get_square(*where)
        if 0 <= x < 8 and 0 <= y < 8:
            converts = self.game.list_flips(x, y, turn)
            ## draw stuff showing possible move
            if converts:
                self.board.draw_trans(x, y, turn)
                self.prevHover = (x, y)
                for a, b in converts:
                    self.board.clear_button(a, b)
                    self.board.draw_trans(a, b, turn)
                self.putback = converts
                self.putturn = 1 - turn
                ## Show +len(converts)+1 at the score table
                plus = [0, 0]
                plus[turn] += len(converts) + 1
                b, w = self.game.get_score()
                self.board.draw_score(b, w, self.bot_turn, plus)
            elif converts is not False:
                ## impossible move
                self.board.draw_red(x, y, turn)
                self.prevHover = (x, y)
                self.putback = []
        

if __name__ == "__main__":
    #import time
    game = othello()
    player = game.menu.show_menu("Vali, kes alustab:")
    try:
        while True:
            player = game.play_game(1 - player)
    finally:
        pygame.quit()
