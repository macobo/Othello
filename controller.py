class OthelloGame(object):
    """Brains class for getting what moves can be made and to list buttons needed
        to be flipped by a move.
        
    """
    def __init__(self):
        self.board = [[0] * 8 for _ in xrange(8)]
        self.place(3, 3, 1)
        self.place(4, 4, 1)
        self.place(3, 4, 0)
        self.place(4, 3, 0)

    def place(self, c, r, color):
        self.board[c][r] = 1 + color

    def get_score(self):
        score = [0,0]
        for r in self.board:
            for s in r:
                if s:
                    score[s-1] += 1
        return score

    def list_flips(self, c, r, color):
        if self.board[c][r]:
            return False
        solution = []
        for dx, dy in [(a, b) for a in xrange(-1,2) for b in xrange(-1,2)]:
            toadd = []
            x, y = c + dx, r + dy
            while 0 <= x < 8 and 0 <= y < 8:
                if self.board[x][y] == 1 + color:
                    solution.extend(toadd)
                    break
                elif self.board[x][y] == 0:
                    #empty square
                    break
                #print [x, y, color]
                toadd.append((x, y))
                x += dx
                y += dy
        #print color,solution
        return solution

    def game_over(self):
        """Returns 0 if no win, 1 if black wins and 2 if white wins"""
        count = [0, 0]
        for c in xrange(8):
            for r in xrange(8):
                if self.board[c][r] == 0:
                    if self.list_flips(c, r, 0) or self.list_flips(c, r, 1):
                        return 0 #no joy
                else:
                    count[self.board[c][r] - 1] += 1
        if count[0] == count[1]:
            return 0 #tie
        if count[0] > count[1]:
            return 1
        return 2
    
    def can_move(self, player):
        for c in xrange(8):
            for r in xrange(8):
                if self.list_flips(c, r, player):
                    return True
        return False
    
    