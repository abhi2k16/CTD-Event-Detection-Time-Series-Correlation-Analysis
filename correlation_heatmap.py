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
