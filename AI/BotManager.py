from AI.ChessAI import Minimax

bot_difficulties = {
    "Begineer1": 1,
    "Begineer2": 2,
    "Begineer3": 3,
    "Intermediate1": 4,
    "Intermediate2": 4,
    "Expert": 5
}

class BotManager:
    def __init__(self, board):
        self.board = board

    def create_bot(self, difficulty):
        depth = bot_difficulties[difficulty]
        return Minimax(depth, self.board)
