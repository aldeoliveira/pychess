"""
Tarefas:
 - Descobrir como pedir para o pycharm parar de verificar a ordografia
 - O que é o comando "def "?
 - O que é o "self"?
 - Baixar Slack
"""


import pygame as p  # Importa as funções do pygame para o código, com o prefixo "p."
from Chess import ChessEngine  # Importa as funções do arquivo ChessEngine.py

WIDTH = HEIGHT = 512  # Largura e altura do display
DIMENSION = 8  # Número de casas numa coluna ou fileira
SQ_SIZE = HEIGHT//DIMENSION  # Tamanho das casas
MAX_FPS = 15  # ???
IMAGES = {}  # Arquiva as imagens


def loadImages():
    pieces = ['bP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'wP', 'wR', 'wN', 'wB', 'wQ', 'wK']
    for piece in pieces:  # Para cada peça, importa a figura da peça em escala
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


"""
Driver principal do código. Lida com os inputs do usuário e faz update das figuras
"""


def main():
    p.init()  # Inicializa os módulos do pygame
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()
    running = True  # Variável que indica se o programa deve ou não estar rodando. Começa como True.
    sqSelected = ()  # Vetor da casa selecionada. Mantém a última casa selecionada. Uma tuple (row, col).
    playerClicks = []  # Guarda um par de cliques do usuário. Duas tuples (row, col).
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:  # Se clicar o botão de sair...
                running = False  # o programa deve parar de rodar
            elif e.type == p.MOUSEBUTTONDOWN:  # Se o usuário pressionar uma casa...
                location = p.mouse.get_pos()  # pega a posição x,y do mouse
                col = location[0]//SQ_SIZE  # localiza em que coluna o mouse está de acordo com o tamanho das casas
                row = location[1]//SQ_SIZE  # localiza em que fileira o mouse está de acordo com o tamanho das casas
                if sqSelected == (row, col):  # Se o usuário clicou na mesma casa duas vezes...
                    sqSelected = ()  # desfaz a seleção da casa
                    playerClicks = []  # esvazia o vetor do par de cliques
                else:  # se o usuário clicou em casas diferentes...
                    sqSelected = (row, col)  # guarda a posição clicada, em fileiras e colunas
                    playerClicks.append(sqSelected)  # arquiva a posição clicada
                if len(playerClicks) == 2:  # Se o usuário fez um segundo clique...
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(playerClicks)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = ()  # reseta a casa selecionada
                    playerClicks = []  # esvazia o registro de cliques
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


"""
Responsável por todos os desenhos
"""


def drawGameState(screen, gs):
    drawBoard(screen)  # Desenha as casas do tabuleiro
    # Adiciona indicações de peças/casas e sugestões de lances
    drawPieces(screen, gs.board)  # Desenha as peças sobre as casas


"""
Desenha as casas do tabuleiro
"""


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""
Desenha as peças usando o GameState.board
"""


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
