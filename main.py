import tkinter.ttk
import tkinter.messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pylab import *
from matplotlib.ticker import MultipleLocator
import matplotlib.patches as patches
from numpy.linalg import *
from numpy import *

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

# 平移变换，方向（x0, y0）
def translate(x, y, x0, y0):
    X = array([[x], [y], [1]])
    T = array([[1, 0, x0],
               [0, 1, y0],
               [0, 0,  1]])
    Y = T.dot(X)
    return round(Y[0, 0]), round(Y[1, 0])

# 旋转变换，圆心（x0, y0），角度a
def rotate(x, y, x0, y0, a):
    t = a * pi / 180
    X = array([[x], [y], [1]])
    R = array([[cos(t), -sin(t), 0],
               [sin(t),  cos(t), 0],
               [     0,       0, 1]])
    T = array([[1, 0, -x0],
               [0, 1, -y0],
               [0, 0,   1]])
    A = inv(T).dot(R).dot(T)
    Y = A.dot(X)
    return round(Y[0, 0]), round(Y[1, 0])

# 对称变换，对称轴（x1, y1）（x2, y2）
def reflect(x, y, x1, y1, x2, y2):
    X = array([[x], [y], [1]])
    if x1 == x2:
        return round(2 * x1 - x), y
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    m = (y2 - y1) / (x2 - x1)
    b = y1 - x1 * m
    t = arctan(m)
    T = array([[1, 0,  0],
               [0, 1, -b],
               [0, 0,  1]])
    R = array([[ cos(t), sin(t),  0],
               [-sin(t), cos(t),  0],
               [      0,      0,  1]])
    M = array([[1,  0, 0],
               [0, -1, 0],
               [0,  0, 1]])
    A = inv(T).dot(inv(R)).dot(M).dot(R).dot(T)
    Y = A.dot(X)
    return round(Y[0, 0]), round(Y[1, 0])

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
    while x - x0 <= y - y0:
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
    fill.geometry("1000x600+120+50")  # 设置窗口大小和位置
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
    canvas_spice = FigureCanvasTkAgg(fig, fill)
    canvas_spice.get_tk_widget().place(x=0, y=200)  # 放置位置
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
    canvas_spice = FigureCanvasTkAgg(fig, fill)
    canvas_spice.get_tk_widget().place(x=0, y=200)  # 放置位置
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
    canvas_spice = FigureCanvasTkAgg(fig, fill)
    canvas_spice.get_tk_widget().place(x=0, y=200)  # 放置位置
    a = eval(entryLine_x.get().strip())
    b = eval(entryLine_y.get().strip())
    draw_ellipse(a, b)

#定义点
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#定义线段
class Line:
    def __init__(self, point1, point2):     # 由两个端点输出化直线段
        if point1.y > point2.y:
            self.Y_max = point1.y       # 最大的y值
            self.Y_min = point2.y       # 新增Y_min属性储存直线中最小的y值，便于后面奇异点的判断
            self.X = point2.x           # 线段下端顶点的x值
            if point2.y == point1.y:  # 处理常数直线情况
                self.k = 0
            else:
                self.k = (point2.x - point1.x) / (point2.y - point1.y)  # 斜率的倒数
        else:
            self.Y_max = point2.y
            self.Y_min = point1.y
            self.X = point1.x
            if point2.y == point1.y:
                self.k = 0
            else:
                self.k = (point2.x - point1.x) / (point2.y - point1.y)

# 由线段列表生成多边形并画出显示
def draw_polygon(point_list, color):
    for i in range(len(point_list) - 1):
        plt.plot([point_list[i].x, point_list[i + 1].x],
                 [point_list[i].y, point_list[i + 1].y],
                 color=color)
    plt.plot([point_list[len(point_list) - 1].x, point_list[0].x],
             [point_list[len(point_list) - 1].y, point_list[0].y],
             color=color)

# 取得扫描的上下界
def get_y_area(point_list_new):
    global Y_max, Y_min
    Y_max = point_list_new[0].y
    Y_min = point_list_new[0].y
    for i in range(1, len(point_list_new)):
        if Y_max < point_list_new[i].y:
            Y_max = point_list_new[i].y
        if Y_min > point_list_new[i].y:
            Y_min = point_list_new[i].y
    return Y_max, Y_min

# 画每一条扫描线
def draw_cropoint_x(scan_y, line_list_new, ax):
    x_list = []
    for lines in line_list_new:
        if scan_y == lines.Y_min:        # 处理奇异点，因为奇异点一定出线在Y_min处，所以干脆直接在扫描的时候判断增加两个x坐标值
            x_list.append(lines.X)
        if lines.Y_min <= scan_y <= lines.Y_max:
            x = round(lines.X + (scan_y - lines.Y_min) * lines.k)
            x_list.append(x)
    x_list.sort()   # 按照顺序排列
    for i in range(0, len(x_list) - 1, 2):
        ax.plot(np.arange(x_list[i] + 1, x_list[i + 1]),
                np.array([scan_y] * (x_list[i + 1] - x_list[i] - 1)),
                ".", color='b')

# 填充多边形
def area_filling(line_list_new, point_list_new, ax):
    Y_max, Y_min = get_y_area(point_list_new)   # 获取扫描区域
    for scan_y in range(Y_min - 1, Y_max + 1):
        draw_cropoint_x(scan_y, line_list_new, ax)

# 扫描转换填充算法
def PolyFill(point_list, point_list_new, line_list, line_list_new, operation):
    ax = subplot(111, aspect='equal', title='fill')
    init(ax)
    if operation == "raw":
        draw_polygon(point_list, color='y')
        area_filling(line_list, point_list, ax)
    else:
        draw_polygon(point_list, color='y')
        draw_polygon(point_list_new, color='r')
        area_filling(line_list_new, point_list_new, ax)

# 【填充】页面
def B_fill_click():
    global fill, entryLine_x, entryLine_y, \
           entryLine_x_t, entryLine_y_t,\
           entryLine_x0_r, entryLine_y0_r, entryLine_a_r,\
           entryLine_x1, entryLine_y1, entryLine_x2, entryLine_y2,\
           point_list, point_list_new, line_list, line_list_new,\
           point_list_add, line_list_add,\
           point_list_rotate, line_list_rotate,\
           point_list_reflect, line_list_reflect
    point_list = []  # 点组成的列表
    point_list_new = []
    point_list_add = []
    point_list_rotate = []
    point_list_reflect = []
    line_list = []  # 线段组成的列表
    line_list_new = []
    line_list_add = []
    line_list_rotate = []
    line_list_reflect = []
    fill = tkinter.Tk()  # 创建tkinter应用程序窗口
    fill.geometry("1100x600+120+50")  # 设置窗口大小和位置
    fill.resizable(False, False)  # 不允许改变窗口大小
    fill.title("填充")  # 设置窗口标题

    # 在窗口上放置标签组件和用于输入坐标的文本框组件
    # 【添加】
    lbLine_x = tkinter.Label(fill, text='新增顶点横坐标 x：')
    lbLine_x.place(x=20, y=10, width=130, height=20)
    entryLine_x = tkinter.Entry(fill)
    entryLine_x.place(x=150, y=10, width=80, height=20)
    lbLine_y = tkinter.Label(fill, text='新增顶点纵坐标 y：')
    lbLine_y.place(x=20, y=50, width=130, height=20)
    entryLine_y = tkinter.Entry(fill)
    entryLine_y.place(x=150, y=50, width=80, height=20)
    B_fill_draw = tkinter.Button(fill, text='添加', command=B_fill_add_click)
    B_fill_draw.place(x=250, y=10, width=160, height=60)

    # 【平移】
    lbLine_x_t = tkinter.Label(fill, text='平移向量横坐标 x：')
    lbLine_x_t.place(x=20, y=130, width=130, height=20)
    entryLine_x_t = tkinter.Entry(fill)
    entryLine_x_t.place(x=150, y=130, width=80, height=20)
    lbLine_y_t = tkinter.Label(fill, text='平移向量纵坐标 y：')
    lbLine_y_t.place(x=20, y=170, width=130, height=20)
    entryLine_y_t = tkinter.Entry(fill)
    entryLine_y_t.place(x=150, y=170, width=80, height=20)
    B_fill_draw = tkinter.Button(fill, text='平移', command=B_fill_translate_click)
    B_fill_draw.place(x=250, y=130, width=160, height=60)

    # 【旋转】
    lbLine_x0_r = tkinter.Label(fill, text='旋转中心横坐标 x0：')
    lbLine_x0_r.place(x=20, y=250, width=130, height=20)
    entryLine_x0_r = tkinter.Entry(fill)
    entryLine_x0_r.place(x=150, y=250, width=80, height=20)
    lbLine_y0_r = tkinter.Label(fill, text='旋转中心纵坐标 y0：')
    lbLine_y0_r.place(x=20, y=290, width=130, height=20)
    entryLine_y0_r = tkinter.Entry(fill)
    entryLine_y0_r.place(x=150, y=290, width=80, height=20)
    lbLine_a_r = tkinter.Label(fill, text='旋转角度 a：')
    lbLine_a_r.place(x=20, y=330, width=130, height=20)
    entryLine_a_r = tkinter.Entry(fill)
    entryLine_a_r.place(x=150, y=330, width=80, height=20)
    B_fill_draw = tkinter.Button(fill, text='旋转', command=B_fill_rotate_click)
    B_fill_draw.place(x=250, y=250, width=160, height=100)

    # 【对称】
    lbLine_x1 = tkinter.Label(fill, text='对称轴第一个点 x1：')
    lbLine_x1.place(x=20, y=410, width=130, height=20)
    entryLine_x1 = tkinter.Entry(fill)
    entryLine_x1.place(x=150, y=410, width=80, height=20)
    lbLine_y1 = tkinter.Label(fill, text='对称轴第一个点 y1：')
    lbLine_y1.place(x=20, y=450, width=130, height=20)
    entryLine_y1 = tkinter.Entry(fill)
    entryLine_y1.place(x=150, y=450, width=80, height=20)
    lbLine_x2 = tkinter.Label(fill, text='对称轴第二个点 x2：')
    lbLine_x2.place(x=20, y=490, width=130, height=20)
    entryLine_x2 = tkinter.Entry(fill)
    entryLine_x2.place(x=150, y=490, width=80, height=20)
    lbLine_y2 = tkinter.Label(fill, text='对称轴第二个点 y2：')
    lbLine_y2.place(x=20, y=530, width=130, height=20)
    entryLine_y2 = tkinter.Entry(fill)
    entryLine_y2.place(x=150, y=530, width=80, height=20)
    B_fill_draw = tkinter.Button(fill, text='对称', command=B_fill_reflect_click)
    B_fill_draw.place(x=250, y=410, width=160, height=140)

# 【填充】【添加】
def B_fill_add_click():
    x = eval(entryLine_x.get().strip())
    y = eval(entryLine_y.get().strip())
    point_list.append(Point(x, y))

    line_list = []  # 线段组成的列表
    for i in range(len(point_list) - 1):
        temp_line = Line(point_list[i], point_list[i + 1])
        line_list.append(temp_line)
    temp_line = Line(point_list[len(point_list) - 1], point_list[0])
    line_list.append(temp_line)

    fig = plt.figure(figsize=(6, 6), dpi=100)  # 图像比例
    canvas_spice = FigureCanvasTkAgg(fig, fill)
    canvas_spice.get_tk_widget().place(x=450, y=0)  # 放置位置
    PolyFill(point_list, point_list_new, line_list, line_list_new, operation="raw")

# 【填充】【平移】
def B_fill_translate_click():
    x0 = eval(entryLine_x_t.get().strip())
    y0 = eval(entryLine_y_t.get().strip())

    point_list_new = []
    for p in point_list:
        x_new, y_new = translate(p.x, p.y, x0, y0)
        point_list_new.append(Point(x_new, y_new))

    line_list = []  # 线段组成的列表
    line_list_new = []
    for i in range(len(point_list) - 1):
        temp_line = Line(point_list[i], point_list[i + 1])
        line_list.append(temp_line)
    temp_line = Line(point_list[len(point_list) - 1], point_list[0])
    line_list.append(temp_line)
    for i in range(len(point_list_new) - 1):
        temp_line_new = Line(point_list_new[i], point_list_new[i + 1])
        line_list_new.append(temp_line_new)
    temp_line_new = Line(point_list_new[len(point_list_new) - 1], point_list_new[0])
    line_list_new.append(temp_line_new)

    fig = plt.figure(figsize=(6, 6), dpi=100)  # 图像比例
    canvas_spice = FigureCanvasTkAgg(fig, fill)
    canvas_spice.get_tk_widget().place(x=450, y=0)  # 放置位置
    PolyFill(point_list, point_list_new, line_list, line_list_new, operation="translate")

# 【填充】【旋转】
def B_fill_rotate_click():
    x0 = eval(entryLine_x0_r.get().strip())
    y0 = eval(entryLine_y0_r.get().strip())
    a = eval(entryLine_a_r.get().strip())

    point_list_new = []
    for p in point_list:
        x_new, y_new = rotate(p.x, p.y, x0, y0, a)
        point_list_new.append(Point(x_new, y_new))

    line_list = []  # 线段组成的列表
    line_list_new = []
    for i in range(len(point_list) - 1):
        temp_line = Line(point_list[i], point_list[i + 1])
        line_list.append(temp_line)
    temp_line = Line(point_list[len(point_list) - 1], point_list[0])
    line_list.append(temp_line)
    for i in range(len(point_list_new) - 1):
        temp_line_new = Line(point_list_new[i], point_list_new[i + 1])
        line_list_new.append(temp_line_new)
    temp_line_new = Line(point_list_new[len(point_list_new) - 1], point_list_new[0])
    line_list_new.append(temp_line_new)

    fig = plt.figure(figsize=(6, 6), dpi=100)  # 图像比例
    canvas_spice = FigureCanvasTkAgg(fig, fill)
    canvas_spice.get_tk_widget().place(x=450, y=0)  # 放置位置
    PolyFill(point_list, point_list_new, line_list, line_list_new, operation="rotate")

# 【填充】【对称】
def B_fill_reflect_click():
    x1 = eval(entryLine_x1.get().strip())
    y1 = eval(entryLine_y1.get().strip())
    x2 = eval(entryLine_x2.get().strip())
    y2 = eval(entryLine_y2.get().strip())

    point_list_new = []
    for p in point_list:
        x_new, y_new = reflect(p.x, p.y, x1, y1, x2, y2)
        point_list_new.append(Point(x_new, y_new))

    line_list = []  # 线段组成的列表
    line_list_new = []
    for i in range(len(point_list) - 1):
        temp_line = Line(point_list[i], point_list[i + 1])
        line_list.append(temp_line)
    temp_line = Line(point_list[len(point_list) - 1], point_list[0])
    line_list.append(temp_line)
    for i in range(len(point_list_new) - 1):
        temp_line_new = Line(point_list_new[i], point_list_new[i + 1])
        line_list_new.append(temp_line_new)
    temp_line_new = Line(point_list_new[len(point_list_new) - 1], point_list_new[0])
    line_list_new.append(temp_line_new)

    fig = plt.figure(figsize=(6, 6), dpi=100)  # 图像比例
    canvas_spice = FigureCanvasTkAgg(fig, fill)
    canvas_spice.get_tk_widget().place(x=450, y=0)  # 放置位置
    PolyFill(point_list, point_list_new, line_list, line_list_new, operation="reflect")

# 程序入口
if __name__ == '__main__':
    main()