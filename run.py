
import copy
from tkinter import *
import tkinter.messagebox as msgbox

# 围墙
wall = 0
# 工人
worker = 1
# 箱子
box = 2
# 通道
passageway = 3
# 目的地
destination = 4
# 人在目的地
workerindest = 5
# 放到目的地的箱子
redbox = 6

size = 40

# 工人当前位置
x = y = 0

# 原始地图, 7*7
my_array1 = [[0, 3, 1, 4, 3, 3, 3],
             [0, 3, 3, 2, 3, 3, 0],
             [0, 0, 3, 0, 3, 3, 0],
             [3, 3, 2, 3, 0, 0, 0],
             [3, 4, 3, 3, 3, 0, 0],
             [0, 0, 3, 3, 3, 3, 0],
             [0, 0, 0, 0, 0, 0, 0]]

my_array = copy.deepcopy(my_array1)

root = Tk()

cv = Canvas(root, bg='green', width=280, height=280)

imgs = [PhotoImage(file="imgs/wall.png"),
        PhotoImage(file="imgs/man.png"),
        PhotoImage(file='imgs/box.png'),
        PhotoImage(file='imgs/road.png'),
        PhotoImage(file='imgs/target.png'),
        PhotoImage(file='imgs/target_s.png'),
        PhotoImage(file='imgs/red_box.png')]


def draw_game_image():
    """
    绘制游戏区域图形
    :return:
    """
    global x, y
    for i in range(0, 7):
        for j in range(0, 7):
            if my_array[i][j] == worker:
                x = i
                y = j
                print("工人当前位置:", x, y)
            img1 = imgs[my_array[i][j]]
            # 20 是固定值。显示效果为画板左侧有20像素在隐藏着。原因未知
            cv.create_image((i * size + 20, j * size + 20), image=img1)
    # cv.pack()


def is_in_game_area(row, col):
    """
    判断是否在游戏区域
    :param row:x轴方块位置
    :param col:y轴方块位置
    :return:
    """
    return 7 > row >= 0 and 7 > col >= 0


def is_finish():
    """
    是否游戏结束
    当地图中存在目的地或者工人站在目的地。认为游戏未结束（可以优化避免遍历
    :return:
    """
    for i in range(7):
        for j in range(7):
            if my_array[i][j] == destination or my_array[i][j] == workerindest:
                return False
    return True


def move_man(x, y):
    """
    把指定位置的工人移开
    :param x:
    :param y:
    :return:
    """
    # 若当前位置是工人。则设置当前位置为通道。
    # 若当前位置是站在目的地的工人。则设置当前位置为目的地
    if my_array[x][y] == worker:
        my_array[x][y] = passageway
    elif my_array[x][y] == workerindest:
        my_array[x][y] = destination


def showinfo(title, message):
    """
    弹出提示
    :param title:
    :param message:
    :return:
    """
    msgbox.showinfo(title, message)


def move_to(x1, y1, x2, y2):
    """
    移动到指定坐标
    :param x1:目标x
    :param y1:目标y
    :param x2:目标方向第二格x
    :param y2:目标方向第二格y
    :return:
    """
    global x, y
    p1 = None
    p2 = None
    if is_in_game_area(x1, y1):
        p1 = my_array[x1][y1]

    if is_in_game_area(x2, y2):
        # 判断是否在区域内
        p2 = my_array[x2][y2]

    if p1 == passageway:
        # p1 处为通道
        move_man(x, y)
        x = x1
        y = y1
        my_array[x1][y1] = worker

    if p1 == destination:
        # p1处为目的地
        move_man(x, y)
        x = x1
        y = y1
        my_array[x1][y1] = workerindest

    if p1 == wall or not is_in_game_area(x1, y1):
        # p1处为墙或出界
        return

    # p1处为箱子。
    if p1 == box:

        # p2处为墙或出界
        if p2 == wall or not is_in_game_area(x1, y1) or p2 == box:
            return

    # p1为箱子，p2为通道
    if p1 == box and p2 == passageway:
        print("p1 box p2 road")
        move_man(x, y)
        x = x1
        y = y1
        my_array[x2][y2] = box
        my_array[x1][y1] = worker

    # p1为箱子，p2为目的地
    if p1 == box and p2 == destination:
        move_man(x, y)
        x = x1
        y = y1
        my_array[x2][y2] = redbox
        my_array[x1][y1] = worker

    # p1为放到目的地的箱子，p2为通道
    if p1 == redbox and p2 == passageway:
        move_man(x, y)
        x = x1
        y = y1
        my_array[x2][y2] = box
        my_array[x1][y1] = workerindest

    # p1为放到目的地的箱子 p2为目的地
    if p1 == redbox and p2 == destination:
        move_man(x, y)
        x = x1
        y = y1
        my_array[x2][y2] = redbox
        my_array[x1][y1] = workerindest

    draw_game_image()

    if is_finish():
        showinfo(title='提示', message='恭喜你顺利过关')
        print("下一关")


def callback(event):
    """
    按键处理
    :param event:
    :return:
    """
    global x, y, my_array
    print("按下键:", event.char)
    key_code = event.keysym.lower()
    if key_code == 'up':
        # 向上移动
        x1 = x
        y1 = y - 1
        x2 = x
        y2 = y - 2
        move_to(x1, y1, x2, y2)
    elif key_code == 'down':
        x1 = x
        y1 = y + 1
        x2 = x
        y2 = y + 2
        move_to(x1, y1, x2, y2)
    elif key_code == 'left':
        x1 = x - 1
        y1 = y
        x2 = x - 2
        y2 = y
        move_to(x1, y1, x2, y2)
    elif key_code == 'right':
        x1 = x + 1
        y1 = y
        x2 = x + 2
        y2 = y
        move_to(x1, y1, x2, y2)
    elif key_code == 'space':
        # 空格键恢复原始地图
        print("按下键:", event.char)
        my_array = copy.deepcopy(my_array1)
        draw_game_image()


root.title("推啊推箱子-姬乙亥")
draw_game_image()
# 绑定按键回调函数
cv.bind("<KeyPress>", callback)
cv.pack()
# 把焦点设置到cv上
cv.focus_force()
root.mainloop()


