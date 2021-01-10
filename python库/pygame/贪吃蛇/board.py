import pygame
import random
from constant import Constant


class Board(pygame.surface.Surface):
    # 棋盘类，用于定位蛇的身体和食物的左上角位置，使蛇是一格一格移动的
    GRIDS = [(i, j) for i in range(Constant.BOARD_EDGE, Constant.BOARD_WIDTH-Constant.BOARD_EDGE, Constant.GRID_SIZE)
             for j in range(Constant.BOARD_EDGE, Constant.BOARD_HEIGHT-Constant.BOARD_EDGE, Constant.GRID_SIZE)]

    CENTER_X = Constant.WIDTH // 2 * Constant.GRID_SIZE + Constant.BOARD_EDGE
    CENTER_Y = Constant.HEIGHT // 2 * Constant.GRID_SIZE + Constant.BOARD_EDGE
    CENTER = CENTER_X, CENTER_Y

    def __init__(self, *args, **kwargs):
        super(Board, self).__init__(*args, **kwargs)
        self.init()

    def init(self):
        self.fill(Constant.BLACK)
        surf = pygame.surface.Surface((Constant.BOARD_WIDTH - 2 * Constant.BOARD_EDGE,
                                            Constant.BOARD_HEIGHT - 2 * Constant.BOARD_EDGE))
        surf.fill(Constant.WHITE)

        self.blit(surf, (Constant.BOARD_EDGE, Constant.BOARD_EDGE))

    def get_random_position(self, busy_grids):
        """
        随机返回一个未被占用的格子
        :param busy_grids: 已经被占用的格子
        :return:
        """
        # 找出空闲的格子
        space_grids = [grid for grid in self.GRIDS if grid not in busy_grids]
        if len(space_grids) > 0:
            return random.choice(space_grids)
        return None

    @property
    def center(self):
        """ 游戏初始化时蛇待的格子 """
        return self.CENTER
