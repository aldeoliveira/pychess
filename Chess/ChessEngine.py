class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):  # Função que executa os lances no tabuleiro
        self.board[move.startRow][move.startCol] = "--"  # Retira a peça da casa de saída
        self.board[move.endRow][move.endCol] = move.pieceMoved  # Coloca a peça movida na casa de detino
        self.moveLog.append(move)  # guarda o lance para que possamos desfazê-lo mais tarde
        self.whiteToMove = not self.whiteToMove  # troca o jogador que deve fazer o próximo lance


class Move:  # Classe que vai passar os lances para o tabuleiro
    # Dicionário que associa a notação algébrica às casas do tabuleiro
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]  # coloca a fileira de saída no vetor casa inicial
        self.startCol = startSq[1]  # coloca a coluna de saída no vetor casa inicial
        self.endRow = endSq[0]  # coloca a fileira de chegada no vetor casa final
        self.endCol = endSq[1]  # coloca a coluna de chegada no vetor casa final
        self.pieceMoved = board[self.startRow][self.startCol]  # guarda qual peça foi movida
        self.pieceCaptured = board[self.endRow][self.endCol]  # guarda qual peça foi capturada

    def getChessNotation(self):  # Traduz para notação algébrica as casas de saída e de destino
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):  # Traduz para notação algébrica a casa selecionada
        # return self.colsToFiles[c] + self.ranksToRows[r]
        return self.colsToFiles[c] + self.rowsToRanks[r]
