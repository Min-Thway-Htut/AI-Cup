import random
import numpy as np

class GomokuAgent:
    
    def __init__(self, agent_symbol, blank_symbol, opponent_symbol):
        self.name = __name__
        self.agent_symbol = agent_symbol
        self.blank_symbol = blank_symbol
        self.opponent_symbol = opponent_symbol
    
    def play(self, board):
        # Step 1: Try to win immediately
        for i in range(15):
            for j in range(15):
                if board[i, j] == self.blank_symbol:
                    board[i, j] = self.agent_symbol
                    if self.is_winner(board, (i, j)):
                        return (i, j)
                    board[i, j] = self.blank_symbol
        
        # Step 2: Block the opponent's winning move
        for i in range(15):
            for j in range(15):
                if board[i, j] == self.blank_symbol:
                    board[i, j] = self.opponent_symbol
                    if self.is_winner(board, (i, j)):
                        board[i, j] = self.blank_symbol
                        return (i, j)
                    board[i, j] = self.blank_symbol
        
        # Step 3: Create multiple threats (fork strategy)
        best_move = None
        max_threats = 0
        for i in range(15):
            for j in range(15):
                if board[i, j] == self.blank_symbol:
                    threat_count = self.count_potential_wins(board, (i, j), self.agent_symbol)
                    if threat_count > max_threats:
                        max_threats = threat_count
                        best_move = (i, j)
        
        if best_move:
            return best_move
        
        # Step 4: Default to random move if no strategic advantage is found
        i = random.randint(0, 14)
        j = random.randint(0, 14)
        while board[i, j] != self.blank_symbol:
            i = random.randint(0, 14)
            j = random.randint(0, 14)
        return (i, j)
    
    def is_winner(self, board, move):
        i, j = move
        player = board[i, j]

        def check(values):
            counter = 0
            for value in values:
                if value == player:
                    counter += 1
                else:
                    counter = 0
                if counter >= 5:
                    return True
            return False

        c1 = check(board[i, :])  # Check row
        c2 = check(board[:, j])  # Check column
        c3 = check(board.diagonal(j-i))  # Check main diagonal
        c4 = check(np.fliplr(board).diagonal(board.shape[0]-i-j-1))  # Check anti-diagonal

        return c1 or c2 or c3 or c4
    
    def count_potential_wins(self, board, move, symbol):
        i, j = move
        potential_wins = 0
        
        # Temporarily place the symbol on the board to evaluate the position
        board[i, j] = symbol

        if self.is_winner(board, (i, j)):
            potential_wins += 1
        
        # Reset the board after evaluation
        board[i, j] = self.blank_symbol
        
        return potential_wins
