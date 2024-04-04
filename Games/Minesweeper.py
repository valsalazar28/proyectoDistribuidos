import pygame
import random

'''
To do 
1.Add interactions system
2.Add Score system
3.Set UI kit
'''

WIDTH, HEIGHT = 400, 400
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS
MINE_COUNT = 15
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.revealed = False
        self.is_mine = False
        self.neighbor_mine_count = 0

    def draw(self, screen):
        rect = pygame.Rect(self.col * CELL_SIZE, self.row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        if self.revealed:
            if self.is_mine:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, GRAY, rect)
                if self.neighbor_mine_count > 0:
                    font = pygame.font.Font(None, 20)
                    text = font.render(str(self.neighbor_mine_count), True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
        else:
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

def count_neighbor_mines(board, row, col):
    count = 0
    for i in range(max(0, row - 1), min(ROWS, row + 2)):
        for j in range(max(0, col - 1), min(COLS, col + 2)):
            if board[i][j].is_mine:
                count += 1
    return count

def generate_board():
    board = [[Cell(i, j) for j in range(COLS)] for i in range(ROWS)]
    mine_positions = random.sample([(i, j) for i in range(ROWS) for j in range(COLS)], MINE_COUNT)
    for position in mine_positions:
        row, col = position
        board[row][col].is_mine = True
        for i in range(max(0, row - 1), min(ROWS, row + 2)):
            for j in range(max(0, col - 1), min(COLS, col + 2)):
                board[i][j].neighbor_mine_count += 1
    return board

def reveal_neighbors(board, row, col):
    if row < 0 or row >= ROWS or col < 0 or col >= COLS or board[row][col].revealed:
        return
    board[row][col].revealed = True
    if board[row][col].neighbor_mine_count == 0:
        for i in range(max(0, row - 1), min(ROWS, row + 2)):
            for j in range(max(0, col - 1), min(COLS, col + 2)):
                reveal_neighbors(board, i, j)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Minesweeper')
    clock = pygame.time.Clock()
    board = generate_board()
    game_over = False

    while True:
        screen.fill(WHITE)

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if event.button == 1:  # Click izquierdo del ratón
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    row = mouse_y // CELL_SIZE
                    col = mouse_x // CELL_SIZE
                    cell = board[row][col]
                    if not cell.revealed:
                        cell.revealed = True
                        if cell.is_mine:
                            game_over = True
                        elif cell.neighbor_mine_count == 0:
                            reveal_neighbors(board, row, col)

        # Dibujar el tablero
        for row in board:
            for cell in row:
                cell.draw(screen)

        pygame.display.flip()
        clock.tick(30)

