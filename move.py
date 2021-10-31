"""
Coisas a acrescentar:
 1) quando for dado o comando print(objeto_desta_classe), deve-se retornar o lance em notação algébrica
 2) Devem haver um atributos especificando se o lance é:
        - roque na ala do rei
        - roque na ala da dama
        - xeque (depende da posição das outras peças no tabuleiro)
        - xeque-duplo (depende da posição das outras peças no tabuleiro)
        - cheque-mate (depende da posição das outras peças no tabuleiro)
        - xeque descoberto (depende da posição das outras peçcas no tabuleiro)
        - captura en passant (depende da posição das outras peças no tabuleiro)
"""


class Move:  # Classe que vai passar os lances para o tabuleiro
    # Dicionário que associa a notação algébrica às casas do tabuleiro
    rank_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in rank_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, is_en_passant_move=False, is_castle_move=False):
        self.start_row = start_sq[0]  # coloca a fileira de saída no vetor casa inicial
        self.start_col = start_sq[1]  # coloca a coluna de saída no vetor casa inicial
        self.end_row = end_sq[0]  # coloca a fileira de chegada no vetor casa final
        self.end_col = end_sq[1]  # coloca a coluna de chegada no vetor casa final
        self.piece_moved = board[self.start_row][self.start_col]  # guarda qual peça foi movida
        self.player_color = self.piece_moved[0]
        self.piece_captured = board[self.end_row][self.end_col]  # guarda qual peça foi capturada
        self.is_pawn_promotion = (self.piece_moved == 'wP' and self.end_row == 0) or \
                                 (self.piece_moved == 'bP' and self.end_row == 7)
        self.is_en_passant_move = is_en_passant_move
        if self.is_en_passant_move:
            self.piece_captured = board[self.start_row][self.end_col]
        self.is_castle_move = is_castle_move
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        return self.moveID == other.moveID

    def __str__(self):
        pass

    def get_chess_notation(self):  # Traduz para notação algébrica as casas de saída e de destino
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):  # Traduz para notação algébrica a casa selecionada
        return self.cols_to_files[c] + self.rows_to_ranks[r]
