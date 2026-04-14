import numpy as np
import matplotlib.pyplot as plt


def multi_axis_plot(data):
    parameters_2 = ['AZIM_RT_RAW', 'INCL_RT_RAW', 'WH_PRS', 'DEPT', 'CT_WGT', 'BVEL', 'GTF_RT_RAW']
    fig, ax1 = plt.subplots(figsize=(20, 10))
    y = np.arange(0, len(data['SHK_LAT']), 1) / 60

    colors = ['blue', 'green', 'red', 'darkorange', 'deeppink', 'brown', 'purple', 'black']
    axes = [ax1]
    ax1.plot(y, data[parameters_2[0]], color=colors[0], alpha=0.9)
    ax1.set_ylabel(parameters_2[0])
    ax1.set_xlabel('Time(Minutes)')

    ax2 = ax1.twinx()
    ax2.plot(y, data['SHK_LAT'], color=colors[1], alpha=0.9)
    ax2.set_ylabel('SHK_LAT', color=colors[1])
    axes.append(ax2)

    offsets = [0, 40, 80, 120, 160, 220, 260]
    labels = [parameters_2[1], parameters_2[2], parameters_2[3], parameters_2[4], parameters_2[5], parameters_2[6]]
    for idx, (label, offset, color) in enumerate(zip(labels, offsets, colors[2:])):
        ax = ax1.twinx()
        ax.plot(y, data[label], color=color, alpha=0.5 if idx % 2 == 0 else 1)
        ax.set_ylabel(label, color=color)
        ax.spines['right'].set_position(('outward', offset))
        ax.spines['right'].set_color(color)
        ax.tick_params(axis='y', colors=color)
        axes.append(ax)

    ax1.tick_params(axis='y', colors=colors[0])
    ax2.spines['right'].set_color(colors[1])
    ax2.tick_params(axis='y', colors=colors[1])
    plt.show()
