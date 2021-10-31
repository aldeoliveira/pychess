import ChessMove
import ChessCastleRights


class ValidMoves:

    move_class = ChessMove.Move
    castle_rights = ChessCastleRights.CastleRights

    def __init__(self, current_gamestate):
        self.board = current_gamestate.board
        self.white_to_move = current_gamestate.white_to_move
        self.move_functions = {'P': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                               'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}
        self.white_king_location = (7, 4)  # Posição inicial do rei branco
        self.black_king_location = (0, 4)  # Posição inicial do rei negro
        self.pins = []
        self.checks = []
        self.en_passant_possible = current_gamestate.en_passant_possible  # Casa em que uma captura en passant é possível
        self.en_passant_log = []
        self.in_check = False
        self.current_castling_rights = current_gamestate.current_castling_rights

    def get_valid_moves(self):
        moves = []
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()
        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        if self.in_check:
            if len(self.checks) == 1:  # Verificar se há apenas uma peça dando xeque
                moves = self.get_all_possible_moves()
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = []
                if piece_checking[1] == 'N':
                    valid_squares = [check_row, check_col]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_moved[1] != 'K':
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
            else:
                self.get_king_moves(king_row, king_col, moves)
        else:
            moves = self.get_all_possible_moves()

        if self.white_to_move:
            self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves)
        else:
            self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves)

        return moves

    def in_check(self):  # Verifica se está em xeque
        if self.white_to_move:  # Se for a vez de as brancas jogarem, consulta se o rei branco está sob ataque
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:  # Se for a vez de as pretas jogarem, consulta se o rei negro está sob ataque
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    def square_under_attack(self, r, c):
        self.white_to_move = not self.white_to_move  # Muda para o ponto de vista do oponente
        opponent_moves = self.get_all_possible_moves()  # Obtem os lances do oponente
        self.white_to_move = not self.white_to_move  # Muda de volta o ponto de vista
        for move in opponent_moves:
            if move.end_row == r and move.end_col == c:
                return True
        return False

    def get_all_possible_moves(self):
        moves = []  # Cria um vetor de movimentos possíveis, inicialmente vazio
        for r in range(len(self.board)):  # Percorre o tabuleiro
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]  # Verifica a cor da peça
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):  # Se a peça for
                    # branca e for a vez de as brancas jogarem ou se a peça for preta e for a vez das pretas jogarem...
                    piece = self.board[r][c][1]  # Verifica o tipo de peça
                    self.move_functions[piece](r, c, moves)  # chama a função apropriada para cada tipo de peça
        return moves

    def get_pawn_moves(self, r, c, moves):
        # Varre a lista de peças cravadas para saber se esse peão está cravado
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        # Pega a fileira inicial e a direção do peão de acordo com a cor
        pawn_step = 1
        second_rank = 1
        enemy_color = 'w'
        if self.white_to_move:
            pawn_step = -1
            second_rank = 6
            enemy_color = 'b'

        if self.board[r + pawn_step][c] == "--":  # Se a casa à frente estiver disponível
            if not piece_pinned or pin_direction == (pawn_step, 0):  # e se o peão não estiver cravado ou a diração da cravada for igual à direção de movimento
                moves.append(self.move_class((r, c), (r + pawn_step, c), self.board))  # Acrescenta o lance como possível
                if r == second_rank and self.board[r + pawn_step * 2][c] == "--":  # Se o peão estiver na segunda fileira e a segunda casa à frente estiver livre
                    moves.append(self.move_class((r, c), (r + pawn_step * 2, c), self.board))  # Acrescenta o lance como possível
        for capture_side in (-1, 1):  # Para cada lado de captura
            if 0 <= c + capture_side <= 7:  # Verifica se está dentro do tabuleiro
                if self.board[r + pawn_step][c + capture_side][0] == enemy_color:  # Se houver uma peça inimiga na casa de captura
                    if not piece_pinned or pin_direction == (pawn_step, capture_side):  # Se o peão não estiver cravado ou a direção de cravada for igual à direção de captura
                        moves.append(self.move_class((r, c), (r + pawn_step, c + capture_side), self.board))
                elif (r + pawn_step, c + capture_side) == self.en_passant_possible:  # Se a casa de captura for uma casa em que o en passant é possível
                    if not piece_pinned or pin_direction == (pawn_step, capture_side):
                        moves.append(self.move_class((r, c), (r + pawn_step, c + capture_side), self.board, is_en_passant_move=True))

    def get_rook_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # vetores de direção
        enemy_color = "b" if self.white_to_move else "w"  # determina a cor das peças que podem ser capturadas
        for d in directions:  # Para cada direção...
            for i in range(1, 8):  # Para cada casa em cada direção...
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # Limita o escopo dentro do tabuleiro
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = self.board[end_row][end_col]  # Identifica qual peça está na casa analisada
                        if end_piece == "--":  # Se a casa estiver vazia
                            moves.append(self.move_class((r, c), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:  # Se a casa tiver uma peça inimiga...
                            moves.append(self.move_class((r, c), (end_row, end_col), self.board))
                            break  # ... e não analisa nenhuma casa depois dela
                        else:
                            break  # Se a casa não está vazia e a peça ocupante não é inimiga, pára a análise
                else:
                    break  # Se chegar na bora do tabuleiro, pára a análise

    def get_knight_moves(self, r, c, moves):
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break
        knight_moves = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2))
        ally_color = "w" if self.white_to_move else "b"
        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:
                        moves.append(self.move_class((r, c), (end_row, end_col), self.board))

    def get_bishop_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":
                            moves.append(self.move_class((r, c), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:
                            moves.append(self.move_class((r, c), (end_row, end_col), self.board))
                            break
                        else:
                            break
                else:
                    break

    def get_queen_moves(self, r, c, moves):
        self.get_bishop_moves(r, c, moves)
        self.get_rook_moves(r, c, moves)

    def get_king_moves(self, r, c, moves):
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = "w" if self.white_to_move else "b"  # identifica qual a cor das peças aliadas
        for i in range(8):
            end_row = r + row_moves[i]
            end_col = c + col_moves[i]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # Se a casa de destino estiver dentro do tabuleiro...
                end_piece = self.board[end_row][end_col]  # verifica o que está na casa de destino
                if end_piece[0] != ally_color:
                    if ally_color == 'w':
                        self.white_king_location = (end_row, end_col)
                    else:
                        self.black_king_location = (end_row, end_col)
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    if not in_check:
                        moves.append(self.move_class((r, c), (end_row, end_col), self.board))
                    if ally_color == 'w':
                        self.white_king_location = (r, c)
                    else:
                        self.black_king_location = (r, c)

    def get_castle_moves(self, r, c, moves):  # Gera todos os lances legais de roque
        if self.square_under_attack(r, c):
            return
        if (self.white_to_move and self.current_castling_rights.wks) or \
                (not self.white_to_move and self.current_castling_rights.bks):
            self.get_kingside_castle_moves(r, c, moves)
        if (self.white_to_move and self.current_castling_rights.wqs) or \
                (not self.white_to_move and self.current_castling_rights.bqs):
            self.get_queenside_castle_moves(r, c, moves)

    def get_kingside_castle_moves(self, r, c, moves):
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
            if not self.square_under_attack(r, c + 1) and not self.square_under_attack(r, c + 2):
                moves.append(self.move_class((r, c), (r, c + 2), self.board, is_castle_move=True))

    def get_queenside_castle_moves(self, r, c, moves):
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--':
            if not self.square_under_attack(r, c - 1) and not self.square_under_attack(r, c - 2):
                moves.append(self.move_class((r, c), (r, c - 2), self.board, is_castle_move=True))

    def check_for_pins_and_checks(self):
        pins = []
        checks = []
        in_check = False
        if self.white_to_move:
            enemy_color = 'b'
            ally_color = 'w'
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = 'w'
            ally_color = 'b'
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != 'K':
                        if possible_pin == ():
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:
                            break
                    elif end_piece[0] == enemy_color:
                        piece_type = end_piece[1]
                        # 5 possibilidades nessa condicional:
                        # 1) Ortogonal ao rei e é uma torre
                        # 2) Diagonal ao rei e é um bispo
                        # 3) Uma casa na diagonal e é um peão
                        # 4) A qualquer direção e é uma dama
                        # 5) Uma casa em qualquer direção e é um rei
                        if (0 <= j <= 3 and piece_type == 'R') or \
                                (4 <= j <= 7 and piece_type == 'B') or \
                                (i == 1 and piece_type == 'P'
                                 and ((enemy_color == 'w' and 6 <= j <= 7) or (enemy_color == 'b' and 4 <= j <= 5))) or \
                                (piece_type == 'Q') or (i == 1 and piece_type == 'K'):
                            if possible_pin == ():
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else:
                                pins.append(possible_pin)
                                break
                        else:
                            break
                else:
                    break  # off board
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knight_moves:
            end_row = start_row + m[0]
            end_col = start_col + m[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == 'N':
                    in_check = True
                    checks.append((end_row, end_col, m[0], m[1]))
        return in_check, pins, checks
