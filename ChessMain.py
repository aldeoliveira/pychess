"""
DEBUG
 - Problema com os direitos de roque
"""


import pygame
import ChessGameState
import ChessMove
import ChessGraphics
import ChessValidMoves

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15


class ChessMain:
    """
    Esta classe gerencia os comandos do usuário.
    """

    current_gamestate = None
    valid_moves_class = None
    graphic_resources = None
    move_class = None

    def __init__(self):
        pygame.init()

        self.game_over = False
        self.last_square_clicked = ()
        self.pair_of_clicks = []
        self.running = True
        self.valid_moves_for_current_position = None

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(pygame.Color("White"))
        self.clock = pygame.time.Clock()

    def main(self):
        """
        Captura em tempo real os inputs do usuário.
        """
        self.load_images()
        self.set_new_game()

        while self.running:
            self.event_controls()
            self.draw_gamestate()
            self.maybe_finish_game()
            self.clock.tick(MAX_FPS)
            pygame.display.flip()

    def load_images(self):
        self.graphic_resources = ChessGraphics.Graphics()
        self.graphic_resources.load_images()

    def set_new_game(self):
        """
        Reseta os atributos para uma nova partida.
        """
        self.current_gamestate = ChessGameState.GameState()
        self.get_valid_moves_for_current_position()

        self.game_over = False
        self.last_square_clicked = ()
        self.pair_of_clicks = []
        self.running = True

    def get_valid_moves_for_current_position(self):
        self.valid_moves_class = ChessValidMoves.ValidMoves(self.current_gamestate)
        self.valid_moves_for_current_position = self.valid_moves_class.get_valid_moves()

    def event_controls(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
            elif e.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                self.select_square_by_left_click()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:  # Desfazer quando 'z' for pressionado
                    self.undo_move()
                if e.key == pygame.K_r:  # Resetar o tabuleiro quando 'r' for pressionado
                    self.set_new_game()

    def select_square_by_left_click(self):  # Gerencia o botão esquerdo do mouse
        location = pygame.mouse.get_pos()  # pega a posição x,y do mouse
        col = location[0] // SQ_SIZE  # localiza em que coluna o mouse está
        row = location[1] // SQ_SIZE  # localiza em que fileira o mouse está
        self.select_squares(row, col)

    def select_squares(self, row, col):
        if self.last_square_clicked == (row, col):  # Se o usuário clicou na mesma casa duas vezes...
            self.last_square_clicked = ()  # desfaz a seleção da casa
            self.pair_of_clicks = []  # esvazia o vetor do par de cliques
        else:
            self.last_square_clicked = (row, col)
            self.pair_of_clicks.append(self.last_square_clicked)
        if len(self.pair_of_clicks) == 2:
            move = ChessMove.Move(self.pair_of_clicks[0], self.pair_of_clicks[1], self.current_gamestate.board)
            valid_move_chosen = self.check_if_move_is_valid(move)
            if valid_move_chosen:
                self.execute_move(valid_move_chosen)
            else:
                self.pair_of_clicks = [self.last_square_clicked]

    def check_if_move_is_valid(self, move):
        valid_move_chosen = None
        for valid_move in range(len(self.valid_moves_for_current_position)):
            if move == self.valid_moves_for_current_position[valid_move]:
                valid_move_chosen = self.valid_moves_for_current_position[valid_move]
        return valid_move_chosen

    def execute_move(self, move_chosen):
        self.current_gamestate.make_move(move_chosen)
        print(move_chosen.get_chess_notation())
        self.get_valid_moves_for_current_position()
        self.make_animation()
        self.last_square_clicked = ()
        self.pair_of_clicks = []

    def make_animation(self):
        self.graphic_resources.animate_move(self.current_gamestate.move_log[-1], self.screen,
                                            self.current_gamestate.board, self.clock)

    def undo_move(self):
        self.current_gamestate.undo_move()
        self.get_valid_moves_for_current_position()

    def draw_gamestate(self):
        self.graphic_resources.draw_gamestate(self.screen, self.current_gamestate,
                                              self.valid_moves_for_current_position, self.last_square_clicked)

    def maybe_finish_game(self):
        if self.current_gamestate.checkmate or self.current_gamestate.stalemate:
            self.graphic_resources.game_finished_message(self.current_gamestate, self.screen)

    def print_valid_moves(self):
        print("Lista de lances válidos:")
        list_of_valid_moves = []
        for move in self.valid_moves_for_current_position:
            list_of_valid_moves.append(move.get_chess_notation())
        print(list_of_valid_moves)


if __name__ == "__main__":
    chess_main = ChessMain()
    chess_main.main()
