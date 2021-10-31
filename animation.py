import pygame

ANIMATION_FPS = 60


class Animations:
    def __init__(self, move, frame_count, sq_size):
        self.colors = []
        self.start_row = move.start_row
        self.start_col = move.start_col
        self.end_row = move.end_row
        self.end_col = move.end_col
        self.piece_captured = move.piece_captured
        self.piece_moved = move.piece_moved
        self.frame_count = frame_count
        self.sq_size = sq_size

    def animate_move(self):
        dr = self.end_row - self.start_row
        dc = self.end_col - self.start_col
        for frame in range(self.frame_count + 1):
            r, c = (self.start_row + dr * (frame/self.frame_count), self.start_col + dc * (frame/self.frame_count))
            draw_board(screen)
            draw_pieces(screen, board)
            color = self.colors[(self.end_row + self.end_col) % 2]
            end_square = pygame.Rect(self.end_col * self.sq_size, self.end_row * self.sq_size, self.sq_size, self.sq_size)
            pygame.draw.rect(screen, color, end_square)
            if self.piece_captured != '--':
                screen.blit(IMAGES[self.piece_captured], end_square)
            screen.blit(IMAGES[self.piece_moved], pygame.Rect(c * self.sq_size, r * self.sq_size, self.sq_size, self.sq_size))
            pygame.display.flip()
            clock.tick(ANIMATION_FPS)
