#!/usr/bin/env python
import LaserDisplay
import math
import pygame
import random

LD = LaserDisplay.create()

clock = pygame.time.Clock()

FPS = 30
PLAYER1_X = 20
PLAYER2_X = 230
BARRIER1 = 15
BARRIER2 = 235
BARRIER_TOP = 235
BARRIER_BOTTOM = 15
BALL_RADIUS = 5
BAT_SPEED = 5
BALL_SPEED = 5

player1 = 128
player2 = 128
dir1 = 0
dir2 = 0
ballx = 128
bally = 128
ball_dx = BALL_SPEED
ball_dy = 0

shutdown = False
score1 = 0
score2 = 0

DIR_TBL = [8, 5, 2, 0, -2, -5, -8]
bounce_idx = 3

def clamp_int(value, min, max):
    if value > max: return max
    if value < min: return min
    return value

def reset():
    global player1, player2, dir1, dir2, ballx, bally, ball_dx, ball_dy, bounce_idx
    player1 = 128
    player2 = 128
    dir1 = 0
    dir2 = 0
    ballx = 128
    bally = 128
    if random.random() > 0.5:
        ball_dx = BALL_SPEED
    else:
        ball_dx = -BALL_SPEED
    ball_dy = 0
    bounce_idx = 3

while not shutdown:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                dir1 = -BAT_SPEED
            if event.key == pygame.K_a:
                dir1 = BAT_SPEED
            if event.key == pygame.K_o:
                dir2 = -BAT_SPEED
            if event.key == pygame.K_l:
                dir2 = BAT_SPEED
            if event.key == pygame.K_ESCAPE:
                shutdown = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_q:
                dir1 = 0
            if event.key == pygame.K_l or event.key == pygame.K_o:
                dir2 = 0

    player1 += dir1
    player2 += dir2

    player1 = clamp_int(player1, 20, 230)
    player2 = clamp_int(player2, 20, 230)

    ball_dy = DIR_TBL[bounce_idx]

    ballx += ball_dx
    bally += ball_dy

    region = -1

    if ballx < PLAYER1_X + BALL_RADIUS:
        diff = bally - player1
        if diff > 20 or diff < -20:
            reset()
            score2 += 1
        elif diff >= 15:
            region = 0
        elif diff >= 10:
            region = 1
        elif diff > -10:
            region = 2
        elif diff > -15:
            region = 3
        else:
            region = 4
    if ballx > PLAYER2_X - BALL_RADIUS:
        diff = bally - player2
        if diff > 20 or diff < -20:
            reset()
            score1 += 1
        elif diff >= 15:
            region = 0
        elif diff >= 10:
            region = 1
        elif diff > -10:
            region = 2
        elif diff > -15:
            region = 3
        else:
            region = 4

    if region != -1:
        bounce_idx = region + bounce_idx - 2
        if bounce_idx < 0: bounce_idx = 0
        if bounce_idx > 6: bounce_idx = 6
        ball_dx = -ball_dx

    if bally < BARRIER_BOTTOM or bally > BARRIER_TOP:
        bounce_idx = 6 - bounce_idx

    if ballx < BARRIER1 or ballx > BARRIER2:
        reset()

    LD.set_color(LD.YELLOW)
    LD.draw_ellipse(ballx, bally, 5, 5)

    LD.set_color(LD.MAGENTA)
    LD.draw_line(PLAYER1_X, player1-20, PLAYER1_X, player1+20)

    LD.set_color(LD.CYAN)
    LD.draw_line(PLAYER2_X, player2-20, PLAYER2_X, player2+20)

    LD.set_color(LD.WHITE)
    LD.draw_text("%02i"%(score1), 20, 220, 20)
    LD.draw_text("%02i"%(score2), 205, 220, 20)

    LD.show_frame()
