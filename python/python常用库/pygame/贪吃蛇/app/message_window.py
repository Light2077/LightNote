import pygame

from constant import Constant


class Msg(pygame.surface.Surface):
    def __init__(self, *args, **kwargs):
        super(Msg, self).__init__(*args, **kwargs)

        self.best_score = 0
        self.score = 0

        self.font_small = pygame.font.SysFont('consolas', 24)
        self.zh_font = pygame.font.SysFont('SimHei', 22)
        self.init()

    def init(self):
        self.fill(Constant.BLACK)

        surf = pygame.surface.Surface((Constant.MSG_WIDTH - 2 * Constant.BOARD_EDGE,
                                       Constant.MSG_HEIGHT - 2 * Constant.BOARD_EDGE))
        surf.fill(Constant.WHITE)

        self.blit(surf, (Constant.BOARD_EDGE, Constant.BOARD_EDGE))

        score_text = self.font_small.render(f'score: {self.score}', True, Constant.BLACK)
        best_score_text = self.font_small.render(f' best: {self.best_score}', True, Constant.BLACK)
        speed_text = self.font_small.render(f'speed: {Constant.SPEED}', True, Constant.BLACK)

        add_speed_text = self.zh_font.render(f'加速: +', True, Constant.BLACK)
        sub_speed_text = self.zh_font.render(f'减速: -', True, Constant.BLACK)
        pause_text = self.zh_font.render(f'暂停: 空格', True, Constant.BLACK)

        self.blit(score_text, (Constant.BOARD_EDGE + 10, 10))
        self.blit(best_score_text, (Constant.BOARD_EDGE + 10, 36))
        self.blit(speed_text, (Constant.BOARD_EDGE + 10, 62))

        self.blit(add_speed_text, (Constant.BOARD_EDGE + 160, 10))
        self.blit(sub_speed_text, (Constant.BOARD_EDGE + 160, 36))
        self.blit(pause_text, (Constant.BOARD_EDGE + 160, 62))

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score
        if self.best_score < self._score:
            self.best_score = self._score

