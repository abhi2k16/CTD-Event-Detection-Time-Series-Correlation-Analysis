import matplotlib.pyplot as plt
import seaborn as sns


def correlation_heatmap(data, parameters):
    data1 = data[parameters]
    corr_mat = data1.corr()
    print(corr_mat)
    plt.figure(figsize=(14, 10))
    sns.heatmap(corr_mat, annot=True, cmap='cubehelix', vmin=-1, vmax=1)
    plt.title('Correlation Matrix Heatmap')
    plt.show()


if __name__ == "__main__":
    from config import load_and_clean_data, DATA_PATH_56_7
    data = load_and_clean_data(DATA_PATH_56_7)
    correlation_heatmap(data, ['TEMP_DNI_RAW', 'ATEMP_RAW', 'PTEMP_RAW', 'DAGR_Temp'])
