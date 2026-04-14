import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import scipy.spatial.distance as dist
from tslearn import metrics
from scipy import signal
#plt.style.use('seaborn')
#%% import data
# Parameter to be analys:N2_rate, Depth, IPRS_RAW,WOB_DH,TOB_DH,CT_WGT,CIRC_PRS,WH_PRS,BVEL
# FLWI, GTF_RAW, VIB_LAT, SHK_LAT,
parameters = ['N2_RATE','APRS_RAW','IPRS_RAW','WOB_DH','TOB_DH','CT_WGT',
              'CIRC_PRS','WH_PRS','BVEL','FLWI','GTF_RT_RAW','VIB_LAT','SHK_LAT'] 
data = pd.read_csv("Pandas_dataframe_O_1011724_56-7.csv")
N2data = data[['TIME','N2_RATE']]
APRS_RAWdata = data[['TIME','APRS_RAW']]
#%% Data cleaning: fill NaN with adjecent value
for column in data.columns:
    if column in parameters:
        if data[column].isnull().values.any() == True:
            #print(column)
            data[column]=data[column].bfill()
#%% Dynamic programming function 
def dp(dist_mat):
    N, M = dist_mat.shape    
    # Initialize the cost matrix
    cost_mat = np.zeros((N + 1, M + 1))
    for i in range(1, N + 1):
        cost_mat[i, 0] = np.inf
    for i in range(1, M + 1):
        cost_mat[0, i] = np.inf
    # Fill the cost matrix while keeping traceback information
    traceback_mat = np.zeros((N, M))
    for i in range(N):
        for j in range(M):
            penalty = [
                cost_mat[i, j],      # match (0)
                cost_mat[i, j + 1],  # insertion (1)
                cost_mat[i + 1, j]]  # deletion (2)
            i_penalty = np.argmin(penalty)
            cost_mat[i + 1, j + 1] = dist_mat[i, j] + penalty[i_penalty]
            traceback_mat[i, j] = i_penalty
    # Traceback from bottom right
    i = N - 1
    j = M - 1
    path = [(i, j)]
    while i > 0 or j > 0:
        tb_type = traceback_mat[i, j]
        if tb_type == 0:
            # Match
            i = i - 1
            j = j - 1
        elif tb_type == 1:
            # Insertion
            i = i - 1
        elif tb_type == 2:
            # Deletion
            j = j - 1
        path.append((i, j))
    # Strip infinity edges from cost_mat before returning
    cost_mat = cost_mat[1:, 1:]
    return (path[::-1], cost_mat)
#%% Univariate Example 
#x = np.array([0, 0, 1, 1, 0, 0, -1, 0, 0, 0, 0])
x = data.N2_RATE[0:9000].values
#y = np.array([0, 0, 0, 0, 1, 1, 0, 0, 0, -1, -0.5, 0, 0])
y = data.APRS_RAW[0:9000].values
# Normalize the x and y data
def normalize_data(x):
    normData = (x-np.min(x))/(np.max(x)-np.min(x))
    return normData
norm_x = normalize_data(x)+0
norm_y = normalize_data(y)+0
norm_x = signal.savgol_filter(x = norm_x, window_length = 100, polyorder = 3)
norm_y = signal.savgol_filter(x = norm_y, window_length = 100, polyorder = 3)
norm_x = norm_x+0
norm_y = norm_y+0
plt.figure(figsize=(6, 4))
plt.plot(np.arange(norm_x.shape[0]), norm_x, "-", c="C3")
plt.plot(np.arange(norm_y.shape[0]), norm_y, "-", c="C0")
plt.show()
#plt.savefig("fig/signals_a_b.pdf")
#%% Distance matrix
N = norm_x.shape[0]
M = norm_y.shape[0]
dist_mat = np.zeros((N, M))
for i in range(N):
    for j in range(M):
        dist_mat[i, j] = abs(norm_x[i] - norm_y[j])
#%% DTW
path, cost_mat = dp(dist_mat)
print("Alignment cost: {:.4f}".format(cost_mat[N - 1, M - 1]))
print("Normalized alignment cost: {:.4f}".format(cost_mat[N - 1, M - 1]/(N + M)))
#%%
plt.figure(figsize=(8, 8))
plt.subplot(221)
plt.title("Distance matrix")
plt.imshow(dist_mat, cmap=plt.cm.CMRmap_r, interpolation="nearest", origin="lower")
plt.xlabel('APRS_RAW [time (sec)]')
plt.ylabel('N2 Rate [time (sec)]')
plt.subplot(222)
plt.title("Cost matrix")
plt.imshow(cost_mat, cmap=plt.cm.CMRmap_r, interpolation="nearest", origin="lower")
x_path, y_path = zip(*path)
plt.plot(y_path, x_path);
#plt.xlabel('N2_Rate time (sec)')
plt.xlabel('APRS_RAW [time (sec)]')
plt.subplot(212)
plt.plot(np.arange(norm_x.shape[0]), norm_x, "-", c="C3")
plt.plot(np.arange(norm_y.shape[0]), norm_y, "-", c="C0")
plt.legend(['N2 Rate','APRS RAW'])
plt.title('Normalized Data')
plt.xlabel('time (sec)')
plt.show()
#%%
plt.figure(figsize=(12,12))
for x_i, y_j in path:
    plt.plot([x_i, y_j], [norm_x[x_i] + 1.5, norm_y[y_j] - 1.5], c="C7")
plt.plot(np.arange(norm_x.shape[0]), norm_x + 1.5, "-o", c="C3")
plt.plot(np.arange(norm_y.shape[0]), norm_y - 1.5, "-o", c="C0")
plt.axis("off")
#%%