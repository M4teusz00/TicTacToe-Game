import sys, pygame
import pygame_menu
import numpy as np   #m.in do planszy/macierzy wyswietlanej w konsoli
import random as rand



# definiujemy stałe
HEIGHT = 700
WIDTH = 700
LINE_WIDTH = 4
B_ROWS = 3
B_COLS = 3
SQUARE_SIZE = HEIGHT // B_COLS
CIRCLE_RADIUS = SQUARE_SIZE//3
CIRCLE_WIDTH = 12
CROSS_WIDTH = 20
SPACE = SQUARE_SIZE//4

#kolory
BG_COLOR = (212, 217, 216)
LINE_COLOR = (155, 171, 168)
O_COLOR = (201, 20, 44)
X_COLOR = (78, 66, 245)

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Kółko i krzyżyk')


def start_the_game_2_players():
    window.fill(BG_COLOR)
    # plansza - wykonująca się w konsoli
    board = np.zeros((B_ROWS, B_COLS))
    print(board)

    def lines():
        # rysujemy linie:
        # 1 pozioma
        pygame.draw.line(window, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        # 2 pozioma
        pygame.draw.line(window, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
        # 1 pionowa
        pygame.draw.line(window, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        # 2 pionowa
        pygame.draw.line(window, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    lines()

    def shapes():
        for row in range(B_ROWS):
            for col in range(B_COLS):
                # rysujemy kółko (przypisane do gracza 1)
                if board[row][col] == 1:
                    pygame.draw.circle(window, O_COLOR, (
                        int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                       CIRCLE_RADIUS, CIRCLE_WIDTH)
                # rysujemy krzyżyk (przypisany do gracza 2)
                elif board[row][col] == 2:
                    pygame.draw.line(window, X_COLOR,
                                     (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                     (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                     CROSS_WIDTH)
                    pygame.draw.line(window, X_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                     (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                     CROSS_WIDTH)


    def select_field(row, col, player):
        board[row][col] = player
        print(board)

    def available_field(row, col):
        if board[row][col] == 0:
            return True
        else:
            return False


    def check_win(player):
        # w pionie
        for col in range(B_COLS):
            if board[0][col] == player and board[1][col] == player and board[2][col] == player:
                ver_winning_line(col, player)
                return True
        # w poziomie
        for row in range(B_ROWS):
            if board[row][0] == player and board[row][1] == player and board[row][2] == player:
                hor_winning_line(row, player)
                return True
        # po skosie (rosnąco)
        if board[2][0] == player and board[1][1] == player and board[0][2] == player:
            asc_diagonal_line(player)
            return True
        # po skosie (malejąco)
        if board[0][0] == player and board[1][1] == player and board[2][2] == player:
            desc_diagonal_line(player)
            return True
        return False

    # tworzymy linie "wygrywające":
    # pionowo
    def ver_winning_line(col, player):
        posX = col * SQUARE_SIZE + SQUARE_SIZE // 2

        if player == 1:
            color = O_COLOR
        elif player == 2:
            color = X_COLOR

        pygame.draw.line(window, color, (posX, 10), (posX, HEIGHT - 10), 10)

    # poziomo
    def hor_winning_line(row, player):
        posY = row * SQUARE_SIZE + SQUARE_SIZE // 2

        if player == 1:
            color = O_COLOR
        elif player == 2:
            color = X_COLOR

        pygame.draw.line(window, color, (10, posY), (WIDTH - 10, posY), 10)

    # po skosie (rosnąco)
    def asc_diagonal_line(player):
        if player == 1:
            color = O_COLOR
        elif player == 2:
            color = X_COLOR

        pygame.draw.line(window, color, (10, HEIGHT - 10), (WIDTH - 10, 10), 10)

    # po skosie (malejąco)
    def desc_diagonal_line(player):
        if player == 1:
            color = O_COLOR
        elif player == 2:
            color = X_COLOR

        pygame.draw.line(window, color, (10, 10), (WIDTH - 10, HEIGHT - 10), 10)

    def restart():
        window.fill(BG_COLOR)
        lines()
        for row in range(B_ROWS):
            for col in range(B_COLS):
                board[row][col] = 0



    #gracz kolko(1)/krzyzyk(2) zostaje wybierany losowo
    random_player = [1,2]
    player = rand.choice(random_player)

    end = False

    # pętla główna
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not end:

                mouseX = event.pos[0]  # wspolrzedne x
                mouseY = event.pos[1]  # wspolrzedne y

                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_col = int(mouseX // SQUARE_SIZE)

                if available_field(clicked_row, clicked_col):
                    select_field(clicked_row, clicked_col, player)
                    if check_win(player):
                        end = True
                    player = player % 2 + 1

                    shapes()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                    end = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


menu = pygame_menu.Menu('GRA KÓŁKO I KRZYŻYK', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_DEFAULT)
menu.add.text_input('Gracz 1: ', default='')
menu.add.text_input('Gracz 2: ', default='')
menu.add.button('Graj na 2 osoby', start_the_game_2_players)
menu.add.button('Wyjdź', pygame_menu.events.EXIT)

menu.mainloop(window)













