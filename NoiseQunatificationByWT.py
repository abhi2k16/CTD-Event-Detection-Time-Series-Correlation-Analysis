import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import obspy
from obspy.imaging.cm import obspy_sequential
from obspy.signal.tf_misfit import cwt
#%% import data
# Parameter to be analys:N2_rate, Depth, IPRS_RAW,WOB_DH,TOB_DH,CT_WGT,CIRC_PRS,WH_PRS,BVEL
# FLWI, GTF_RAW, VIB_LAT, SHK_LAT,TEMP_DNI_RAW, ATEMP_RAW, PTEMP_RAW, DAGR_Temp
parameters = ['N2_RATE','APRS_RAW','IPRS_RAW','WOB_DH','TOB_DH','CT_WGT',
              'CIRC_PRS','WH_PRS','BVEL','FLWI','GTF_RT_RAW','VIB_LAT','SHK_LAT',
              'TEMP_DNI_RAW', 'ATEMP_RAW', 'PTEMP_RAW', 'DAGR_Temp'] 
data = pd.read_csv("Pandas_dataframe_O_1011724_56-7.csv")
#%% plot data
vib_signal = data.VIB_LAT[0:135000].values
shk_signal = data.SHK_LAT[0:135000].values
shk_signal_1stDiff = np.diff(shk_signal)
vib_signal_1stDiff = np.diff(vib_signal)
plt.plot(np.arange(0,len(vib_signal_1stDiff),1)/60,shk_signal_1stDiff)
plt.show()
#%% Wavelet transform using 
st = obspy.read()
tr = st[0]
npts = tr.stats.npts
dt = tr.stats.delta
t = np.linspace(0, dt * npts, npts)
f_min = 1
f_max = 50

scalogram = cwt(tr.data, dt, 4, f_min, f_max)

fig = plt.figure()
ax = fig.add_subplot(111)

x, y = np.meshgrid(
    t,
    np.logspace(np.log10(f_min), np.log10(f_max), scalogram.shape[0]))

ax.pcolormesh(x, y, np.abs(scalogram), cmap=obspy_sequential)
ax.set_xlabel("Time after %s [s]" % tr.stats.starttime)
ax.set_ylabel("Frequency [Hz]")
ax.set_yscale('log')
ax.set_ylim(f_min, f_max)
plt.show()
#%%
end_time = 135000
N2_rate = data.N2_RATE[0:end_time].values
vib_signal = data.VIB_LAT[0:end_time].values
shk_signal = data.SHK_LAT[0:end_time].values
shk_signal_1stDiff = np.diff(shk_signal)
vib_signal_1stDiff = np.diff(vib_signal)
dt = 1
t = np.linspace(0, 1,end_time)
f_min =1
f_max =4
scalogram = cwt(vib_signal_1stDiff, dt, 4, f_min, f_max)
#%%
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(211)
ax2 = ax.twinx()
ax.plot(np.arange(0,len(vib_signal),1)/60,vib_signal)
ax2.plot(np.arange(0,len(vib_signal),1)/60,N2_rate,color='darkorange')
ax2.legend(['N2_Rate'], loc = 'upper center')
ax2.set_ylabel('N2 Rate')
ax.set_ylabel('VIB_Lat')
ax2.set_xlim(0,int(end_time)/60)
ax.set_xlim(0,int(end_time)/60)
ax = fig.add_subplot(212)
x, y = np.meshgrid(t*end_time/60,
    np.logspace(np.log10(f_min), np.log10(f_max), scalogram.shape[0]))
WC = np.abs(scalogram)/np.max(np.max(np.abs(scalogram)))
abs_sci = np.abs(scalogram)

ax.pcolormesh(x, y, np.abs(scalogram[:99,:end_time-1]), cmap='gist_ncar')
ax.set_ylabel("Frequency [Hz]")
#ax.set_yscale('log')
ax.set_ylim(f_min, f_max)
ax.set_xlabel('Time (Minute)')
fig.suptitle('VIB_LAT')
plt.show()
#%%