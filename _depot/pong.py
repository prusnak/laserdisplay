#!/usr/bin/env python
# This example draws a dashed 2 color circle with increasing radius length
import LaserFactory
import math
import pygame
import random

LD = LaserFactory.createDisplay()

x=0x80
y=0x80
r=0x00
CIRCLE = [[0.0,0.5],[0.0,1.0],[0.5,1.0],[1.0,1.0],[1.0,0.5],[1.0,0.0],[0.5,0.0],[0.0,0.0],[0.0,0.5]]

def gen_circle(x, y, r):
  points = []
  for i in range(9):
    points.append([(int)(x + (CIRCLE[i][0]-0.5)*r*2), (int)(y + (CIRCLE[i][1]-0.5)*r*2-0.5)])
  return points

circle1 = gen_circle(0x80, 0x80, 0x10);
circle2 = gen_circle(0x80, 0x80, 0x18);
circle3 = gen_circle(0x80, 0x80, 0x20);

pygame.init()

size=width,height=320,200;screen=pygame.display.set_mode(size);
clock = pygame.time.Clock()

FPS = 30
PLAYER1_X = 20
PLAYER2_X = 230
BARRIER1 = 15
BARRIER2 = 235
BARRIER_TOP = 235
BARRIER_BOTTOM = 15
BALL_RADIUS = 5
BAT_ACC = 1
BAT_MAXSPEED = 5
BALL_SPEED = 6

player1 = 128
player2 = 128
dir1 = 0
dir2 = 0
ballx = 128
bally = 128
ball_dx = BALL_SPEED
ball_dy = 0
acc1 = 0
acc2 = 0

time = 0
shutdown = 0
score1 = 0
score2 = 0

DIR_TBL = [8, 5, 2, 0, -2, -5, -8]
bounce_idx = 3

def clamp_int(value, min, max):
  if value > max: return max
  if value < min: return min
  return value

def reset():
  global player1, player2, dir1, dir2, ballx, bally, ball_dx, ball_dy, acc1, acc2
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
  bounce_idx = int(random.random()*7)
  acc1 = 0
  acc2 = 0

while shutdown != 1:
  clock.tick(FPS)
  time += 1

  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_q:
        acc2 = BAT_ACC
      if event.key == pygame.K_a:
        acc2 = -BAT_ACC
      if event.key == pygame.K_o:
        acc1 = BAT_ACC
      if event.key == pygame.K_l:
        acc1 = -BAT_ACC
      if event.key == pygame.K_ESCAPE:
        shutdown = 1
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_q:
        acc2 -= BAT_ACC
        clamp_int(acc2, 0, BAT_ACC)
      if event.key == pygame.K_a:
        acc2 += BAT_ACC
        clamp_int(acc2, -BAT_ACC, 0)
      if event.key == pygame.K_o:
        acc1 -= BAT_ACC
        clamp_int(acc1, 0, BAT_ACC)
      if event.key == pygame.K_l:
        acc1 += BAT_ACC
        clamp_int(acc1, -BAT_ACC, 0)

  dir1 += acc1
  dir2 += acc2
  dir1 = clamp_int(dir1, -BAT_MAXSPEED, BAT_MAXSPEED)
  dir2 = clamp_int(dir2, -BAT_MAXSPEED, BAT_MAXSPEED)

  player1 += dir1
  player2 += dir2

  if player1 < 20:
    player1 = 20
  if player1 > 230:
    player1 = 230
  if player2 < 20:
    player2 = 20
  if player2 > 230:
    player2 = 230

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

  if (ballx < BARRIER1):
    reset()
  if (ballx > BARRIER2):
    reset()

  circle = gen_circle(ballx, bally, BALL_RADIUS)
  circle2 = gen_circle(ballx, bally, BALL_RADIUS-2)

  LD.set_color(LD.RED)
  LD.draw_quadratic_bezier(circle, 10)
  LD.set_color(LD.GREEN)
  LD.draw_quadratic_bezier(circle2, 6)
  LD.set_color([0xff,0x00,0x20])
  LD.draw_line(PLAYER1_X, player1-20, PLAYER1_X, player1+20)
  LD.set_color([0x20,0xff,0xff])
  LD.draw_line(PLAYER2_X, player2-20, PLAYER2_X, player2+20)

  LD.draw_text("%02i"%(score1), 20, 220, 20)
  LD.draw_text("%02i"%(score2), 235, 220, 20)
  LD.show_frame()
