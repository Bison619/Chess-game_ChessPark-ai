from AI.PointMap import map_points, PieceMap
from pieces import Pawn


class TranspositionTable:
    def __init__(self):
        self.table = {}

    def lookup(self, board_hash, depth, alpha, beta):
        if board_hash in self.table:
            entry = self.table[board_hash]
            if entry['depth'] >= depth:
                if entry['flag'] == 'exact':
                    return entry['score']
                elif entry['flag'] == 'lowerbound' and entry['score'] > alpha:
                    alpha = entry['score']
                elif entry['flag'] == 'upperbound' and entry['score'] < beta:
                    beta = entry['score']
                if alpha >= beta:
                    return entry['score']
        return None

    def store(self, board_hash, depth, score, alpha, beta):
        entry = {'depth': depth, 'score': score}
        if score <= alpha:
            entry['flag'] = 'upperbound'
        elif score >= beta:
            entry['flag'] = 'lowerbound'
        else:
            entry['flag'] = 'exact'
        self.table[board_hash] = entry

class Minimax(object):
    def __init__(self, depth, board, AlphBetaPruning=True, UsePointMaps=True):
        self.depth = depth
        self.board = board
        self.AlphaBetaPruning = AlphBetaPruning
        self.UsePointMaps = UsePointMaps
        self.transposition_table = TranspositionTable()

    def Start(self, depth):
        bestMove = None
        bestScore = -9999
        currentPiece = None
        isMaximizer = self.board.player == 1

        if not isMaximizer:
            bestScore *= -1

        for pieces in self.board.grid:
            for piece in pieces:
                if piece and piece.color == self.board.player:
                    moves, captures = self.board.GetAllowedMoves(piece, True)
                    possibleMoves = captures + moves
                    for position in possibleMoves:
                        prev_pos = piece.position
                        pion = self.board.MoveSimulation(piece, position)
                        score = self.minimax(depth + 1, not isMaximizer, -10000, 10000)
                        if type(piece) == Pawn and (position.y == 7 or position.y == 0):
                            score += 80
                        elif self.board.isEnPassant(piece, position):
                            score += 10
                        if not isMaximizer:
                            score *= -1
                        if score >= bestScore and isMaximizer:
                            bestScore = score
                            bestMove = position
                            currentPiece = piece

                        if pion is None:
                            self.board.MoveSimulation(piece, prev_pos)
                        else:
                            self.board.MoveSimulation(piece, prev_pos)
                            self.board.MoveSimulation(pion, position)
        return currentPiece, bestMove

    def minimax(self, depth, isMaximizer, alpha, beta):
        board_hash = self.board.hash()
        tt_entry = self.transposition_table.lookup(board_hash, depth, alpha, beta)
        if tt_entry is not None:
            return tt_entry

        if self.depth == depth:
            return self.Evaluate() * -1

        if isMaximizer:
            bestScore = -9999
            possibleMoves = self.LegalMoves(1, 7)
            for _index in range(len(possibleMoves) - 1, -1, -1):
                piece = possibleMoves[_index][1]
                i = possibleMoves[_index][2]
                prev_pos = piece.position
                pion = self.board.MoveSimulation(piece, i)
                score = self.minimax(depth + 1, False, alpha, beta)
                bestScore = max(bestScore, score)
                if self.AlphaBetaPruning:
                    alpha = max(alpha, bestScore)
                self.UndoMove(pion, piece, prev_pos, i)

                if beta <= alpha and self.AlphaBetaPruning:
                    break

            self.transposition_table.store(board_hash, depth, bestScore, alpha, beta)
            return bestScore
        else:
            bestScore = 9999
            possibleMoves = self.LegalMoves(0, 0)
            for _index in range(len(possibleMoves) - 1, -1, -1):
                piece = possibleMoves[_index][1]
                i = possibleMoves[_index][2]
                prev_pos = piece.position
                currentPiece = self.board.MoveSimulation(piece, i)
                score = self.minimax(depth + 1, True, alpha, beta)
                bestScore = min(bestScore, score)
                if self.AlphaBetaPruning:
                    beta = min(beta, bestScore)
                self.UndoMove(currentPiece, piece, prev_pos, i)
                if beta <= alpha and self.AlphaBetaPruning:
                    break

            self.transposition_table.store(board_hash, depth, bestScore, alpha, beta)
            return bestScore

    def Evaluate(self):
        totalScore = 0
        for pieces in self.board.grid:
            for piece in pieces:
                if piece:
                    p_map = PieceMap(piece)
                    score = piece.value
                    if self.UsePointMaps:
                        score += p_map[piece.position.y][piece.position.x]
                    totalScore += score
        return totalScore

    def UndoMove(self, currentPiece, piece, prev_pos, p):
        if currentPiece is None:
            self.board.MoveSimulation(piece, prev_pos)
        else:
            self.board.MoveSimulation(piece, prev_pos)
            self.board.MoveSimulation(currentPiece, p)

    def GetMoves(self, piece, position):
        bestMoves = []
        possibleMoves = []
        moves, captures = self.board.GetAllowedMoves(piece, True)
        for pos in captures:
            if self.board.grid[pos.x][pos.y]:
                bestMoves.append([10 * self.board.grid[pos.x][pos.y].value - piece.value, piece, pos])
                if type(piece) == Pawn and (pos.y == position):
                    bestMoves[-1][0] += 90
            else:
                bestMoves.append([piece.value, piece, pos])
        for pos in moves:
            if type(piece) == Pawn and (pos.y == position):
                bestMoves.append([90, piece, pos])
            else:
                bestMoves.append([0, piece, pos])

        return possibleMoves, bestMoves

    def LegalMoves(self, color, pos):
        possibleMoves = []
        bestMoves = []
        for pieces in self.board.grid:
            for piece in pieces:
                if piece and piece.color == color:
                    temp_moves, better_temp_moves = self.GetMoves(piece, pos)
                    possibleMoves += temp_moves
                    bestMoves += better_temp_moves

        bestMoves.sort(key=lambda key: key[0])
        possibleMoves += bestMoves
        return possibleMoves
