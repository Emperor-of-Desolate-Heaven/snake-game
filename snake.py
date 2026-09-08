# -*- coding: utf-8 -*-
"""贪吃蛇 —— 使用 Python 标准库 turtle，无需安装任何依赖。

操作：方向键 / WASD 控制移动，空格暂停，Esc 打开暂停菜单（↑↓ 或鼠标选择，Enter 确认）；
撞墙或撞到自己身体后弹出失败菜单，可选择重新开始或退出。
"""
import turtle
import random

# 游戏设置
GRID = 20          # 每个格子的大小（像素）
WIDTH, HEIGHT = 30, 22   # 场地格子数
SPEED = 0.2        # 每步间隔（秒），越小越快

# 窗口与画笔
screen = turtle.Screen()
screen.title("贪吃蛇")
screen.setup(WIDTH * GRID + 40, HEIGHT * GRID + 40)
screen.tracer(0)   # 关闭自动刷新，手动控制帧
screen.bgcolor("#2b2b2b")

pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.speed(0)

# 游戏状态
snake = [(WIDTH // 2, HEIGHT // 2)]   # 蛇身坐标列表，头在前
direction = (1, 0)                    # 当前移动方向
food = None
score = 0
paused = False
menu_open = False     # 暂停菜单是否打开
selected = 0          # 菜单当前选中项（0/1/2）
running = True


def fill_rect(x, y, w, h, color):
    """以 (x, y) 为左上角画一个实心矩形。"""
    pen.goto(x, y)
    pen.color(color)
    pen.begin_fill()
    for side in (w, h, w, h):
        pen.forward(side)
        pen.left(90)
    pen.end_fill()


def draw_rect(gx, gy, color):
    """在格子坐标 (gx, gy) 画一个方格。"""
    fill_rect(gx * GRID - WIDTH * GRID // 2,
              gy * GRID - HEIGHT * GRID // 2,
              GRID, GRID, color)


def spawn_food():
    """在空白处随机生成食物。"""
    global food
    while True:
        pos = (random.randrange(WIDTH), random.randrange(HEIGHT))
        if pos not in snake:
            food = pos
            return


def set_direction(new_dir):
    """改变方向（禁止直接掉头）。"""
    global direction
    if (new_dir[0] != -direction[0]) or (new_dir[1] != -direction[1]):
        direction = new_dir


def handle_space():
    """游戏中空格=暂停/继续；菜单中空格=确认选中项（失败后即重开）。"""
    global paused
    if menu_open:
        confirm_menu(selected)
        return
    if running:
        paused = not paused
        if paused:
            # 在画面左下角提示已暂停
            pen.goto(-WIDTH * GRID // 2 + 10, -HEIGHT * GRID // 2 + 10)
            pen.color("white")
            pen.write("已暂停（空格继续，Esc 菜单）", font=("Microsoft YaHei", 12, "normal"))
            screen.update()
    else:
        reset()


def step():
    """前进一步：移动蛇、判定吃食物 / 撞墙 / 撞自己。"""
    global food, score
    head = snake[0]
    new_head = (head[0] + direction[0], head[1] + direction[1])

    # 撞墙判定：直接游戏失败
    if not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
        game_over()
        return
    # 撞自己判定
    if new_head in snake:
        game_over()
        return

    snake.insert(0, new_head)

    if new_head == food:
        score += 10
        spawn_food()          # 吃到食物，不删尾巴 → 蛇变长
    else:
        snake.pop()           # 没吃到，删尾巴 → 长度不变


def draw():
    """重绘整个画面。"""
    pen.clear()
    for i, seg in enumerate(snake):
        # 头部亮绿，身体渐暗
        color = "#8be04e" if i == 0 else "#4c9e38"
        draw_rect(seg[0], seg[1], color)
    if food:
        draw_rect(food[0], food[1], "#e0524e")
    pen.goto(-WIDTH * GRID // 2 + 10, HEIGHT * GRID // 2 - 5)
    pen.color("white")
    pen.write(f"分数: {score}   空格=暂停", font=("Microsoft YaHei", 14, "normal"))
    screen.update()


def game_over():
    """撞到自己身体：结束游戏，弹出失败菜单（你失败 + 得分 + 选项）。"""
    global running, paused, menu_open, selected
    running = False
    paused = True
    menu_open = True
    selected = 0
    draw_menu()


def reset():
    """重新开始一局。"""
    global snake, direction, food, score, paused, menu_open, selected, running
    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = (1, 0)
    score = 0
    paused = False
    menu_open = False
    selected = 0
    running = True
    spawn_food()
    draw()


MENU_ITEMS = ("继续游戏", "重新开始", "退出游戏")
MENU_ITEM_Y = (50, 12, -26)          # 暂停菜单三个选项的 y 坐标
GAMEOVER_ITEMS = ("重新开始", "退出游戏")
GAMEOVER_ITEM_Y = (12, -26)          # 失败菜单两个选项的 y 坐标


def active_menu():
    """当前菜单的内容：(标题, 副标题, 选项列表, 选项 y 坐标)。"""
    if running:
        return "暂停", None, MENU_ITEMS, MENU_ITEM_Y
    return "你失败", "得分：%d" % score, GAMEOVER_ITEMS, GAMEOVER_ITEM_Y


def draw_menu():
    """在画面中央显示菜单（暂停 / 失败），高亮当前选中项。"""
    draw()   # 先清屏重绘游戏画面，防止菜单元素重复叠加
    panel_w, panel_h, top = 240, 220, 140
    fill_rect(-panel_w // 2, top, panel_w, panel_h, "#1e1e1e")
    title, subtitle, items, ys = active_menu()
    # 高亮条
    hy = ys[selected]
    fill_rect(-100, hy + 19, 200, 38, "#3a3f4b")
    pen.color("#e0524e" if not running else "white")
    pen.goto(0, 95)
    pen.write(title, align="center", font=("Microsoft YaHei", 22, "bold"))
    if subtitle:
        pen.color("#ffd94e")
        pen.goto(0, 58)
        pen.write(subtitle, align="center", font=("Microsoft YaHei", 16, "normal"))
    for i, y in enumerate(ys):
        pen.goto(0, y)
        pen.color("#ffd94e" if i == selected else "white")
        pen.write(("▶ " if i == selected else "  ") + items[i],
                  align="center", font=("Microsoft YaHei", 15, "normal"))
    pen.goto(0, -66)
    pen.color("#9e9e9e")
    hint = "↑↓ 选择   Enter 确认   Esc 关闭" if running else "↑↓ 选择   Enter 确认   Esc 退出"
    pen.write(hint, align="center", font=("Microsoft YaHei", 11, "normal"))
    screen.update()


def close_menu():
    """关闭菜单并继续游戏。"""
    global paused, menu_open
    menu_open = False
    paused = False
    draw()


def confirm_menu(i):
    """执行菜单第 i 项（仅菜单打开时有效）。"""
    if not menu_open:
        return
    if running:      # 暂停菜单：0 继续，1 重开，2 退出
        if i == 0:
            close_menu()
        elif i == 1:
            reset()
        else:
            screen.bye()
    else:            # 失败菜单：0 重新开始，1 退出游戏
        if i == 0:
            reset()
        else:
            screen.bye()


def toggle_menu():
    """Esc：游戏中打开/关闭暂停菜单；游戏结束后直接退出。"""
    global paused, menu_open, selected
    if not running:
        screen.bye()
        return
    if menu_open:
        close_menu()
    else:
        menu_open = True
        paused = True
        selected = 0
        draw_menu()


def handle_arrow(new_dir):
    """方向键/WASD：菜单中上下移动选择，游戏中改变移动方向。"""
    global selected
    if menu_open:
        n = len(active_menu()[2])
        if new_dir == (0, 1):        # 上
            selected = (selected - 1) % n
            draw_menu()
        elif new_dir == (0, -1):     # 下
            selected = (selected + 1) % n
            draw_menu()
        # 左/右在菜单中忽略
    else:
        set_direction(new_dir)


def on_menu_click(x, y):
    """鼠标点击：点中菜单项直接执行；游戏中点面板外=关闭菜单，失败后必须二选一。"""
    if not menu_open:
        return
    # 面板范围：x∈[-120,120]，y∈[-80,140]
    if not (-120 <= x <= 120 and -80 <= y <= 140):
        if running:
            close_menu()
        else:
            draw_menu()   # 失败菜单点外面不关闭，重新显示
        return
    for i, cy in enumerate(active_menu()[3]):
        if abs(y - cy) <= 19:        # 点中某个选项
            confirm_menu(i)
            return
    if running:
        close_menu()                 # 面板内但没点中选项 → 关闭菜单
    else:
        draw_menu()


# 按键绑定
screen.listen()
screen.onkey(lambda: handle_arrow((0, 1)), "Up")
screen.onkey(lambda: handle_arrow((0, -1)), "Down")
screen.onkey(lambda: handle_arrow((-1, 0)), "Left")
screen.onkey(lambda: handle_arrow((1, 0)), "Right")
screen.onkey(lambda: handle_arrow((0, 1)), "w")
screen.onkey(lambda: handle_arrow((0, -1)), "s")
screen.onkey(lambda: handle_arrow((-1, 0)), "a")
screen.onkey(lambda: handle_arrow((1, 0)), "d")
screen.onkey(handle_space, "space")
screen.onkey(toggle_menu, "Escape")
screen.onkey(lambda: confirm_menu(0), "1")          # 数字键快捷方式
screen.onkey(lambda: confirm_menu(1), "2")
screen.onkey(lambda: confirm_menu(2), "3")
screen.onkey(lambda: confirm_menu(selected), "Return")       # Enter 确认
screen.onkey(lambda: confirm_menu(selected), "KP_Enter")     # 小键盘回车
screen.onclick(on_menu_click)                       # 鼠标点击菜单

spawn_food()
draw()

# 主循环：ontimer 定时驱动，mainloop 持续处理按键事件，
# 这样暂停时键盘依然响应，不会卡死。
def game_loop():
    if running and not paused:
        step()
        if not menu_open:    # 撞自己刚结束时失败菜单已画好，别再重绘覆盖
            draw()
    screen.ontimer(game_loop, int(SPEED * 1000))


screen.ontimer(game_loop, int(SPEED * 1000))
screen.mainloop()
