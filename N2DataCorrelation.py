import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#plt.style.use('seaborn')
from statsmodels.graphics.tsaplots import plot_acf, acf, plot_pacf
import statsmodels.api as sm
#%% import data
data = pd.read_csv("Pandas_dataframe_O_1011724_56-7.csv")
N2data = data[['TIME','N2_RATE']]
plt.plot(np.log10(data.APRS_RAW[3600:14400]))
plt.plot(np.log10(N2data['N2_RATE'][3600:14400]))
plt.show()
#%% Plot seasonality, trends, and residual of data
from statsmodels.tsa.seasonal import seasonal_decompose
series = N2data["N2_RATE"][3600:14400]
results = seasonal_decompose(series, model = 'additive', period =100)
results.plot()
plt.show()
#%% differenciate the seasonal, trends, and residual data
plot_acf(results.seasonal, lags= 100)
plt.show()
#%% Stationarity: Take first difference of this series
N2dta_first_diff = series.values[1:]-series.values[:-1]
plt.plot(N2dta_first_diff)
plt.show()
plot_acf(N2dta_first_diff, lags= 100)
plt.show()
#%% Estimating auto-correlation for segmented data
N2data_Segment = N2data['N2_RATE'][3600:14400]
# print(acf_samples)
#plot_acf(N2data['N2_RATE'][0:3000])
#plt.show()
fig, ax = plt.subplots(6,3, figsize = (18,12))
for i,ax in zip(range(18),ax.ravel()):
    sm.graphics.tsa.plot_acf(N2data_Segment[0:0+(i+1)*600], lags=100, ax=ax,
                            title= 'Autcorrelation for 1st '+ str((i+1)*10) +' minute' )
    #sm.graphics.tsa.plot_acf(N2data_Segment[0+i*600:0+(i+1)*600], lags=100, ax=ax,
    #                       title= 'Autcorr. from '+str(60+i*10) +' to ' +str(60+(i+1)*10) +' minute' )
    plt.subplots_adjust(left=None, bottom=0, right=None,
            top=None, wspace=None, hspace=0.3)
#plt.savefig('Autocorrelation for N2_Rate 1st_diff data segemented time')
plt.show()
#%% Autocovariance
data = N2data['N2_RATE'][0:900]
auto_covariance = np.correlate(data-data.mean(), data-data.mean(), mode='full')
positive_lag = np.arange(len(data))
auto_covariance = auto_covariance[len(data)-1:]
#print(auto_covarience)
#plot autocovariance
lags = np.arange(1, len(auto_covariance) + 1)
plt.stem(lags[0:25], auto_covariance[0:25], use_line_collection=True)
plt.xlabel('Lag')
plt.ylabel('Auto-covariance')
plt.title('Auto-covariance Plot with Lag')
plt.grid(True)
plt.show()
#%%



