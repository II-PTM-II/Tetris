# bibliothèques utilisées
import pygame
from copy import deepcopy
from random import choice, randrange

# réglages des parametres

# dimensions du plateau de jeu
W, H = 10, 20
TILE = 45
GAME_RES = W * TILE, H * TILE
# taille du fond
RES = 700,940
# réglage fps
FPS = 60

# lancement des modules inclus dans pygame
pygame.init()
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

# affichage des grilles sur le plateau
grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(W)] for j in range(H)]

anim_count, anim_speed, anim_limit = 0, 60, 2000

# image du fond
bg = pygame.image.load('img/fond.jpg').convert()
# image du plateau
game_bg = pygame.image.load('img/plateau.jpg').convert()

main_font = pygame.font.Font('font/font.ttf', 65)
font = pygame.font.Font('font/font.ttf', 45)

# mise en page du titre
title_tetris = main_font.render('TETRIS', True, pygame.Color('red'))
# mise en page du score
title_score = font.render('score:', True, pygame.Color('green'))
# mise en page du record
title_record = font.render('record:', True, pygame.Color('purple'))

# selection aléatoire des couleurs de pieces
get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))

# selection aléatoire des pieces
figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

# fonction qui permet de delimite les murs
def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True

# fonction qui permet charger le meilleur score
def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')

# fonction qui permet de sauvegarder le record
def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))

while True:
    record = get_record()
    dx, rotate = 0, False
    sc.blit(bg, (0, 0))
    sc.blit(game_sc, (20, 20))
    game_sc.blit(game_bg, (0, 0))

# delai d'attente lorqu'une ou plusieurs lignes sont remplies
    for i in range(lines):
        pygame.time.wait(200)

# controle des mouvements avec les touches fleches
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True

# deplacements abscisse et detection des bordures
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break
# deplacements ordonnée avec detection des bordures et affichage de la piece suivante
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_limit = 2000
                break
# rotation des pieces
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break

# verifications lignes
    line, lines = H - 1, 0
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            lines += 1

# ajout du nouveau score dans les sauvegardes du jeu
    score += scores[lines]

# apparition de la grille
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
# apparition de la piece
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc, color, figure_rect)
# inscrutation du fond
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)
# apparition de la piece suivante
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 380
        figure_rect.y = next_figure[i].y * TILE + 185
        pygame.draw.rect(sc, next_color, figure_rect)
# affichage du titre et du meilleur score
    sc.blit(title_tetris, (480, 40))
    sc.blit(title_score, (535, 580))
    sc.blit(font.render(str(score), True, pygame.Color('white')), (550, 640))
    sc.blit(title_record, (525, 400))
    sc.blit(font.render(record, True, pygame.Color('gold')), (550, 460))
# game over
    for i in range(W):
        if field[0][i]:
            set_record(record, score)
            field = [[0 for i in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(game_sc, get_color(), i_rect)
                sc.blit(game_sc, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(FPS)