import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


class correlation:
    def __init__(self, parameters):
        self.parameters = parameters

    def normalize_data(self, x):
        return (x - np.min(x)) / (np.max(x) - np.min(x))

    def scatter_plot(self, data, n_step, time_step, fig_size, sub_plot_row, sub_plot_col):
        time = np.arange(time_step / 60, (time_step / 60) * n_step + 1, time_step / 60)
        for parameter in self.parameters:
            if parameter == 'N2_RATE':
                continue
            plt.figure(figsize=fig_size)
            for j in range(n_step):
                x = data.N2_RATE[j * time_step:(j + 1) * time_step].values
                y = data[parameter][j * time_step:(j + 1) * time_step].values
                plt.subplot(sub_plot_row, sub_plot_col, j + 1)
                plt.scatter(self.normalize_data(x), self.normalize_data(y), marker=".")
                plt.title(str(int(time[j])) + ' minute')
            plt.suptitle(parameter, fontsize=16)
            plt.subplots_adjust(wspace=0.3, hspace=0.3)
            plt.show()

    def corr_plot(self, data, n_step, time_step, fig_size):
        plt.figure(figsize=(12, 9))
        for j, parameter in enumerate(self.parameters):
            if parameter == 'N2_RATE':
                continue
            corr_coefficients = []
            for i in range(n_step):
                x = data.N2_RATE[i * time_step:(i + 1) * time_step].values
                y = data[parameter][i * time_step:(i + 1) * time_step].values
                coef, _ = stats.pearsonr(x, y)
                corr_coefficients.append(coef)
            plt.subplot(4, 3, j)
            plt.plot(np.arange(time_step / 60, (time_step / 60) * n_step + 1, time_step / 60),
                     np.array(corr_coefficients), '-')
            plt.title(parameter)
            plt.ylabel('Corr. Coefficient')
        plt.xlabel('time (minute)')
        plt.subplots_adjust(wspace=0.3, hspace=0.3)
        plt.show()

    def corr_param(self, data, max_steps, time_steps, fig_size, sub_plot_row, sub_plot_col):
        for parameter in self.parameters:
            if parameter == 'N2_RATE':
                continue
            plt.figure(figsize=fig_size)
            for k, time_step in enumerate(time_steps):
                corr_coefficients, p_values = [], []
                n_step = int(max_steps / time_step)
                for j in range(n_step):
                    x = data.N2_RATE[j * time_step * 60:(j + 1) * time_step * 60].values
                    y = data[parameter][j * time_step * 60:(j + 1) * time_step * 60].values
                    coef, p = stats.kendalltau(x, y)
                    corr_coefficients.append(coef)
                    p_values.append(p)
                plt.subplot(sub_plot_row, sub_plot_col, k + 1)
                plt.plot(np.arange(time_step, time_step * n_step + 1, time_step),
                         np.array(corr_coefficients), '-')
                plt.ylabel('Corr. Coefficient')
                plt.xlabel('time (minute)')
                plt.title(str(time_step) + ' MINUTES')
            plt.suptitle(parameter, fontsize=16)
            plt.subplots_adjust(wspace=0.3, hspace=0.3)
            plt.show()

    def corr_slid(self, data, start_time, end_time, time_steps, fig_size, sub_plot_row, sub_plot_col):
        for parameter in self.parameters:
            if parameter == 'N2_RATE':
                continue
            fig, axs = plt.subplots(sub_plot_row, sub_plot_col, figsize=fig_size)
            for k, time_step in enumerate(time_steps):
                time_step_sec = time_step * 60
                x_N2Rate = data.N2_RATE[start_time:end_time].values
                corr_coefficients, p_values = [], []
                for j in range(int(len(x_N2Rate[0:end_time - time_step_sec]) / 60)):
                    x = data.N2_RATE[start_time + j * 60:start_time + (j + 1) * 60 + time_step_sec - 60].values
                    y = data[parameter][start_time + j * 60:start_time + (j + 1) * 60 + time_step_sec - 60].values
                    coef, p = stats.spearmanr(x, y)
                    corr_coefficients.append(coef)
                    p_values.append(p)
                axs[k + 1].plot(
                    np.arange(start_time / 60, end_time / 60,
                               ((end_time - start_time) / 60) / len(corr_coefficients)),
                    corr_coefficients)
                axs[k + 1].set_ylabel('Corr. Coefficient')
                z = data[parameter][start_time:end_time]
                axs[k].plot(np.arange(start_time, end_time, 1) / 60, z, label=parameter)
                axs_twin = axs[k].twinx()
                axs_twin.plot(np.arange(start_time, end_time, 1) / 60, x_N2Rate,
                              label='N2_Rate', color='darkorange')
                axs_twin.set_ylabel('N2 rate', color='darkorange')
                axs_twin.legend()
                axs_twin.tick_params(axis='y', colors='darkorange')
                axs_twin.spines['right'].set_color('darkorange')
                axs[k].set_ylabel(parameter)
                axs[k + 1].set_xlabel('time (minute)')
                axs[k].legend()
            fig.suptitle(parameter, fontsize=16)
            plt.show()

    def corr_slid_timeLag(self, data, end_time, time_steps, fig_size, sub_plot_row, sub_plot_col, TimeLags):
        for parameter in self.parameters:
            if parameter == 'N2_RATE':
                continue
            plt.figure(figsize=fig_size)
            for k, time_step in enumerate(time_steps):
                time_step_sec = time_step * 60
                x_N2Rate = data.N2_RATE[0:end_time].values
                all_corrs = [[] for _ in TimeLags]
                for j in range(int(len(x_N2Rate[0:end_time - time_step_sec]) / 60)):
                    for l, timeLag in enumerate(TimeLags):
                        x = data.N2_RATE[j * 60:(j + 1) * 60 + time_step_sec - 60].values
                        y = data[parameter][j * 60 + timeLag * 60:(j + 1) * 60 + time_step_sec - 60 + timeLag * 60].values
                        coef, _ = stats.pearsonr(x, y)
                        all_corrs[l].append(coef)
                plt.subplot(sub_plot_row, sub_plot_col, k + 1)
                for corr_list in all_corrs:
                    plt.plot(corr_list, linewidth=1.5)
                plt.legend(list(map(str, TimeLags)), loc='lower left')
                plt.ylabel('Corr. Coefficient')
                plt.xlabel('time (minute)')
                plt.title(str(time_step) + ' MINUTES')
            plt.suptitle(parameter, fontsize=16)
            plt.subplots_adjust(wspace=0.3, hspace=0.3)
            plt.show()
