import numpy as np

class GomokuAgent:
    def __init__(self, agent_symbol, blank_symbol, opponent_symbol, max_depth=5):
        self.name = "First Agent"
        self.agent_symbol = agent_symbol
        self.blank_symbol = blank_symbol
        self.opponent_symbol = opponent_symbol
        self.max_depth = max_depth

    def play(self, board):
        return max(self.get_available_moves(board), key=lambda move: self.search(board, move))

    def search(self, board, move, depth=0, alpha=-float('inf'), beta=float('inf')):
        if depth == self.max_depth or self.is_winner(board, move):
            return self.evaluate_move(board, move)
        
        best_score = -float('inf')
        for child_move in self.get_child_moves(board, move):
            score = -self.search(self.make_move(board, child_move), child_move, depth + 1, -beta, -alpha)
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return best_score

    def evaluate_move(self, board, move):
        return (
            1000 if self.is_winner(board, move) else
            500 if self.is_winner(self.make_move(board, move, self.opponent_symbol), move) else
            200 if move == (len(board) // 2, len(board) // 2) else
            100 if any(board[move[0]+di, move[1]+dj] == self.blank_symbol
                       for di in [-1, 0, 1] for dj in [-1, 0, 1]
                       if 0 <= move[0]+di < len(board) and 0 <= move[1]+dj < len(board)) else
            0
        )

    def is_winner(self, board, move):
        player = board[move]
        lines = [board[move[0], :], board[:, move[1]],
                 board.diagonal(move[1] - move[0]),
                 np.fliplr(board).diagonal(len(board) - move[1] - 1 - move[0])]
        return any(np.all(line[i:i+5] == player) for line in lines for i in range(len(line) - 4))

    def get_child_moves(self, board, move):
        return [(move[0]+di, move[1]+dj) for di in [-1, 0, 1] for dj in [-1, 0, 1]
                if 0 <= move[0]+di < len(board) and 0 <= move[1]+dj < len(board) and board[move[0]+di, move[1]+dj] == self.blank_symbol]

    def get_available_moves(self, board):
        return list(zip(*np.where(board == self.blank_symbol)))

    def make_move(self, board, move, player=None):
        new_board = board.copy()
        new_board[move] = player or self.agent_symbol
        return new_board