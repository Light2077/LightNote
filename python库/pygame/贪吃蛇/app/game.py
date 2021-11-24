import pygame
import sys
from constant import Constant
from message_window import Msg
from snake import Snake, Food
from board import Board


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(Constant.CAPTION)
        self.screen = pygame.display.set_mode((Constant.SCREEN_WIDTH, Constant.SCREEN_HEIGHT))
        self.board = Board((Constant.BOARD_WIDTH, Constant.BOARD_HEIGHT))
        self.msg = Msg((Constant.MSG_WIDTH, Constant.MSG_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.time.set_timer(Constant.SNAKE_MOVE, Constant.SPEED_TIME, 1)
        self.pause = False  # 是否处于暂停状态

    def run(self):
        snake = Snake(self.board.center)
        food = Food()
        food.move(self.board, snake.busy_grids)
        foods = pygame.sprite.Group()
        foods.add(food)

        while True:
            # 刷新屏幕
            self.board.init()
            self.msg.init()
            self.screen.fill(Constant.WHITE)
            self.screen.blit(self.msg, (0, Constant.BOARD_HEIGHT - Constant.BOARD_EDGE))

            snake.turn()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # 如果系统在pygame.quit()前终止，IDLE会挂起。所以一般会在最后调用sys.exit()
                    sys.exit()
                if event.type == Constant.SNAKE_MOVE:
                    snake.move()
                    if not self.pause:
                        pygame.time.set_timer(Constant.SNAKE_MOVE, Constant.SPEED_TIME, 1)

                if event.type == pygame.KEYDOWN:
                    snake.change_speed()
                    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        pygame.quit()
                        # 如果系统在pygame.quit()前终止，IDLE会挂起。所以一般会在最后调用sys.exit()
                        sys.exit()
                    if pygame.key.get_pressed()[pygame.K_SPACE]:
                        self.pause = not self.pause
                        if not self.pause:
                            pygame.time.set_timer(Constant.SNAKE_MOVE, Constant.SPEED_TIME, 1)


            if food not in foods:
                food.move(self.board, snake.busy_grids)
                foods.add(food)

            # 如果蛇头吃到了食物
            if pygame.sprite.spritecollide(snake.head, foods, True):
                snake.eat()  # 食物进入蛇口
                self.msg.score += 1

            # 如果
            if pygame.sprite.spritecollide(snake.head, snake.body_group, False):
                snake = Snake(self.board.center)
                self.msg.score = 0

            self.board.blit(food.surf, food.rect)
            snake.draw(self.board)
            self.screen.blit(self.board, (0, 0))

            self.clock.tick(Constant.FPS)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
