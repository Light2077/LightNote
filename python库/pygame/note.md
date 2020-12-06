[pygame官方文档](https://www.pygame.org/docs/)

# 初见pygame

以下每个案例都是相互关联的，比如案例2基于案例1，案例3又基于案例2

## 1. 第一个窗口

创建一个窗口，大小是300x300的，默认背景是黑色的。

```python
import pygame
import sys

pygame.init()
# 设置窗体显示大小
screen = pygame.display.set_mode((300, 300))

while True:
    # 刷新屏幕
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # 如果系统在pygame.quit()前终止，IDLE会挂起。所以一般会在最后调用sys.exit()
            sys.exit()  


```

## 2. 设置背景颜色

定义一些颜色，把背景颜色设置为白色

颜色有好几种定义方式，按照自己喜欢的来就ok

有关于颜色，可以查看：

https://www.pygame.org/docs/ref/color.html

```python
# 定义颜色变量
WHITE = pygame.color.Color(255, 255, 255)
BLACK = pygame.color.Color(0, 0, 0, a = 255)
RED = "#FF0000"
GREEN = "0x00ff00"
BLUE = (0, 0, 255)
```

设置标题

```python
pygame.display.set_caption("我的游戏")
```

设置背景颜色为白色

```python
screen = pygame.display.set_mode((300, 300))
screen.fill(WHITE)	
```

综合来就是

```python
import pygame
import sys

# 定义颜色变量
WHITE = pygame.color.Color(255, 255, 255)
BLACK = pygame.color.Color(0, 0, 0, a = 255)
RED = "#FF0000"
GREEN = "0x00ff00"
BLUE = (0, 0, 255)

pygame.init()
# 设置窗体显示大小
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption("我的游戏")
# 设置背景颜色
screen.fill(WHITE)

while True:
    # 刷新屏幕
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # 如果系统在pygame.quit()前终止，IDLE会挂起。所以一般会在最后调用sys.exit()
            sys.exit()
```

## 3. 画几个图形

https://www.pygame.org/docs/ref/draw.html

while循环内，多了几句绘制图形的语句。

```python
import pygame
import sys

# 定义颜色变量
WHITE = pygame.color.Color(255, 255, 255)
BLACK = pygame.color.Color(0, 0, 0, a = 255)
RED = "#FF0000"
GREEN = "0x00ff00"
BLUE = (0, 0, 255)

pygame.init()
# 设置窗体显示大小
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption("我的游戏")
# 设置背景颜色
screen.fill(WHITE)

while True:
    pygame.draw.circle(screen, BLACK, (100, 50), 30)
    pygame.draw.circle(screen, BLACK, (200, 50), 30)
    pygame.draw.line(screen, BLUE, (150, 130), (130, 170))
    pygame.draw.line(screen, BLUE, (150, 130), (170, 170))
    pygame.draw.line(screen, 'green', (130, 170), (170, 170))
    pygame.draw.rect(screen, 'red', (100, 200, 100, 50))
    # 刷新屏幕
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # 如果系统在pygame.quit()前终止，IDLE会挂起。所以一般会在最后调用sys.exit()
            sys.exit()


```

## 4. 加载素材

实际上，我们不会自己用pygame绘图，通常是加载已有的素材。
Surface对象，也称为“表面对象”。本质上是在内存中分配一块存放指定尺寸的内存空间，来存放用于显示的图像。可以理解为一个“图层”，即将显示的图片会先放在上面。
Rect对象，就是一个矩形方框。方便我们对于屏幕上的画面进行局部绘制、移动、碰撞检测。  

```python
# 把图片加载到内存，返回一个surface对象
player = pygame.image.load('Player.png')
# 通过surface对象尺寸，获取对应图像的外切矩形对象
player_rect = player.get_rect()
```

![image-20201206171349365](image-20201206171349365.png)

矩形对象用于移动和对齐的虚拟属性

```
x,y
top, left, bottom, right
topleft, bottomleft, topright, bottomright
midtop, midleft, midbottom, midright
center, centerx, centery
size, width, height
w,h
```

可以这么设置属性

```
rect1.right = 10
rect2.center = (20, 30)
```

加载背景图片和小车

`bilt`是局部刷新，可以节省一定的计算资源。

```python
import pygame
import sys

pygame.init()
# 设置窗体显示大小
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("我的游戏")
# 加载背景
background = pygame.image.load("AnimatedStreet.png")
player = pygame.image.load("Player.png")
x, y = 178, 504

while True:
    # 绘制背景图片和小车
    screen.blit(background, (0, 0))
    screen.blit(player, (x, y))
    # 刷新屏幕
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # 如果系统在pygame.quit()前终止，IDLE会挂起。所以一般会在最后调用sys.exit()
            sys.exit()


```

## 5. 素材的移动

需要设定FPS，每秒刷新的频率

```python
FPS = 30  # 1秒30绘制张图片

clock = pygame.time.Clock()
# 放到主循环
# clock.tick(FPS)
```



```python
import pygame
import sys

pygame.init()
# 设置窗体显示大小
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("我的游戏")
# 加载背景
background = pygame.image.load("AnimatedStreet.png")
player = pygame.image.load("Player.png")
x, y = 178, 504
FPS = 30  # 1秒30张图片

clock = pygame.time.Clock()
while True:
    # 绘制背景图片和小车
    y -= 1
    screen.blit(background, (0, 0))
    screen.blit(player, (x, y))
    # 刷新屏幕
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # 如果系统在pygame.quit()前终止，IDLE会挂起。所以一般会在最后调用sys.exit()
            sys.exit()

    clock.tick(FPS)
```

## 6. 对象封装

实际上，用面向对象的方式封装游戏里的对象会让你的代码变得更加清晰。所以这一步主要是把小车player对象封装成一个类，便于管理。

```python
import pygame
import sys


class Player:
    def __init__(self):
        x, y = (width / 2, height / 2)
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect(center=(x, y))  # 默认是top和left

    def move(self):
        # self.rect.y -= 1
        # self.rect = self.rect.move(0,-1)
        self.rect.move_ip(0, -5)
        
        
# 初始化player对象
player = Player()
pygame.init()
# 设置窗体显示大小
width, height = 400, 600
screen = pygame.display.set_mode((width, height))

# 加载背景
background = pygame.image.load("AnimatedStreet.png")

FPS = 30  # 1秒30张图片
clock = pygame.time.Clock()
while True:
    # 绘制背景图片和小车
    screen.blit(background, (0, 0))
    screen.blit(player.image, player.rect)
    player.move()
    # 刷新屏幕
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # 如果系统在pygame.quit()前终止，IDLE会挂起。所以一般会在最后调用sys.exit()
            sys.exit()

    clock.tick(FPS)
```

# 事件处理机制

