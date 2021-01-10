import pygame

class Constant:
    # 定义颜色
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BODY_COLOR = LIGHTBLUE = 'lightblue'  # 蛇身颜色
    HEAD_COLOR = PINK = 'pink'
    FOOD_COLOR = YELLOW = 'yellow'
    STOMACH_COLOR = LIGHTGREEN = 'lightgreen'

    CAPTION = '贪吃蛇'  # 窗口标题

    GRID_EDGE = 2
    GRID_SIZE = 20
    WIDTH = 15  # 宽多少个格子
    HEIGHT = 15  # 高多少个格子

    BOARD_EDGE = 10
    BOARD_WIDTH = WIDTH * GRID_SIZE + BOARD_EDGE * 2
    BOARD_HEIGHT = HEIGHT * GRID_SIZE + BOARD_EDGE * 2

    MSG_WIDTH = BOARD_WIDTH
    MSG_HEIGHT = 100

    SCREEN_WIDTH = BOARD_WIDTH
    SCREEN_HEIGHT = BOARD_HEIGHT + MSG_HEIGHT - BOARD_EDGE

    SNAKE_MOVE = pygame.USEREVENT + 1  # 蛇移动事件
    SPEED = 5  # 一秒移动5次
    SPEED_TIME = 1000 // SPEED  # 控制蛇多少时间移动一次，单位毫秒

    FPS = 60
