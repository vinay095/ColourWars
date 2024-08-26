import pygame
import numpy as np
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 5
CELL_SIZE = 100
SCREEN_SIZE = GRID_SIZE * CELL_SIZE
BACKGROUND_COLOR = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
COLORS = {0: BACKGROUND_COLOR, 1: RED, 2: BLUE}

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Color War")

class ColorWar:
    def __init__(self, mode='human', difficulty='easy'):
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)  # Create a 5x5 grid initialized to 0
        self.current_player = 1  # Player 1 starts
        self.mode = mode  # 'human' for two human players, 'computer' for one human vs. AI
        self.ai_player = 2 if mode == 'computer' else None
        self.difficulty = difficulty

    def draw_grid(self):
        screen.fill(BACKGROUND_COLOR)
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                color = COLORS[self.grid[x, y]]
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, (0, 0, 0), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
        pygame.display.flip()

    def handle_click(self, pos):
        x, y = pos
        x //= CELL_SIZE
        y //= CELL_SIZE
        if self.grid[x, y] == 0:
            self.grid[x, y] = 3  # Starting color value
        else:
            if self.grid[x, y] == self.current_player or self.grid[x, y] == 3:
                self.increase_value(x, y)

    def increase_value(self, x, y):
        if self.grid[x, y] == 0:
            return
        self.grid[x, y] += 1
        if self.grid[x, y] == 4:
            self.split(x, y)
        self.check_win()

    def split(self, x, y):
        value = self.grid[x, y]
        self.grid[x, y] = 0
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if self.grid[nx, ny] == 0 or self.grid[nx, ny] == 3:
                    self.grid[nx, ny] = self.current_player
                else:
                    self.grid[nx, ny] += 1
                if self.grid[nx, ny] == 4:
                    self.split(nx, ny)
        self.capture_opponent_cells(x, y)

    def capture_opponent_cells(self, x, y):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if self.grid[nx, ny] > 0 and self.grid[nx, ny] != self.current_player:
                    self.grid[nx, ny] = self.current_player

    def check_win(self):
        player1_count = np.count_nonzero(self.grid == 1)
        player2_count = np.count_nonzero(self.grid == 2)

        # Check if one player has completely dominated
        if player1_count > 0 and player2_count == 0:
            pygame.time.delay(1000)
            print("Player 1 Wins!")
            pygame.quit()
            sys.exit()
        elif player2_count > 0 and player1_count == 0:
            pygame.time.delay(1000)
            print("Player 2 Wins!")
            pygame.quit()
            sys.exit()

    def ai_move(self):
        empty_cells = np.argwhere(self.grid == 0)
        if len(empty_cells) == 0:
            return
        x, y = empty_cells[random.randint(0, len(empty_cells) - 1)]
        if self.grid[x, y] == 0:
            self.grid[x, y] = 3
        else:
            if self.grid[x, y] == self.current_player or self.grid[x, y] == 3:
                self.increase_value(x, y)

    def play(self):
        self.draw_grid()
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.mode == 'human' and self.current_player == 1:
                        self.handle_click(pygame.mouse.get_pos())
                        self.draw_grid()
                        self.check_win()
                        self.current_player = 2
                    elif self.mode == 'computer' and self.current_player == 1:
                        self.handle_click(pygame.mouse.get_pos())
                        self.draw_grid()
                        self.check_win()
                        self.current_player = 2
                if self.mode == 'computer' and self.current_player == 2:
                    self.ai_move()
                    self.draw_grid()
                    self.check_win()
                    self.current_player = 1
                if self.mode == 'human' and self.current_player == 2:
                    self.handle_click(pygame.mouse.get_pos())
                    self.draw_grid()
                    self.check_win()
                    self.current_player = 1
            clock.tick(60)

def main_menu():
    font = pygame.font.Font(None, 74)
    text = font.render('Color War', True, (0, 0, 0))
    screen.fill(BACKGROUND_COLOR)
    screen.blit(text, (SCREEN_SIZE // 2 - text.get_width() // 2, SCREEN_SIZE // 4))

    font = pygame.font.Font(None, 36)
    text1 = font.render('Play vs Friend', True, (0, 0, 0))
    text2 = font.render('Play vs Computer', True, (0, 0, 0))

    button1 = pygame.Rect(SCREEN_SIZE // 2 - text1.get_width() // 2, SCREEN_SIZE // 2, text1.get_width(), text1.get_height())
    button2 = pygame.Rect(SCREEN_SIZE // 2 - text2.get_width() // 2, SCREEN_SIZE // 2 + 50, text2.get_width(), text2.get_height())

    screen.blit(text1, (button1.x, button1.y))
    screen.blit(text2, (button2.x, button2.y))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button1.collidepoint(event.pos):
                    return 'human'
                elif button2.collidepoint(event.pos):
                    return 'computer'

def difficulty_menu():
    font = pygame.font.Font(None, 74)
    text = font.render('Select Difficulty', True, (0, 0, 0))
    screen.fill(BACKGROUND_COLOR)
    screen.blit(text, (SCREEN_SIZE // 2 - text.get_width() // 2, SCREEN_SIZE // 4))

    font = pygame.font.Font(None, 36)
    text1 = font.render('Easy', True, (0, 0, 0))
    text2 = font.render('Medium', True, (0, 0, 0))
    text3 = font.render('Hard', True, (0, 0, 0))

    button1 = pygame.Rect(SCREEN_SIZE // 2 - text1.get_width() // 2, SCREEN_SIZE // 2, text1.get_width(), text1.get_height())
    button2 = pygame.Rect(SCREEN_SIZE // 2 - text2.get_width() // 2, SCREEN_SIZE // 2 + 50, text2.get_width(), text2.get_height())
    button3 = pygame.Rect(SCREEN_SIZE // 2 - text3.get_width() // 2, SCREEN_SIZE // 2 + 100, text3.get_width(), text3.get_height())

    screen.blit(text1, (button1.x, button1.y))
    screen.blit(text2, (button2.x, button2.y))
    screen.blit(text3, (button3.x, button3.y))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button1.collidepoint(event.pos):
                    return 'easy'
                elif button2.collidepoint(event.pos):
                    return 'medium'
                elif button3.collidepoint(event.pos):
                    return 'hard'

if __name__ == '__main__':
    mode = main_menu()
    if mode == 'computer':
        difficulty = difficulty_menu()
        game = ColorWar(mode=mode, difficulty=difficulty)
    else:
        game = ColorWar(mode=mode)
    game.play()
