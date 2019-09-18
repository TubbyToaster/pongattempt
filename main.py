import random
import sys

import pygame
from pygame.locals import *
from pygame.math import Vector2

pygame.init()
mainClock = pygame.time.Clock()

WINDOWWIDTH = 600
WINDOWHEIGHT = 500
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),
                                        0, 32)
pygame.display.set_caption('PONG BABY YEAH!!!!!')

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
COLOR1 = (55, 155, 255)
foodCounter = 0
NEWFOOD = 40
FOODSIZE = 20
playing = True
winner = "none"
# player paddles
player = pygame.Rect(WINDOWWIDTH - 20, WINDOWHEIGHT / 2, 15, 50)
player2 = pygame.Rect(3 * (WINDOWWIDTH / 4), 10, 50, 15)
player3 = pygame.Rect(3 * (WINDOWWIDTH / 4), WINDOWHEIGHT - 20, 50, 15)

enemy = pygame.Rect(20, WINDOWHEIGHT / 2, 15, 50)
enemy2 = pygame.Rect(1 * (WINDOWWIDTH / 4), 10, 50, 15)
enemy3 = pygame.Rect(1 * (WINDOWWIDTH / 4), WINDOWHEIGHT - 20, 50, 15)

line = pygame.Rect(WINDOWWIDTH / 2, 0, 4, WINDOWHEIGHT)

dash_line = pygame.Rect(WINDOWWIDTH / 2, 0, 30, 30)

enemy_Score = 0
player_Score = 0
tot_enemy_Score = 0
tot_player_Score = 0

snd_pong = pygame.mixer.Sound('pong.wav')
snd_ping = pygame.mixer.Sound('ping.wav')
snd_win = pygame.mixer.Sound('youwin.wav')
snd_lose = pygame.mixer.Sound('youlose.wav')

game_mode = 0


def play_sound(snd):
    if snd == 1:
        snd_ping.play()
    if snd == 0:
        snd_pong.play()
    if snd == 3:
        snd_lose.play()
    if snd == 4:
        snd_win.play()


def vector2(xy_tuple, scale):
    vv = Vector2()
    vv[0], vv[1] = xy_tuple[0], xy_tuple[1]
    return vv * scale


screen = pygame.display.set_mode((200, 200))


class Box:
    def __init__(self, rect, bg_color, velocity, scale=1):
        self.bg_color_ = Color(bg_color)
        self.rect_ = pygame.Rect(rect)
        self.elip_ = pygame.draw.ellipse(windowSurface, BLACK, rect, 1)
        # self.rect_ = pygame.Rect(rect)
        self.velocity_ = vector2(velocity, scale)

    def __str__(self):
        return 'Box: clr={}, rect={}, velocity={}'.format(self.bg_color_, self.rect_, self.velocity_)

    def get_velocity(self):
        return self.velocity_

    def get_color(self):
        return self.bg_color_

    def get_rect(self):
        return self.rect_

    def get_elip(self):
        return self.elip_

    def move_box(self):
        self.rect_.left += self.velocity_[0]
        self.rect_.top += self.velocity_[1]


on1 = True
moveLeft = False
moveRight = False
moveUp = False
moveDown = False
MOVESPEED = 4
spd = 2

WW = 600
WH = 500
basicFont = pygame.font.SysFont(None, 48)
basicFont1 = pygame.font.SysFont(None, 36)

text = basicFont1.render(str(player_Score), True, WHITE, GREEN)
textRect = text.get_rect()
textRect.centerx = WINDOWWIDTH / 2 + 30  # windowSurface.get_rect().centerx
textRect.centery = 80  # windowSurface.get_rect().centery

text2 = basicFont1.render(str(enemy_Score), True, WHITE, GREEN)
textRect2 = text.get_rect()
textRect2.centerx = WINDOWWIDTH / 2 - 30  # windowSurface.get_rect().centerx
textRect2.centery = 80  # windowSurface.get_rect().centery

text3 = basicFont.render(str(tot_player_Score), True, WHITE, GREEN)
textRect3 = text.get_rect()
textRect3.centerx = WINDOWWIDTH / 2 + 50  # windowSurface.get_rect().centerx
textRect3.centery = 40  # windowSurface.get_rect().centery

text4 = basicFont.render(str(tot_enemy_Score), True, WHITE, GREEN)
textRect4 = text.get_rect()
textRect4.centerx = WINDOWWIDTH / 2 - 50  # windowSurface.get_rect().centerx
textRect4.centery = 40  # windowSurface.get_rect().centery

text5 = basicFont.render("Restart?", True, WHITE, BLACK)
textRect5 = text.get_rect()
textRect5.centerx = WINDOWWIDTH / 2 - 100  # windowSurface.get_rect().centerx
textRect5.centery = WINDOWHEIGHT / 2  # windowSurface.get_rect().centery

text6 = basicFont.render("winner", True, WHITE, BLACK)
textRect6 = text.get_rect()
textRect6.centerx = WINDOWWIDTH / 2 - 100  # windowSurface.get_rect().centerx
textRect6.centery = WINDOWHEIGHT / 2 + 100  # windowSurface.get_rect().centery

surf = pygame.display.set_mode((WW, WH), 0, 32)
b1 = Box(rect=(WINDOWWIDTH / 2, WINDOWHEIGHT / 2, 20, 20), bg_color="#FF0060", velocity=(3, 3), scale=spd)

boxes = [b1]
dash = [dash_line, dash_line, dash_line, dash_line, dash_line, dash_line, dash_line, dash_line, dash_line, dash_line,
        dash_line, dash_line]
# balls = [b2]

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            playing = True

        if event.type == K_0:
            if event.key == K_0:
                if game_mode == 1:
                    game_mode = 0
                elif game_mode == 0:
                    game_mode = 1

        if event.type == KEYDOWN:
            # Change the keyboard variables.
            if event.key == K_LEFT or event.key == K_a:
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == K_d:
                moveLeft = False
                moveRight = True
            if event.key == K_UP or event.key == K_w:
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == K_s:
                moveUp = False
                moveDown = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == K_a:
                moveLeft = False
            if event.key == K_RIGHT or event.key == K_d:
                moveRight = False
            if event.key == K_UP or event.key == K_w:
                moveUp = False
            if event.key == K_DOWN or event.key == K_s:
                moveDown = False
            if event.key == K_x:
                player.top = random.randint(0, WINDOWHEIGHT -
                                            player.height)
                player.left = random.randint(0, WINDOWWIDTH -
                                             player.width)

        if event.type == K_SPACE:
            if not on1:
                on1 = True
                player_Score += 1
            elif on1:
                on1 = False

    windowSurface.fill(COLOR1)
    # Move the player.
    if moveDown and player.bottom < WINDOWHEIGHT:
        player.top += MOVESPEED
    if moveUp and player.top > 0:
        player.top -= MOVESPEED
    if moveLeft and player.left > 0:
        player2.left -= MOVESPEED
        player3.left -= MOVESPEED
    if moveRight and player2.right < WINDOWWIDTH:
        player2.right += MOVESPEED
        player3.right += MOVESPEED

    if moveLeft and player2.left < WINDOWWIDTH / 2:
        player2.right += MOVESPEED
        player3.right += MOVESPEED

    if game_mode == 0:
        if b1.rect_.right < WINDOWWIDTH / 2 - 10:
            if enemy.top < b1.rect_.top:
                enemy.top += 4
            if enemy.top > b1.rect_.top:
                enemy.top -= 4

        if b1.rect_.right < WINDOWWIDTH / 2 - 10:

            if enemy2.right < b1.rect_.right:
                enemy2.right += 4
                enemy3.right += 4
            if enemy2.left > b1.rect_.left:
                enemy2.left -= 4
                enemy3.left -= 4

    if game_mode == 1:
        if b1.rect_.right < WINDOWWIDTH / 2 - 10:
            if enemy.top < b1.rect_.top:
                enemy.top += 3
            if enemy.top > b1.rect_.top:
                enemy.top -= 3

        if b1.rect_.right < WINDOWWIDTH / 2 - 10:

            if enemy2.right < b1.rect_.right:
                enemy2.right += 3
                enemy3.right += 3
            if enemy2.left > b1.rect_.left:
                enemy2.left -= 3
                enemy3.left -= 3

    if playing:
        pygame.draw.rect(windowSurface, BLACK, line)
        count = 0
        for d in dash:
            d.top = count
            count += WINDOWHEIGHT / 10
            pygame.draw.rect(windowSurface, COLOR1, dash_line)
        # Draw the player and enemy onto the surface.
        pygame.draw.rect(windowSurface, BLACK, player)
        pygame.draw.rect(windowSurface, BLACK, player2)
        pygame.draw.rect(windowSurface, BLACK, player3)
        pygame.draw.rect(windowSurface, BLACK, enemy)
        pygame.draw.rect(windowSurface, BLACK, enemy2)
        pygame.draw.rect(windowSurface, BLACK, enemy3)

        for b in boxes:
            r = b.get_rect()
            e = b.get_elip()
            v = b.get_velocity()
            clr = b.get_color()
            if on1:
                r.left += v[0]
                r.top += v[1]
            if not on1:
                r.left = WINDOWWIDTH / 2
                r.top = WINDOWHEIGHT / 2
            if player.colliderect(b.get_rect()):
                # v[1] *= -1
                if r.right - 1 > player.left + 1:
                    v[0] *= -1  # x
                r_sound = random.randint(0, 1)
                play_sound(r_sound)
            if player2.colliderect(b.get_rect()):
                v[1] *= -1
                # v[0] *= -1
                r_sound = random.randint(0, 1)
                play_sound(r_sound)
            if player3.colliderect(b.get_rect()):
                v[1] *= -1
                # v[0] *= -1
                r_sound = random.randint(0, 1)
                play_sound(r_sound)
            if enemy.colliderect(b.get_rect()):
                # v[1] *= -1
                v[0] *= -1
                r_sound = random.randint(0, 1)
                play_sound(r_sound)
            if enemy2.colliderect(b.get_rect()):
                v[1] *= -1
                # v[0] *= -1
                r_sound = random.randint(0, 1)
                play_sound(r_sound)
            if enemy3.colliderect(b.get_rect()):
                v[1] *= -1
                # v[0] *= -1
                r_sound = random.randint(0, 1)
                play_sound(r_sound)

            if r.left > WINDOWWIDTH / 2 + 10:
                if r.left > WINDOWWIDTH or r.bottom < 0 or r.top > WINDOWHEIGHT:
                    v[1] = random.randint(-4, 4)
                    v[0] = random.randint(-4, 4)
                    if v[1] == 0 or v[0] == 0 or v[1] == 1 or v[0] == 1 or v[1] == -1 or v[0] == -1:
                        v[1] = 3
                        v[0] = -3
                    r.top = WINDOWWIDTH / 2
                    r.bottom = WINDOWHEIGHT / 2
                    r.right = WINDOWWIDTH / 2
                    r.left = WINDOWHEIGHT / 2
                    enemy_Score += 1
                    # tot_player_Score += 1
            if r.right < WINDOWWIDTH / 2 - 10:
                if r.right < 0 or r.bottom < 0 or r.top > WINDOWHEIGHT:
                    v[1] = random.randint(-4, 4)
                    v[0] = random.randint(-4, 4)
                    if v[1] == 0 or v[0] == 0 or v[1] == 1 or v[0] == 1 or v[1] == -1 or v[0] == -1:
                        v[1] = 3
                        v[0] = -3
                    r.top = WINDOWWIDTH / 2
                    r.bottom = WINDOWHEIGHT / 2
                    r.right = WINDOWWIDTH / 2
                    r.left = WINDOWHEIGHT / 2
                    player_Score += 1
                    # tot_player_Score += 1

            pygame.draw.ellipse(surf, clr, r, 0)

        if player_Score + 3 > enemy_Score and player_Score > 10:
            tot_player_Score += 1
            enemy_Score = 0
            player_Score = 0

        if enemy_Score + 3 > player_Score and enemy_Score > 10:
            tot_enemy_Score += 1
            enemy_Score = 0
            player_Score = 0

        if tot_enemy_Score + 1 > tot_player_Score and tot_enemy_Score > 2:
            tot_enemy_Score = 0
            tot_player_Score = 0
            enemy_Score = 0
            player_Score = 0
            play_sound(3)
            playing = False
            winner = "You won against the machine"

        if tot_player_Score + 1 > tot_enemy_Score and tot_player_Score > 2:
            tot_enemy_Score = 0
            tot_player_Score = 0
            enemy_Score = 0
            player_Score = 0
            play_sound(4)
            playing = False
            winner = "AI won, you are inferior"

        text = basicFont1.render(str(player_Score), True, WHITE, GREEN)
        text2 = basicFont1.render(str(enemy_Score), True, WHITE, GREEN)
        text3 = basicFont.render(str(tot_enemy_Score), True, WHITE, GREEN)
        text4 = basicFont.render(str(tot_player_Score), True, WHITE, GREEN)
        windowSurface.blit(text, textRect)
        windowSurface.blit(text2, textRect2)
        windowSurface.blit(text3, textRect3)
        windowSurface.blit(text4, textRect4)
    elif not playing:
        text5 = basicFont.render("play again (press down)?", True, WHITE, BLACK)
        windowSurface.blit(text5, textRect5)
        text6 = basicFont.render(winner, True, WHITE, BLACK)
        windowSurface.blit(text6, textRect6)

    # Draw the window onto the screen.
    pygame.display.update()
    mainClock.tick(60)
