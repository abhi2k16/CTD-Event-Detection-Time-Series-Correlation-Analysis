import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.spatial.distance import jensenshannon


def QuartileCOD(x):
    x = sorted(x)
    q1, q3 = np.percentile(x, [23, 75])
    return (q3 - q1) / (q1 + q3)


def Coeff_ofvariance(x):
    return np.std(x) / np.mean(x)


def NoiseQuantification(data, corr_obj, x, time_step, end_time):
    x_noise = x
    y = data.N2_RATE[0:end_time].values
    y_norm = corr_obj.normalize_data(y)
    x_noisless = signal.savgol_filter(x_noise, window_length=200, polyorder=3)
    plt.figure(figsize=(8, 6))
    plt.subplot(311)
    plt.plot(np.arange(0, len(x_noise), 1) / 60, corr_obj.normalize_data(x_noise))
    plt.plot(np.arange(0, len(x_noise), 1) / 60, corr_obj.normalize_data(x_noisless))
    plt.plot(np.arange(0, len(y_norm), 1) / 60, y_norm)
    plt.ylabel('Normalized Scale')
    plt.legend(['Noisy data', 'Filtered data', 'N2 Rate'])
    p_correlations, d_jensenshannons = [], []
    for i in range(int(len(x_noise[0:end_time - time_step]) / 60)):
        x_noise_seg = x_noise[i * 60:(i + 1) * 60 + time_step]
        x_noisless_seg = x_noisless[i * 60:(i + 1) * 60 + time_step]
        p_correlations.append(signal.correlate(x_noise_seg, x_noisless_seg))
        d_jensenshannons.append(jensenshannon(x_noise_seg, x_noisless_seg))
    plt.subplot(312)
    plt.plot(np.arange(5, len(p_correlations) + 5, 1), np.array(p_correlations))
    plt.ylabel('Corr Coefficient')
    plt.subplot(313)
    plt.plot(np.arange(5, len(p_correlations) + 5, 1), np.array(d_jensenshannons))
    plt.ylabel('JS Divergence')
    plt.xlabel('Time (Minute)')
    plt.suptitle('VIB_LAT')
    plt.show()


def NoiseQuantificationCV(data, corr_obj, x, time_step, end_time):
    x_noise = x
    y = data.N2_RATE[0:end_time].values
    y_norm = corr_obj.normalize_data(y)
    y_iprs_norm = corr_obj.normalize_data(data.IPRS_RAW[0:end_time])
    x_noisless = signal.savgol_filter(x_noise, window_length=200, polyorder=3)
    plt.figure(figsize=(12, 9))
    plt.subplot(411)
    plt.plot(np.arange(0, len(y_norm), 1) / 60, y_norm)
    plt.plot(np.arange(0, len(x_noise), 1) / 60, corr_obj.normalize_data(x_noise))
    plt.plot(np.arange(0, len(x_noise), 1) / 60, corr_obj.normalize_data(x_noisless))
    plt.ylabel('Normalized Scale')
    plt.legend(['N2 Rate', 'Noisy data', 'Filtered data'], loc='best')
    Coeff_ofvar_noise, Coeff_ofvar_noiseless = [], []
    for i in range(int(len(x_noise[0:end_time - time_step]) / 60)):
        x_noise_seg = x_noise[i * 60:(i + 1) * 60 + time_step]
        x_noisless_seg = x_noisless[i * 60:(i + 1) * 60 + time_step]
        Coeff_ofvar_noise.append(QuartileCOD(x=x_noise_seg))
        Coeff_ofvar_noiseless.append(QuartileCOD(x=x_noisless_seg))
    plt.subplot(412)
    plt.plot(np.arange(5, len(Coeff_ofvar_noise) + 5, 1), np.array(Coeff_ofvar_noise))
    plt.plot(np.arange(5, len(Coeff_ofvar_noiseless) + 5, 1), np.array(Coeff_ofvar_noiseless))
    plt.plot(np.arange(0, len(y_norm), 1) / 60, y_iprs_norm)
    plt.ylabel('Coeff of Var.')
    plt.xlabel('Time (Minute)')
    plt.subplot(413)
    plt.plot(np.arange(0, len(y_norm), 1) / 60, y_norm)
    plt.plot(np.arange(5, len(Coeff_ofvar_noise) + 5, 1), np.array(Coeff_ofvar_noise))
    plt.plot(np.arange(5, len(Coeff_ofvar_noiseless) + 5, 1), np.array(Coeff_ofvar_noiseless))
    plt.legend(['N2 Rate', 'COV'])
    plt.ylabel('Coeff of Var.')
    plt.xlabel('Time (Minute)')
    plt.xlim(450, 700)
    plt.subplot(414)
    plt.plot(np.arange(0, len(y_norm), 1) / 60, y_norm)
    plt.plot(np.arange(5, len(Coeff_ofvar_noise) + 5, 1), np.array(Coeff_ofvar_noise))
    plt.plot(np.arange(5, len(Coeff_ofvar_noiseless) + 5, 1), np.array(Coeff_ofvar_noiseless))
    plt.legend(['N2 Rate', 'COV'])
    plt.ylabel('Coeff of Var.')
    plt.xlabel('Time (Minute)')
    plt.xlim(0, 400)
    plt.ylim(0, 0.7)
    plt.suptitle('VIB_LAT')
    plt.show()
