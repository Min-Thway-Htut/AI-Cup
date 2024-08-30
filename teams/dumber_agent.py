import numpy as np
import random

class GomokuAgent:
    
    def __init__(self, agent_symbol, blank_symbol, opponent_symbol):
        self.name = "Min's Agent"
        self.agent_symbol = agent_symbol
        self.blank_symbol = blank_symbol
        self.opponent_symbol = opponent_symbol
        self.board_size = 15

    def play(self, board):
        # Use heuristic to find the best move based on threat detection and scoring
        move = self.find_best_move(board)
        return move if move else self.get_random_move(board)

    def find_best_move(self, board):
        best_move = None
        max_score = -float('inf')

        # First, check if there are any winning moves for the opponent that need to be blocked
        for move in self.get_valid_moves(board):
            i, j = move
            board[i, j] = self.opponent_symbol
            if self.is_winner(board, move):
                board[i, j] = self.blank_symbol  # Undo move
                return move  # Block the opponent's winning move
            board[i, j] = self.blank_symbol  # Undo move

        # If no immediate threat, find the best move for the agent
        for move in self.get_valid_moves(board):
            i, j = move
            board[i, j] = self.agent_symbol
            score = self.evaluate_board(board)
            board[i, j] = self.blank_symbol

            if score > max_score:
                max_score = score
                best_move = move
        
        if best_move is None:
            best_move = self.get_random_move(board)
        
        return best_move

    def evaluate_board(self, board):
        score = 0
        
        # Evaluate rows, columns, and diagonals
        for i in range(self.board_size):
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
        return [(i, j) for i in range(self.board_size) for j in range(self.board_size) if board[i, j] == self.blank_symbol]
    
    def get_random_move(self, board):
        valid_moves = self.get_valid_moves(board)
        return random.choice(valid_moves) if valid_moves else None

    def is_winner(self, board, move):
        i, j = move
        player = board[i, j]

        def check(values):
            count = 0
            for value in values:
                if value == player:
                    count += 1
                else:
                    count = 0
                if count >= 5:
                    return True
            return False

        # Check row, column, and diagonals
        return (check(board[i, :]) or  # Row
                check(board[:, j]) or  # Column
                check(board.diagonal(j-i)) or  # Main diagonal
                check(np.fliplr(board).diagonal(self.board_size - i - j - 1)))  # Anti-diagonal

    def detect_threats(self, board, move):
        i, j = move
        threat_score = 0

        def check_line(line, symbol):
            threat = 0
            for i in range(len(line) - 4):
                segment = line[i:i+5]
                if np.sum(segment == symbol) >= 4:
                    threat += 1
            return threat

        # Check all directions for threats
        threat_score += check_line(board[i, :], self.agent_symbol)  # Row
        threat_score += check_line(board[:, j], self.agent_symbol)  # Column
        threat_score += check_line(board.diagonal(i-j), self.agent_symbol)  # Main diagonal
        threat_score += check_line(np.fliplr(board).diagonal(self.board_size - i - j - 1), self.agent_symbol)  # Anti-diagonal
        
        return threat_score