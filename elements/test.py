from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = Tk()  # 创建tkinter的主窗口
root.title("练习窗口")
root.geometry('800x600+10+10')
# 标签
label1 = Label(root, text='测试窗口')
label1.place(x=0, y=0)
# 文本框
Text = Text(root, width=50, height=10)  # 测试文本框
Text.place(x=0, y=30)

# 图像及画布
fig = plt.figure(figsize=(4, 4), dpi=100)  # 图像比例
ax = fig.add_subplot(111)  # 划分区域
canvas_spice = FigureCanvasTkAgg(fig, root)
canvas_spice.get_tk_widget().place(x=0, y=200)  # 放置位置
ax.grid(True)  # 网格


def get_xl():
    return


# 按钮
button = Button(root, text='选择文件', bg='lightblue', width=10, command=get_xl)
button.place(x=400, y=1)

# 主循环
root.mainloop()