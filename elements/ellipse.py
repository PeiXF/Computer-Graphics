from pylab import *
from matplotlib.ticker import MultipleLocator
import matplotlib.patches as patches
import numpy as np

# 画布初始化
def init(ax):
    majorLocator = MultipleLocator(1)
    ax.xaxis.set_major_locator(majorLocator)
    ax.yaxis.set_major_locator(majorLocator)
    ax.grid(True)

# 画点(x, y)
def add_pixel(x, y, ax):
    x = round(x)
    y = round(y)
    ax.add_patch(patches.Rectangle((x - 0.5, y - 0.5), 1, 1, color='b'))
    ax.plot(x, y, 'y.')

# 当 f_ellipse < 0 时，点在椭圆内，反之在外
def f_ellipse(x, y, a, b):
    f = (x ** 2) / (a ** 2) + (y ** 2) / (b ** 2) - 1
    return f

if __name__ == '__main__':
    a, b = map(int, input("输入椭圆长半轴的短半轴: ").split(' '))
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
    show()