import pygame

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
IMAGES = {}
ANIMATION_FPS = 60

COLORS = [pygame.Color("white"), pygame.Color("gray")]


class Graphics:
    def load_images(self):  # Coloca as peças na posição inicial no tabuleiro
        pieces = ['bP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'wP', 'wR', 'wN', 'wB', 'wQ', 'wK']
        for piece in pieces:  # Para cada peça, importa a figura da peça em escala
            IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

    def game_finished_message(self, current_gamestate, screen):
        if current_gamestate.checkmate:
            if current_gamestate.white_to_move:
                self.draw_text(screen, 'Black wins by checkmate')
            else:
                self.draw_text(screen, 'White wins by checkmate')
        elif current_gamestate.stalemate:
            self.draw_text(screen, 'Stalemate')

    def draw_gamestate(self, screen, current_gamestate, valid_moves, sq_selected):
        self.draw_board(screen)  # Desenha as casas do tabuleiro
        self.highlight_squares(screen, current_gamestate, valid_moves, sq_selected)
        self.draw_pieces(screen, current_gamestate.board)  # Desenha as peças sobre as casas

    def draw_board(self, screen):
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                color = COLORS[((r + c) % 2)]
                pygame.draw.rect(screen, color, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def highlight_squares(self, screen, gs, valid_moves, sq_selected):
        if sq_selected != ():
            r, c = sq_selected
            if gs.board[r][c][0] == ('w' if gs.white_to_move else 'b'):
                s = pygame.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(100)  # "valor de transparência: 0-255 (transparente-opaco)
                s.fill(pygame.Color("blue"))
                screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
                s.fill(pygame.Color('yellow'))
                for move in valid_moves:
                    if move.start_row == r and move.start_col == c:
                        screen.blit(s, (SQ_SIZE * move.end_col, SQ_SIZE * move.end_row))

    def draw_pieces(self, screen, board):
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                piece = board[r][c]
                if piece != "--":
                    screen.blit(IMAGES[piece], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def animate_move(self, move, screen, board, clock):
        delta_row = move.end_row - move.start_row  # deslocamento da peça em fileiras
        delta_col = move.end_col - move.start_col  # deslocamento da peça em colunas
        duration_in_frames = 10  # número de frames da animação
        color = COLORS[(move.end_row + move.end_col) % 2]
        pawn_captured_en_passant_square = pygame.Rect(move.end_col * SQ_SIZE, move.start_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)

        for frame in range(duration_in_frames + 1):  # Em cada frame da animação...
            self.draw_board(screen)  # Desenha o tabuleiro
            self.draw_pieces(screen, board)  # Desenha as peças
            r = move.start_row + (delta_row * frame/duration_in_frames)  # Coordenada no eixo das fileiras
            c = move.start_col + (delta_col * frame/duration_in_frames)  # Coordenada no eixo das colunas

            # Desenha a casa de destino da peça
            end_square = pygame.Rect(move.end_col * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, color, end_square)

            # Desenha a peça a ser capturada
            if move.piece_captured != '--':
                if move.is_en_passant_move:
                    screen.blit(IMAGES[move.piece_captured], pawn_captured_en_passant_square)
                else:
                    screen.blit(IMAGES[move.piece_captured], end_square)

            # Desenha a peça movida
            screen.blit(IMAGES[move.piece_moved], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            pygame.display.flip()
            clock.tick(ANIMATION_FPS)

    def draw_text(self, screen, text):
        font = pygame.font.SysFont("Helvetica", 32, True, False)
        text_object = font.render(text, 0, pygame.Color('Grey'))
        text_location = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2,
                                                              HEIGHT / 2 - text_object.get_height() / 2)
        screen.blit(text_object, text_location)
        text_object = font.render(text, 0, pygame.Color("Black"))
        screen.blit(text_object, text_location.move(2, 2))
    pass
