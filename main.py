import numpy as np
import matplotlib.pyplot as plt
from config import load_and_clean_data, DATA_PATH_56_5, DATA_PATH_56_7
from plot_observed import plot_observed
from correlation_class import correlation
from noise_quantification import NoiseQuantification, NoiseQuantificationCV
from multi_axis_plot import multi_axis_plot
from outlier_analysis import outlier_analysis
from correlation_heatmap import correlation_heatmap


if __name__ == "__main__":
    # --- Load & clean primary dataset ---
    data = load_and_clean_data(DATA_PATH_56_5)

    # --- 1. Plot observed data ---
    plot_observed(data, start_time=0, end_time=140000)

    # --- 2. Correlation analysis ---
    corr_params = ['N2_RATE', 'VIB_LAT', 'SHK_LAT', 'CIRC_PRS', 'IPRS_RAW', 'APRS_RAW']
    corr = correlation(corr_params)

    start_time = 300 * 60
    end_time = 600 * 60
    corr.corr_slid(data, start_time=start_time, end_time=end_time,
                   time_steps=[2], fig_size=(8, 4), sub_plot_row=2, sub_plot_col=1)

    # --- 3. Time series plot of parameters with N2 RATE ---
    end_time = 2250 * 60
    start_time = 0
    for parameter in corr.parameters:
        if parameter in ('N2_RATE', 'AZIM_RT_RAW'):
            continue
        x = data['SHK_LAT'][start_time:end_time].values
        y = data[parameter][start_time:end_time].values
        fig, ax1 = plt.subplots(4, 1, figsize=(8, 8))
        for idx, ax in enumerate(ax1):
            ax.plot(np.arange(0, len(y), 1) / 60, x)
            ax2 = ax.twinx()
            ax2.plot(np.arange(0, len(y), 1) / 60, y, '-', color='darkorange')
            ax.set_ylabel('SHK_LAT')
            ax2.set_ylabel(parameter)
        xlims = [None, (0, 400), (400, 1200), (1200, 1600)]
        for idx, xl in enumerate(xlims):
            if xl:
                ax1[idx].set_xlim(xl[0], xl[1])
        ax1[-1].set_xlabel('Time (Minutes)')
        fig.suptitle('SHK_LAT with ' + parameter)
        plt.show()

    # --- 4. Noise quantification ---
    corr_all = correlation(corr_params)
    end_time_nq = 6000
    x_vib = data.VIB_LAT[0:end_time_nq].values
    NoiseQuantification(data, corr_all, x=x_vib, time_step=10, end_time=end_time_nq)

    end_time_cv = 135000
    x_shk = data.SHK_LAT[0:end_time_cv].values
    NoiseQuantificationCV(data, corr_all, x=x_shk, time_step=12, end_time=end_time_cv)

    # --- 5. Load second dataset for multi-axis & heatmap ---
    data2 = load_and_clean_data(DATA_PATH_56_7)

    # --- 6. Multi-axis plot ---
    multi_axis_plot(data2)

    # --- 7. Outlier analysis ---
    outlier_analysis(data2, end_time=135000)

    # --- 8. Correlation heatmap ---
    heatmap_params = ['TEMP_DNI_RAW', 'ATEMP_RAW', 'PTEMP_RAW', 'DAGR_Temp']
    correlation_heatmap(data2, heatmap_params)
