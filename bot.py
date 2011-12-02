from random import choice
oo = 9876 ## infinity for alpha-beta
ALPHA_DEPTH = 4 ## max depth for alpha-beta
CORNER = 9.5
SIDE = 1.5

class Bot(object):
    """Simple bot using a shallow alpha-beta pruning search for 
        finding moves.
        
    """
    def __init__(self, color):
        self.color = color
        self.board = [[0] * 8 for _ in xrange(8)]
        self.score = [0, 0]
        ## place initial
        self.place(3, 3, 1)
        self.place(4, 4, 1)
        self.place(3, 4, 0)
        self.place(4, 3, 0)
        
        
    def check_board(self, board):
        """checks if the bot has correct information about the world"""
        for i in xrange(8):
            for j in xrange(8):
                assert self.board[i][j] == board[i][j], (i, j, self.board[i][j], board[i][j])

    def list_flips(self, c, r, color):
        """lists stones to flip when player "color" places a stone at c, r"""
        if self.board[c][r]:
            return []
        solution = []
        for dx, dy in ((a, b) for a in xrange(-1,2) for b in xrange(-1,2)):
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
    
    def place(self, a, b, color, flip = False):
        self.board[a][b] = 1 + color
        if a in (0, 7) and b in (0, 7):
            ## corners cannot be turned
            self.score[color] += CORNER
        elif a in (0, 7) or b in (0, 7):
            self.score[color] += SIDE
            if flip:
                self.score[1 - color] -= SIDE
        else:
            self.score[color] += 1
            if flip:
                self.score[1 - color] -= 1                
    
    def make_move(self, x, y, flips, player):
        for a, b in flips:
            self.place(a, b, player, True)
        self.place(x, y, player)
    
    def undo_move(self, x, y, flips, player):
        for a, b in flips:
            self.place(a, b, 1 - player, True)
        self.board[x][y] = 0
        if x in (0, 7) and y in (0, 7):
            self.score[player] -= CORNER
        elif x in (0, 7) and y in (0, 7):
            self.score[player] -= SIDE
        else:
            self.score[player] -= 1     
    
    def get_ordering(self, player):
        ## Returns ordered list of moves player can make.
        result = []
        for x in xrange(8):
            for y in xrange(8):
                moves = self.list_flips(x, y, player)
                if len(moves):
                    result.append((len(moves), (x, y)))
        ## Returns [] if no appropriate move is found.
        result.sort(reverse = True)
        return result
    
    def get_move2(self):
        ## backup move generator - returns the move that will generate most gain this turn!
        moves = self.get_ordering(self.color)
        if moves:
            ## place the move
            x, y = moves[0][1]
            for a, b in self.list_flips(x, y, self.color):
                self.place(a, b, self.color, True)
            self.place(x, y, self.color)
            return x, y #(x, y)
        ## Returns None if no moves are found.
    
    def get_move(self):
        #return self.get_move2()
        ## Gets the best move with alpha_beta
        moves = self.get_ordering(self.color)
        if moves:
            x, y = moves[0][1]
            flips = self.list_flips(x, y, self.color)
            self.make_move(x, y, flips, self.color)
            bestAlpha = self.alpha_beta(ALPHA_DEPTH, 1 - self.color, -oo, oo)
            self.undo_move(x, y, flips, self.color)
            bestMove = [(x, y)]
            for _, (x, y) in moves[1:]:
                flips = self.list_flips(x, y, self.color)
                self.make_move(x, y, flips, self.color)
                ## call next round of alpha-betaing.
                result = self.alpha_beta(ALPHA_DEPTH, 1 - self.color, bestAlpha, oo)
                if result > bestAlpha:
                    bestAlpha = result
                    bestMove = [(x, y)]
                elif result == bestAlpha:
                    bestMove.append((x, y))
                ## undo move
                self.undo_move(x, y, flips, self.color)     
            if bestMove is not None:
                bestMove = choice(bestMove) ## pick one of the "best" moves at random. :)
                flips = self.list_flips(bestMove[0], bestMove[1], self.color)
                self.make_move(bestMove[0], bestMove[1], flips, self.color)      
            return bestMove
    
    def heuristic(self):
        """Heuristic - just count the buttons on both sides, giving more value to
            the ones in the corners and sides
            """
        return self.score[self.color] - self.score[1 - self.color] 
    
    def alpha_beta(self, depth, player, alpha = oo, beta = oo):
        if depth == 0:
            return self.heuristic()

        children = self.get_ordering(player)
        ## print len(children)
        if not children:
            ## player must pass?
            if player == self.color:
                return max(alpha, self.alpha_beta(depth - 1, 1 - player, alpha, beta))
            else:
                return min(beta, self.alpha_beta(depth - 1, 1 - player, alpha, beta))

        for _, (x, y) in children:
            ## make the move first, ask the questions later!
            flips = self.list_flips(x, y, player)
            self.make_move(x, y, flips, player)
            ## call next round of alpha-betaing.
            result = self.alpha_beta(depth - 1, 1 - player, alpha, beta)
            ## undo move
            self.undo_move(x, y, flips, player)
            
            if player == self.color: ## maximizing player
                alpha = max(alpha, result)
            else: ## minimizing player
                beta = min(beta, result)
            if beta <= alpha: break ## alpha cutoff
        if player == self.color:
            return alpha
        else:
            return beta