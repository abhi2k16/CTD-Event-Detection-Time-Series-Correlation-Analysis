import numpy as np
import matplotlib.pyplot as plt


def outlier_analysis(data, end_time):
    parameters = ['TEMP_DNI_RAW', 'ATEMP_RAW', 'PTEMP_RAW', 'DAGR_Temp']
    lw = 4
    xlims = [(None, None), (-1, 100), (180, 240), (1100, 1250)]
    for parameter in parameters:
        fig, ax1 = plt.subplots(4, 1, figsize=(12, 12))
        y = data[parameter][0:end_time]
        t = np.arange(0, len(y), 1) / 60
        iprs = data.IPRS_RAW[0:end_time]
        for idx, ax in enumerate(ax1):
            ax.plot(t, y, '-', color='darkorange', linewidth=lw if idx > 0 else 2, label=parameter)
            ax.set_ylabel(parameter)
            ax2 = ax.twinx()
            ax2.plot(t, iprs, label='IPRS_RAW')
            ax2.set_ylabel('IPRS_RAW')
            if idx == 0:
                ax2.legend(loc='best')
                ax.legend(loc='center right')
            xl = xlims[idx]
            if xl[0] is not None:
                ax.set_xlim(xl[0], xl[1])
            if idx >= 2:
                ax.set_xlabel('Time (Minute)')
        fig.suptitle(parameter)
        fig.subplots_adjust(wspace=0.3, hspace=0.3)
        plt.show()


if __name__ == "__main__":
    from config import load_and_clean_data, DATA_PATH_56_7
    data = load_and_clean_data(DATA_PATH_56_7)
    outlier_analysis(data, end_time=135000)
