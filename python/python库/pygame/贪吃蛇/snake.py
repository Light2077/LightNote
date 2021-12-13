import pygame
from constant import Constant
from board import Board


class Body(pygame.sprite.Sprite):
    """ 蛇的身体类 """

    def __init__(self, color=Constant.LIGHTBLUE):
        super().__init__()

        self.surf = pygame.Surface((Constant.GRID_SIZE, Constant.GRID_SIZE))
        self.surf.fill('black')
        self.rect = self.surf.get_rect()
        # 给蛇的身体填充一个颜色
        self.color = color

    # 设置颜色
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        pygame.draw.rect(self.surf, self._color, (Constant.GRID_EDGE, Constant.GRID_EDGE,
                                                  Constant.GRID_SIZE - Constant.GRID_EDGE * 2,
                                                  Constant.GRID_SIZE - Constant.GRID_EDGE * 2))

    # 设置身体的位置
    def set_position(self, x, y):
        self.rect.left = x
        self.rect.top = y

    # 获得身体格子所在的左上角的坐标
    def get_position(self):
        left = self.rect.left
        top = self.rect.top
        return left, top


class Head(Body):
    """ 继承身体类，只有颜色是不一样的 """
    def __init__(self):
        super().__init__(color=Constant.PINK)


class Food(Body):
    def __init__(self):
        """ 继承身体类，颜色是不一样的
        增加了一个move方法，使食物被吃后可以移动到其他地方
        """
        super().__init__(color=Constant.YELLOW)

    def move(self, board, busy_grids):
        x, y = board.get_random_position(busy_grids)
        self.rect.left, self.rect.top = x, y


class Snake:
    # 蛇前进的方向（上下左右）
    DIRECTION = {
        'left': (-1 * Constant.GRID_SIZE, 0),
        'right': (1 * Constant.GRID_SIZE, 0),
        'up': (0, -1 * Constant.GRID_SIZE),
        'down': (0, 1 * Constant.GRID_SIZE),
    }

    def __init__(self, center):
        x, y = center
        self.bodies = [Head()]
        self.bodies[0].set_position(x, y)

        self.first = 0  # 蛇头所在位置
        self.length = 1  # 蛇的长度

        # 用于检测蛇头是否和身体碰撞了
        self.body_group = pygame.sprite.Group()

        self.direction = self.DIRECTION['left']  # 蛇头朝向
        self.direction_cache = self.direction  # 用于辅助转向，避免一些bug

        self.steps = 0  # 蛇移动的次数
        self.stomach = list()  # 蛇的肚子里正在被消化的食物，所在身体的索引

        self.eating = False  # 标记上一轮有没有吃到食物

    # 蛇头
    @property
    def head(self):
        return self.bodies[self.first]

    # 蛇尾
    @property
    def tail(self):
        """ 蛇尾 """
        return self.bodies[self.first - 1]

    # 蛇脖子（蛇头的下一个身体）
    @property
    def head_next(self):
        return self.bodies[(self.first + 1) % self.length]

    # 蛇头方格的left
    @property
    def x(self):
        return self.head.rect.left

    # 蛇头方格的top
    @property
    def y(self):
        return self.head.rect.top

    # 获得蛇头下一次要移动到的位置
    def get_next_position(self):
        """ 负责穿墙的逻辑 """
        dx, dy = self.direction = self.direction_cache
        x, y = self.x + dx, self.y + dy
        if y < Constant.BOARD_EDGE:
            y = Constant.BOARD_HEIGHT - Constant.GRID_SIZE - Constant.BOARD_EDGE
        if x < Constant.BOARD_EDGE:
            x = Constant.BOARD_WIDTH - Constant.GRID_SIZE - Constant.BOARD_EDGE
        if y >= Constant.BOARD_HEIGHT - Constant.BOARD_EDGE:
            y = Constant.BOARD_EDGE
        if x >= Constant.BOARD_WIDTH - Constant.BOARD_EDGE:
            x = Constant.BOARD_EDGE
        return x, y

    # 移动蛇
    def move(self):
        """
        实现移动的逻辑
        1. 把尾巴放到最前面
        2. 蛇头和蛇尾交换位置
        3. 消化食物
        4. 如果食物已经到了尾巴，成长一节
        :return:
        """

        def move_tail_to_first():
            x, y = self.get_next_position()
            self.tail.set_position(x, y)  # 尾巴移动到下一个位置
            self.tail.color = Constant.BODY_COLOR  # 重置尾巴的颜色

        def swap_head_tail():
            # 交换蛇头蛇尾元素
            self.bodies[self.first], self.bodies[self.first - 1] = self.bodies[self.first - 1], self.bodies[self.first]

            head_x, head_y = self.head.get_position()
            tail_x, tail_y = self.tail.get_position()
            self.head.set_position(tail_x, tail_y)
            self.tail.set_position(head_x, head_y)

            self.first = (self.first - 1) % self.length  # 更改蛇头指针

        def digesting():
            # 如果上一轮吃过食物，则蛇头后一节变色，表示消化中
            if self.eating:
                self.eating = False
                self.head_next.color = Constant.STOMACH_COLOR
            self.head.color = Constant.HEAD_COLOR

        grow_x, grow_y = self.tail.get_position()  # 如果蛇要成长，就会用到这个坐标
        move_tail_to_first()
        swap_head_tail()
        digesting()  # 食物进入胃
        self.grow(grow_x, grow_y)  # 成长

    # 通过按键转向
    def turn(self):
        """ 按键如果按得太快，就可以反向穿梭，所以要使用一个额外的变量来存储方向 """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.direction != self.DIRECTION['down']:
            self.direction_cache = self.DIRECTION['up']
        if keys[pygame.K_s] and self.direction != self.DIRECTION['up']:
            self.direction_cache = self.DIRECTION['down']
        if keys[pygame.K_a] and self.direction != self.DIRECTION['right']:
            self.direction_cache = self.DIRECTION['left']
        if keys[pygame.K_d] and self.direction != self.DIRECTION['left']:
            self.direction_cache = self.DIRECTION['right']

    # 吃食物
    def eat(self):
        self.stomach.append(self.first)
        self.eating = True

    # 蛇的成长
    def grow(self, x, y):
        if len(self.stomach) > 0 and self.stomach[0] == self.first:
            # 如果最先进来的食物又回到了头部
            body = Body()  # 创建一个新身体
            body.set_position(x, y)
            self.bodies.insert(self.first, body)  # 新身体插到原来的尾巴
            self.body_group.add(body)
            self.first = self.first + 1  # 绝对不会越界，可以放心+1
            self.length += 1  # 蛇的长度+1
            self.stomach.pop(0)  # 食物消化完了，从胃里移除

    # 绘制蛇
    def draw(self, surface):
        surface.blit(self.head.surf, self.head.rect)
        for body in self.bodies:
            surface.blit(body.surf, body.rect)

    # 获得蛇所占用的格子
    @property
    def busy_grids(self):
        grids = set()
        for body in self.bodies:
            grids.add(body.get_position())
        return grids

    # 调整速度
    def change_speed(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_KP_PLUS]:
            Constant.SPEED += 1
        if keys[pygame.K_KP_MINUS] and Constant.SPEED > 1:
            Constant.SPEED -= 1
        Constant.SPEED_TIME = 1000 // Constant.SPEED
