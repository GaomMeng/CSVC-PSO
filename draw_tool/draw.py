import numpy as np
import matplotlib.pyplot as plt
from draw_tool.utils import get_data_list, get_arguments, check_arguments


def draw_from_file(**kwargs):
    """
    给定文件夹，获取数据绘制图像
    """
    data_file = get_arguments(['filename', 'f', 'path'], kwargs)
    max_step = check_arguments(['max_step', 'max_steps', 'm', 'max'], kwargs, 100)
    time_fac = check_arguments(['b', 'time_fac'], kwargs, 100)
    save_path = check_arguments(['save_path', 'SavePath'], kwargs, False)
    xlabel = check_arguments(['xlable', 'x'], kwargs, f'MPB, b={int(time_fac)}')
    ylabel = check_arguments(['ylable', 'y'], kwargs, 'Accumulated Fitness')
    title = check_arguments(['title', 't'], kwargs, 'data plot')

    mean_lst1, std_list1 = get_data_list([f'b={int(time_fac)}_MPB', '_OPT'], data_file, max_step)
    mean_lst2, std_list2 = get_data_list([f'b={int(time_fac)}_MPB', '_PSO'], data_file, max_step)
    mean_lst3, std_list3 = get_data_list([f'b={int(time_fac)}_MPB', '_POC'], data_file, max_step)

    x_list = [i + 1 for i in range(len(mean_lst1))]
    fig, ax = plt.subplots()  # 创建图实例

    ax.plot(x_list, mean_lst3, color='lime', label='Our', linestyle='-.')
    ax.fill_between(x_list, [mean_lst3[i] + std_list3[i] for i in range(len(x_list))],
                    [mean_lst3[i] - std_list3[i] for i in range(len(x_list))],  # 上限，下限
                    facecolor='lime',  # 填充颜色
                    alpha=0.3)  # 透明度

    ax.plot(x_list, mean_lst2, color='magenta', label='PSO', linestyle='--')
    ax.fill_between(x_list, [mean_lst2[i] + std_list2[i] for i in range(len(x_list))],
                    [mean_lst2[i] - std_list2[i] for i in range(len(x_list))],  # 上限，下限
                    facecolor='magenta',  # 填充颜色
                    alpha=0.3)  # 透明度

    ax.plot(x_list, mean_lst1, color='red', label='Optimal', linestyle='-')
    ax.fill_between(x_list, [mean_lst1[i] + std_list1[i] for i in range(len(x_list))],
                    [mean_lst1[i] - std_list1[i] for i in range(len(x_list))],  # 上限，下限
                    facecolor='red',  # 填充颜色
                    alpha=0.3)  # 透明度


    ax.set_xlabel(xlabel)  # 设置x轴名称 x label
    ax.set_ylabel(ylabel)  # 设置y轴名称 y label
    # ax.axis([0, max_step, 0, np.max(mean_lst1) + 0.1*np.max(mean_lst1)])
    ax.axis([0, max_step, np.min(mean_lst1) - 0.1 * np.max(mean_lst1), np.max(mean_lst1) + 0.1 * np.max(mean_lst1)])
    # plt.yticks([0, 5000, 10000, 15000])
    # 坐标轴刻度（tick）与刻度值（tick label）操作
    ax.tick_params(axis='y',  # 对那个方向（x方向：上下轴；y方向：左右轴）的坐标轴上的tick操作，可选参数{'x', 'y', 'both'}
                   which='both',  # 对主刻度还是次要刻度操作，可选参数为{'major', 'minor', 'both'}
                   colors='k',  # 刻度颜色

                   # 以下四个参数控制上下左右四个轴的刻度的关闭和开启
                   top='on',  # 上轴开启了刻度值和轴之间的线
                   bottom='on',  # x轴关闭了刻度值和轴之间的线
                   left='on',
                   right='on',

                   direction='in',  # tick的方向，可选参数{'in', 'out', 'inout'}
                   length=5,  # tick长度
                   width=1,  # tick的宽度
                   # pad=5000,  # tick与刻度值之间的距离
                   labelsize=10,  # 刻度值大小
                   # labelcolor='#008856',  # 刻度值的颜色
                   zorder=0,

                   # 以下四个参数控制上下左右四个轴的刻度值的关闭和开启
                   labeltop=False,  # 上轴的刻度值也打开了此时
                   labelbottom=True,
                   labelleft=True,
                   labelright=1,

                   # labelrotation=45,  # 刻度值与坐标轴旋转一定角度

                   grid_color='pink',  # 网格线的颜色，网格线与轴刻度值对应，前提是plt.grid()开启了
                   grid_alpha=1,  # 网格线透明度
                   grid_linewidth=10,  # 网格线宽度
                   grid_linestyle='-',
                   # 网格线线型，{'-', '--', '-.', ':', '',matplotlib.lines.Line2D中的都可以用
                   )
    title_ = title + f'_Fit = {round(mean_lst3[-1], 2)} ~ {round(std_list3[-1], 2)}'
    ax.set_title(title_)  # 设置图名为Simple Plot
    ax.legend()  # 自动检测要在图例中显示的元素，并且显示
    if save_path:
        plt.savefig(save_path)
    plt.show()  # 图形可视化
    print(f'{title}    {xlabel}                       :       {round(mean_lst3[-1])} {round(std_list3[-1])}\n'
          f' {round(mean_lst1[-1])} {round(std_list1[-1])}       \n'
          f' {round(mean_lst2[-1])} {round(std_list2[-1])}')

