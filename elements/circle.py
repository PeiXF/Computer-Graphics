from pylab import *
from matplotlib.ticker import MultipleLocator
import matplotlib.patches as patches
import numpy as np

# 画布初始化
def init(ax):
    ax.cla()
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

# 当 f_ellipse < 0 时，点在圆内，反之在外
def f_circle(x, y, x0, y0, r):
    f = (x - x0) ** 2 + (y - y0) ** 2 - r ** 2
    return f

if __name__ == '__main__':
    x0, y0, r = map(int, input("输入圆心坐标和半径: ").split(' '))
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
    show()
    plt.cla()
    show()