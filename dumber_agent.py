import numpy as np
import random

class GomokuAgent:
    
    def __init__(self, agent_symbol, blank_symbol, opponent_symbol):
        self.name = "Agent Two"
        self.agent_symbol = agent_symbol
        self.blank_symbol = blank_symbol
        self.opponent_symbol = opponent_symbol
    
    def play(self, board):
        best_move = self.find_best_move(board)
        return best_move
    
    def find_best_move(self, board):
        best_move = None
        max_score = -float('inf')
        
        # Try to find the best move based on heuristic evaluation
        for move in self.get_valid_moves(board):
            i, j = move
            board[i, j] = self.agent_symbol
            score = self.evaluate_board(board)
            board[i, j] = self.blank_symbol
            
            if score > max_score:
                max_score = score
                best_move = move
        
        # If no good move found, pick a random valid move
        if best_move is None:
            best_move = self.get_random_move(board)
        
        return best_move
    
    def evaluate_board(self, board):
        score = 0
        
        # Evaluate rows, columns, and diagonals
        for i in range(15):
            score += self.evaluate_line(board[i, :])  # Row
            score += self.evaluate_line(board[:, i])  # Column
        
        # Diagonals
        score += self.evaluate_line(board.diagonal())
        score += self.evaluate_line(np.fliplr(board).diagonal())
        
        return score
    
    def evaluate_line(self, line):
        score = 0
        for i in range(len(line) - 4):
            segment = line[i:i+5]
            score += self.evaluate_segment(segment)
        return score
    
    def evaluate_segment(self, segment):
        agent_count = np.sum(segment == self.agent_symbol)
        opponent_count = np.sum(segment == self.opponent_symbol)
        
        if agent_count == 5:
            return 10000  # Winning
        elif agent_count == 4 and opponent_count == 0:
            return 1000  # Strong potential win
        elif agent_count == 3 and opponent_count == 0:
            return 100  # Moderate potential win
        elif opponent_count == 4 and agent_count == 0:
            return -1000  # Block opponent's win
        elif opponent_count == 3 and agent_count == 0:
            return -100  # Block opponent's potential win
        
        return 0
    
    def get_valid_moves(self, board):
        return [(i, j) for i in range(15) for j in range(15) if board[i, j] == self.blank_symbol]
    
    def get_random_move(self, board):
        valid_moves = self.get_valid_moves(board)
        return random.choice(valid_moves) if valid_moves else None