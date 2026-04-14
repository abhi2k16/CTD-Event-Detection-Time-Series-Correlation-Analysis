import matplotlib.pyplot as plt


def plot_observed(data, start_time=0, end_time=140000):
    fig, axs = plt.subplots(4, 4, figsize=(14, 10))
    cols = [
        ('APRS_RAW', axs[0, 0]), ('IPRS_RAW', axs[0, 1]),
        ('WOB_DH', axs[0, 2]), ('AZIM_RT_RAW', axs[0, 3]),
        ('CT_WGT', axs[1, 0]), ('CIRC_PRS', axs[1, 1]),
        ('WH_PRS', axs[1, 2]), ('BVEL', axs[1, 3]),
        ('FLWI', axs[2, 0]), ('GTF_RT_RAW', axs[2, 1]),
        ('VIB_LAT', axs[2, 2]), ('SHK_LAT', axs[2, 3]),
        ('TEMP_DNI_RAW', axs[3, 0]), ('ATEMP_RAW', axs[3, 1]),
        ('PTEMP_RAW', axs[3, 2]), ('DAGR_Temp', axs[3, 3]),
    ]
    for col, ax in cols:
        ax.plot(data[col][start_time:end_time])
        ax.set_title(col)
    axs[3, 2].set(xlabel='Time (sec)')
    plt.subplots_adjust(wspace=0.3, hspace=0.3)
    plt.show()


if __name__ == "__main__":
    from config import load_and_clean_data, DATA_PATH_56_5
    data = load_and_clean_data(DATA_PATH_56_5)
    plot_observed(data, start_time=0, end_time=140000)
