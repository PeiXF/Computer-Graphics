from pylab import *
from matplotlib.ticker import MultipleLocator
import matplotlib.patches as patches

def init(ax):
    majorLocator = MultipleLocator(1)
    ax.xaxis.set_major_locator(majorLocator)
    ax.yaxis.set_major_locator(majorLocator)
    ax.grid(True)

def add_pixel_l(x, y, ax, c):
    x = round(x)
    y = round(y)
    if c == 1:
        ax.add_patch(patches.Rectangle((x - 0.5, y - 0.5), 1, 1, color='b'))
        ax.plot(x, y, 'r.')
    else:
        ax.add_patch(patches.Rectangle((x - 0.5, y - 0.5), 1, 1))
        ax.plot(x, y, 'y.')

if __name__ == '__main__':
    x0, y0, x1, y1 = map(int, input("输入直线的两点: ").split(' '))
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    ax = subplot(121, aspect='equal', title='Bresenham')
    ax.plot([x0, x1], [y0, y1], '-k')
    bx = subplot(122, aspect='equal', title='DDA')
    bx.plot([x0, x1], [y0, y1], '-k')

    init(ax)
    init(bx)
    delta_x = x1 - x0
    delta_y = y1 - y0
    d = 0
    if delta_x == 0:
        k = 999999999
    else:
        k = delta_y / delta_x
    x = round(x0)
    y = round(y0)
    '''
    DDA算法
    '''
    if -1 < k < 1:
        # X 最大位移
        while x <= x1:
            add_pixel_l(x, y, bx, 1)
            x = x+1
            y = y+k
    elif k >= 1:
        # Y 最大位移
        while y <= y1:
            add_pixel_l(x, y, bx, 1)
            y = y+1
            x = x+1/k
    else:
        while y >= y1:
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
    x = x0
    y = y0
    if k > 1:
        while y <= y1:
            add_pixel_l(x, y, ax, 0)
            y = y + 1
            d = d + 1 / k
            if d > 0.5:
                x = x + 1
                d = d - 1
    elif k > 0:
        while x <= x1:
            add_pixel_l(x, y, ax, 0)
            x = x + 1
            d = d + k
            if d > 0.5:
                y = y + 1
                d = d - 1
    elif k > -1:
        while x <= x1:
            add_pixel_l(x, y, ax, 0)
            x = x + 1
            d = d - k
            if d > 0.5:
                y = y - 1
                d = d - 1
    else:
        while y >= y1:
            add_pixel_l(x, y, ax, 0)
            y = y - 1
            d = d - 1 / k
            if d > 0.5:
                x = x + 1
                d = d - 1
    show()