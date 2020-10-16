import tkinter
import tkinter.ttk
import tkinter.messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pylab import *
from matplotlib.ticker import MultipleLocator
import matplotlib.patches as patches
import numpy as np

# 主函数
def main():
    root = tkinter.Tk()  # 创建tkinter应用程序窗口
    root.geometry("550x600+120+50")  # 设置窗口大小和位置
    root.resizable(False, False)  # 不允许改变窗口大小
    root.title("线元绘制与图形填充")  # 设置窗口标题

    B_line = tkinter.Button(root, text='直线', command=B_line_click)
    B_line.place(x=180, y=140, width=160, height=40)
    B_circle = tkinter.Button(root, text='圆', command=B_circle_click)
    B_circle.place(x=180, y=220, width=160, height=40)
    B_ellipse = tkinter.Button(root, text='椭圆', command=B_ellipse_click)
    B_ellipse.place(x=180, y=300, width=160, height=40)
    B_fill = tkinter.Button(root, text='填充', command=B_fill_click)
    B_fill.place(x=180, y=380, width=160, height=40)

    root.mainloop()

# 画布初始化
def init(ax):
    majorLocator = MultipleLocator(1)
    ax.xaxis.set_major_locator(majorLocator)
    ax.yaxis.set_major_locator(majorLocator)
    ax.grid(True)

# 画点（线）
def add_pixel_l(x, y, ax, c):
    x = round(x)
    y = round(y)
    if c == 1:
        ax.add_patch(patches.Rectangle((x - 0.5, y - 0.5), 1, 1, color='b'))
        ax.plot(x, y, 'r.')
    else:
        ax.add_patch(patches.Rectangle((x - 0.5, y - 0.5), 1, 1))
        ax.plot(x, y, 'y.')

# 画点（圆/椭圆）
def add_pixel(x, y, ax):
    x = round(x)
    y = round(y)
    ax.add_patch(patches.Rectangle((x - 0.5, y - 0.5), 1, 1, color='b'))
    ax.plot(x, y, 'y.')

# 当 f_circle < 0 时，点在圆内，反之在外
def f_circle(x, y, x0, y0, r):
    f = (x - x0) ** 2 + (y - y0) ** 2 - r ** 2
    return f

# 当 f_ellipse < 0 时，点在椭圆内，反之在外
def f_ellipse(x, y, a, b):
    f = (x ** 2) / (a ** 2) + (y ** 2) / (b ** 2) - 1
    return f

# 画线
def draw_line(x1, y1, x2, y2):
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    ax = subplot(121, aspect='equal', title='Bresenham')
    ax.plot([x1, x2], [y1, y2], '-k')
    bx = subplot(122, aspect='equal', title='DDA')
    bx.plot([x1, x2], [y1, y2], '-k')

    init(ax)
    init(bx)
    delta_x = x2 - x1
    delta_y = y2 - y1
    d = 0
    if delta_x == 0:
        k = 999999999
    else:
        k = delta_y / delta_x
    x = round(x1)
    y = round(y1)
    '''
    DDA算法
    '''
    if -1 < k < 1:
        # X 最大位移
        while x <= x2:
            add_pixel_l(x, y, bx, 1)
            x = x+1
            y = y+k
    elif k >= 1:
        # Y 最大位移
        while y <= y2:
            add_pixel_l(x, y, bx, 1)
            y = y+1
            x = x+1/k
    else:
        while y >= y2:
            add_pixel_l(x, y, bx, 1)
            y = y-1
            x = x-1/k

    '''
    k的范围
    1.  (0,1)    x为最大位移，y正向增加
    2.  (1,+inf) y为最大位移，x正向增加
    3.  (0,-1)   x为最大位移，y负向增加
    4.  (-1,-inf)y为最大位移，y减小。x正向增加
    '''
    x = x1
    y = y1
    if k > 1:
        while y <= y2:
            add_pixel_l(x, y, ax, 0)
            y = y + 1
            d = d + 1 / k
            if d > 0.5:
                x = x + 1
                d = d - 1
    elif k > 0:
        while x <= x2:
            add_pixel_l(x, y, ax, 0)
            x = x + 1
            d = d + k
            if d > 0.5:
                y = y + 1
                d = d - 1
    elif k > -1:
        while x <= x2:
            add_pixel_l(x, y, ax, 0)
            x = x + 1
            d = d - k
            if d > 0.5:
                y = y - 1
                d = d - 1
    else:
        while y >= y2:
            add_pixel_l(x, y, ax, 0)
            y = y - 1
            d = d - 1 / k
            if d > 0.5:
                x = x + 1
                d = d - 1

# 画圆
def draw_circle(x0, y0, r):
    ax = subplot(111, aspect='equal', title='circle')
    init(ax)
    ax.plot(x0, y0, 'r.')
    theta = np.linspace(0, 2 * np.pi, 100)
    theta = np.append(theta, [2 * np.pi])
    x = x0 + r * np.cos(theta)
    y = y0 + r * np.sin(theta)
    ax.plot(x, y)
    (x, y) = (x0, y0 + r)

    # 只需画出八分之一圆弧，剩下部分通过对称性即可得到
    # plt.ion()
    while x - x0 <= y - y0:
        # plt.pause(0.1)
        add_pixel(x, y, ax)
        add_pixel(x0 - y0 + y, y0 - x0 + x, ax)
        add_pixel(x, 2 * y0 - y, ax)
        add_pixel(x0 - y0 + 2 * y0 - y, y0 - x0 + x, ax)
        add_pixel(2 * x0 - x, y, ax)
        add_pixel(x0 - y0 + y, y0 - x0 + 2 * x0 - x, ax)
        add_pixel(2 * x0 - x, 2 * y0 - y, ax)
        add_pixel(x0 - y0 + 2 * y0 - y, y0 - x0 + 2 * x0 - x, ax)
        if f_circle(x + 1, y - 0.5, x0, y0, r) <= 0:
            (x, y) = (x + 1, y)
        else:
            (x, y) = (x + 1, y - 1)
    # plt.ioff()

# 画椭圆
def draw_ellipse(a, b):
    ax = subplot(111, aspect='equal', title='ellipse')
    init(ax)
    ax.plot(0, 0, 'r.')
    theta = np.linspace(0, 2 * np.pi, 100)
    theta = np.append(theta, [2 * np.pi])
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    ax.plot(x, y)
    (x, y) = (0, b)

    # 只需画出四分之一椭圆，剩下部分通过对称性即可得到
    # 1. 以切线斜率为-1处为分界，画出四分之一椭圆的上半部分
    while x * b ** 2 <= y * a ** 2:
        add_pixel(x, y, ax)
        add_pixel(x, -y, ax)
        add_pixel(-x, y, ax)
        add_pixel(-x, -y, ax)
        if f_ellipse(x + 1, y - 0.5, a, b) <= 0:
            (x, y) = (x + 1, y)
        else:
            (x, y) = (x + 1, y - 1)
    # 2. 再以切线斜率为-1处为分界，画出四分之一椭圆的下半部分
    while y >= 0:
        add_pixel(x, y, ax)
        add_pixel(x, -y, ax)
        add_pixel(-x, y, ax)
        add_pixel(-x, -y, ax)
        if f_ellipse(x + 0.5, y - 1, a, b) <= 0:
            (x, y) = (x + 1, y - 1)
        else:
            (x, y) = (x, y - 1)

# 【直线】页面
def B_line_click():
    global fill, entryLine_x1, entryLine_y1, entryLine_x2, entryLine_y2
    fill = tkinter.Tk()  # 创建tkinter应用程序窗口
    fill.geometry("1100x600+120+50")  # 设置窗口大小和位置
    fill.resizable(False, False)  # 不允许改变窗口大小
    fill.title("直线")  # 设置窗口标题

    # 在窗口上放置标签组件和用于输入坐标的文本框组件
    lbLine_x1 = tkinter.Label(fill, text='第一个点的横坐标 x1：')
    lbLine_x1.place(x=20, y=10, width=130, height=20)
    entryLine_x1 = tkinter.Entry(fill)
    entryLine_x1.place(x=150, y=10, width=80, height=20)
    lbLine_y1 = tkinter.Label(fill, text='第一个点的纵坐标 y1：')
    lbLine_y1.place(x=20, y=50, width=130, height=20)
    entryLine_y1 = tkinter.Entry(fill)
    entryLine_y1.place(x=150, y=50, width=80, height=20)
    lbLine_x2 = tkinter.Label(fill, text='第二个点的横坐标 x2：')
    lbLine_x2.place(x=20, y=90, width=130, height=20)
    entryLine_x2 = tkinter.Entry(fill)
    entryLine_x2.place(x=150, y=90, width=80, height=20)
    lbLine_y2 = tkinter.Label(fill, text='第二个点的纵坐标 y2：')
    lbLine_y2.place(x=20, y=130, width=130, height=20)
    entryLine_y2 = tkinter.Entry(fill)
    entryLine_y2.place(x=150, y=130, width=80, height=20)
    B_line_draw = tkinter.Button(fill, text='绘制', command=B_line_draw_click)
    B_line_draw.place(x=300, y=10, width=160, height=150)

# 【直线】【绘制】
def B_line_draw_click():
    fig = plt.figure(figsize=(10, 4), dpi=100)  # 图像比例
    ax = fig.add_subplot(111)  # 划分区域
    canvas_spice = FigureCanvasTkAgg(fig, fill)
    canvas_spice.get_tk_widget().place(x=0, y=200)  # 放置位置
    init(ax)
    x1 = eval(entryLine_x1.get().strip())
    y1 = eval(entryLine_y1.get().strip())
    x2 = eval(entryLine_x2.get().strip())
    y2 = eval(entryLine_y2.get().strip())
    draw_line(x1, y1, x2, y2)

# 【圆】页面
def B_circle_click():
    global fill, entryLine_x, entryLine_y, entryLine_r
    fill = tkinter.Tk()  # 创建tkinter应用程序窗口
    fill.geometry("550x600+120+50")  # 设置窗口大小和位置
    fill.resizable(False, False)  # 不允许改变窗口大小
    fill.title("圆")  # 设置窗口标题

    # 在窗口上放置标签组件和用于输入坐标的文本框组件
    lbLine_x0 = tkinter.Label(fill, text='圆心的横坐标 x0：')
    lbLine_x0.place(x=20, y=10, width=130, height=20)
    entryLine_x = tkinter.Entry(fill)
    entryLine_x.place(x=150, y=10, width=80, height=20)
    lbLine_y0 = tkinter.Label(fill, text='圆心的纵坐标 y0：')
    lbLine_y0.place(x=20, y=50, width=130, height=20)
    entryLine_y = tkinter.Entry(fill)
    entryLine_y.place(x=150, y=50, width=80, height=20)
    lbLine_r = tkinter.Label(fill, text='圆的半径 r：')
    lbLine_r.place(x=20, y=90, width=130, height=20)
    entryLine_r = tkinter.Entry(fill)
    entryLine_r.place(x=150, y=90, width=80, height=20)
    B_circle_draw = tkinter.Button(fill, text='绘制', command=B_circle_draw_click)
    B_circle_draw.place(x=300, y=10, width=160, height=150)

# 【圆】【绘制】
def B_circle_draw_click():
    fig = plt.figure(figsize=(4, 4), dpi=100)  # 图像比例
    ax = fig.add_subplot(111)  # 划分区域
    canvas_spice = FigureCanvasTkAgg(fig, fill)
    canvas_spice.get_tk_widget().place(x=0, y=200)  # 放置位置
    init(ax)
    x0 = eval(entryLine_x.get().strip())
    y0 = eval(entryLine_y.get().strip())
    r = eval(entryLine_r.get().strip())
    draw_circle(x0, y0, r)

# 【椭圆】页面
def B_ellipse_click():
    global fill, entryLine_x, entryLine_y
    fill = tkinter.Tk()  # 创建tkinter应用程序窗口
    fill.geometry("550x600+120+50")  # 设置窗口大小和位置
    fill.resizable(False, False)  # 不允许改变窗口大小
    fill.title("椭圆")  # 设置窗口标题

    # 在窗口上放置标签组件和用于输入坐标的文本框组件
    lbLine_a = tkinter.Label(fill, text='椭圆的长半轴 a：')
    lbLine_a.place(x=20, y=10, width=130, height=20)
    entryLine_x = tkinter.Entry(fill)
    entryLine_x.place(x=150, y=10, width=80, height=20)
    lbLine_b = tkinter.Label(fill, text='椭圆的短半轴 b：')
    lbLine_b.place(x=20, y=50, width=130, height=20)
    entryLine_y = tkinter.Entry(fill)
    entryLine_y.place(x=150, y=50, width=80, height=20)
    B_ellipse_draw = tkinter.Button(fill, text='绘制', command=B_ellipse_draw_click)
    B_ellipse_draw.place(x=300, y=10, width=160, height=150)

# 【椭圆】【绘制】
def B_ellipse_draw_click():
    fig = plt.figure(figsize=(4, 4), dpi=100)  # 图像比例
    ax = fig.add_subplot(111)  # 划分区域
    canvas_spice = FigureCanvasTkAgg(fig, fill)
    canvas_spice.get_tk_widget().place(x=0, y=200)  # 放置位置
    init(ax)
    a = eval(entryLine_x.get().strip())
    b = eval(entryLine_y.get().strip())
    draw_ellipse(a, b)

# 定义节点
class Node:
    def __init__(self, data):
        self._data = data
        self._next = None

    def get_data(self):
        return self._data

    def get_next(self):
        return self._next

    def set_data(self, ddata):
        self._data = ddata

    def set_next(self, nnext):
        self._next = nnext

# 定义链表
class SingleLinkList:
    def __init__(self):
        #初始化链表为空
        self._head = None
        self._size = 0

    def get_head(self):
        #获取链表头
        return self._head

    def is_empty(self):
        #判断链表是否为空
        return self._head is None

    def append(self, data):
        #在链表尾部追加一个节点
        temp = Node(data)
        if self._head is None:
            self._head = temp
        else:
            node = self._head
            while node.get_next() is not None:
                node = node.get_next()
            node.set_next(temp)
        self._size += 1

    def remove(self, data):
        # 在链表尾部删除一个节点
        node = self._head
        prev = None
        while node is not None:
            if node.get_data() == data:
                if not prev:
                    # 父节点为None
                    self._head = node.get_next()
                else:
                    prev.set_next(node.get_next())
                break
            else:
                prev = node
                node = node.get_next()
        self._size -= 1

# 扫描转换填充算法
def PolyFill(image, polygon, color):
    l = len(polygon)
    Ymax = 0
    Ymin = np.shape(image)[1]
    (width, height) = np.shape(image)
    #求最大最小边
    for [x, y] in enumerate(polygon):
        if y[1] < Ymin:
            Ymin = y[1]
        if y[1] > Ymax:
            Ymax = y[1]

    #初始化并建立NET表
    NET = []
    for i in range(height):
        NET.append(None)

    for i in range(Ymin, Ymax + 1):
        for j in range(0, l):
            if polygon[j][1] == i:
                #左边顶点y是否大于y0
                if (polygon[(j-1+l) % l][1]) > polygon[j][1]:
                    [x1, y1] = polygon[(j-1+l) % l]
                    [x0, y0] = polygon[j]
                    delta_x = (x1-x0) / (y1-y0)
                    NET[i] = SingleLinkList()
                    NET[i].append([x0, delta_x, y1])

                # 右边顶点y是否大于y0
                if (polygon[(j+1+l) % l][1]) > polygon[j][1]:
                    [x1, y1] = polygon[(j + 1 + l) % l]
                    [x0, y0] = polygon[j]
                    delta_x = (x1 - x0) / (y1 - y0)
                    if NET[i] is not None:
                        NET[i].append([x0, delta_x, y1])
                    else:
                        NET[i] = SingleLinkList()
                        NET[i].append([x0, delta_x, y1])

    #建立活性边表
    AET = SingleLinkList()
    for y in range(Ymin, Ymax+1):
        # 更新 start_x
        if not AET.is_empty():
            node = AET.get_head()
            while True:
                [start_x, delta_x, ymax] = node.get_data()
                start_x += delta_x
                node.set_data([start_x, delta_x, ymax])
                node = node.get_next()
                if node is None:
                    break

        # 填充
        if not AET.is_empty():
            node = AET.get_head()
            x_list = []
            # 获取所有交点的x坐标
            while True:
                [start_x, _, _] = node.get_data()
                x_list.append(start_x)
                node = node.get_next()
                if node is None:
                    break

            # 排序
            x_list.sort()
            # 两两配对填充
            for i in range(0, len(x_list), 2):
                x1 = x_list[i]
                x2 = x_list[i+1]
                for pixel in range(int(x1), int(x2)+1):
                    image[y][pixel] = color

        if not AET.is_empty():
            # 删除非活性边
            node = AET.get_head()
            while True:
                [start_x, delta_x, ymax] = node.get_data()
                if ymax == y:
                    AET.remove([start_x, delta_x, ymax])
                node = node.get_next()
                if node is None:
                    break

        # 添加活性边
        if NET[y] is not None:
            node = NET[y].get_head()
            while True:
                AET.append(node.get_data())
                node = node.get_next()
                if node is None:
                    break

# 【填充】页面
def B_fill_click():
    global fill, entryLine_x, entryLine_y, polygon
    polygon = []
    fill = tkinter.Tk()  # 创建tkinter应用程序窗口
    fill.geometry("550x600+120+50")  # 设置窗口大小和位置
    fill.resizable(False, False)  # 不允许改变窗口大小
    fill.title("填充")  # 设置窗口标题

    # 在窗口上放置标签组件和用于输入坐标的文本框组件
    lbLine_x = tkinter.Label(fill, text='新增顶点的横坐标 x：')
    lbLine_x.place(x=20, y=10, width=130, height=20)
    entryLine_x = tkinter.Entry(fill)
    entryLine_x.place(x=150, y=10, width=80, height=20)
    lbLine_y = tkinter.Label(fill, text='新增顶点的纵坐标 y：')
    lbLine_y.place(x=20, y=50, width=130, height=20)
    entryLine_y = tkinter.Entry(fill)
    entryLine_y.place(x=150, y=50, width=80, height=20)
    B_fill_draw = tkinter.Button(fill, text='添加', command=B_fill_add_click)
    B_fill_draw.place(x=300, y=10, width=160, height=150)

# 【填充】【添加】
def B_fill_add_click():
    x = eval(entryLine_x.get().strip())
    y = eval(entryLine_y.get().strip())
    polygon.append([x, y])
    # polygon = [[20, 20],
    #            [120, 20],
    #            [70, 100],
    #            [50, 80],
    #            [30, 120],
    #            [20, 50],
    #            [50, 50]]

    fig = plt.figure(figsize=(4, 4), dpi=100)  # 图像比例
    ax = fig.add_subplot(111)  # 划分区域
    canvas_spice = FigureCanvasTkAgg(fig, fill)
    canvas_spice.get_tk_widget().place(x=0, y=200)  # 放置位置

    x = [i[0] for i in polygon]
    y = [i[1] for i in polygon]
    image = np.ones((max(y) + 2, max(x) + 2))
    plt.xlim(min(x), max(x) + 1)
    plt.ylim(min(y), max(y) + 1)

    PolyFill(image, polygon, False)
    ax.imshow(image, plt.cm.magma)

# 程序入口
if __name__ == '__main__':
    main()