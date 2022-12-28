import random
from BaseAI import BaseAI

H_SNAKE1 = [[2**1,2**2,2**3,2**4],
           [2**8,2**7,2**6,2**5],
           [2**9,2**10,2**11,2**12],
           [2**16,2**15,2**14,2**13]]

class IntelligentAgent(BaseAI):
    def getMove(self, grid):
        child = self.decision((None, grid))
        if child == None:
            return child
        else:
            return child[0]


    def snake_algo(self, board):
        h = 0
        for i in range(board.size):
            for j in range(board.size):
                h += board.map[i][j] * (H_SNAKE1[i][j])


        return h
    def tile_probability(self, board):
        h = 0

        future_board = board.clone()
        empty_tiles = future_board.getAvailableCells()
        for x, y in empty_tiles:
            #board.addTile()
            future_board.map[x][y] = 2
            h +=  self.snake_algo(future_board) / len(empty_tiles)
        return h
    # def dfs(self, state,):
    def chance(self, state, alpha, beta, depth):
        possibilities = []
        empty_tiles = state.getAvailableCells()
        for tile in empty_tiles:
            future_board = state.clone()
            future_board.insertTile(tile, 2)

            _, utility = self.maximize((None, future_board), alpha, beta, depth+1)
            possibilities.append(utility)
        average = float(sum(possibilities)) / float(len(possibilities))
        return average

    def minimize(self, state, alpha, beta, depth):
        #MIN updates alpha - current lower bound on max's outcome
        if not state[1].canMove():
            return None, eval("vecIndex"),

        # heuristic_score = self.heuristic_algo(state)

        minChild, minUtility = None, float('inf')

        util_min = self.chance(state[1], alpha, beta, depth+1)

        moveset = state[1].getAvailableMoves()
        for child in moveset:

            if util_min < minUtility:
                minChild, minUtility = child, util_min
            if minUtility <= alpha:
                break
            if minUtility < beta:
                beta = minUtility
        return minChild, minUtility

    def maximize(self, state, alpha, beta, depth=0):
        #MAX updates beta- current upper bound on min's outcome
        # h_scores = []
        # if not state[1].canMove():
        #     return None, eval("vecIndex")


        maxChild, maxUtility = None, float('-inf')


        moveset = state[1].getAvailableMoves()
        for child in moveset:
            if not depth >= 2:
                _, util_max = self.minimize(child, alpha, beta, depth + 1)

            else:
                util_max = self.snake_algo(child[1])

            if util_max > maxUtility:
                maxChild, maxUtility = child, util_max
            if maxUtility >= beta:
                break
            if maxUtility > alpha:
                alpha = maxUtility
        return maxChild, maxUtility

    def decision(self, state):
        child, _ = self.maximize(state, float('-inf'), float('inf'))
        return child