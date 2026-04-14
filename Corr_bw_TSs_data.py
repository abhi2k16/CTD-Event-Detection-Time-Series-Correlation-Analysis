import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
#plt.style.use('seaborn')
#%% import data
# Parameter to be analys:N2_rate, Depth, IPRS_RAW,WOB_DH,TOB_DH,CT_WGT,CIRC_PRS,WH_PRS,BVEL
# FLWI, GTF_RAW, VIB_LAT, SHK_LAT,
parameters = ['N2_RATE','APRS_RAW','IPRS_RAW','WOB_DH','TOB_DH','CT_WGT',
              'CIRC_PRS','WH_PRS','BVEL','FLWI','GTF_RT_RAW','VIB_LAT','SHK_LAT'] 
data = pd.read_csv("Pandas_dataframe_O_1011724_56-7.csv")
N2data = data[['TIME','N2_RATE']]
APRS_RAWdata = data[['TIME','APRS_RAW']]
#%% Plot the observed data 
start_time = 0 #In second
end_time = 140000 #In second
fig, axs = plt.subplots(4,3, figsize = (12,9))

axs[0,0].plot(data.APRS_RAW[start_time:end_time])
axs[0,0].set_title('APRS_RAW')

axs[0,1].plot(data.IPRS_RAW[start_time:end_time])
axs[0,1].set_title('IPRS_RAW')

axs[0,2].plot(data.WOB_DH[start_time:end_time])
axs[0,2].set_title('WOB_DH')

axs[1,0].plot(data.TOB_DH[start_time:end_time])
axs[1,0].set_title('TOB_DH')

axs[1,1].plot(data.CT_WGT[start_time:end_time])
axs[1,1].set_title('CT_WGT')

axs[1,2].plot(data.CIRC_PRS[start_time:end_time])
axs[1,2].set_title('CIRC_PRS')

axs[2,0].plot(data.WH_PRS[start_time:end_time])
axs[2,0].set_title('WH_PRS')

axs[2,1].plot(data.BVEL[start_time:end_time])
axs[2,1].set_title('BVEL')

axs[2,2].plot(data.FLWI[start_time:end_time])
axs[2,2].set_title('FLWI')

axs[3,0].plot(data.GTF_RT_RAW[start_time:end_time])
axs[3,0].set_title('GTF_RT_RAW')
axs[3,0].set(xlabel = 'Time (sec)')

axs[3,1].plot(data.VIB_LAT[start_time:end_time])
axs[3,1].set_title('VIB_LAT')
axs[3,1].set(xlabel = 'Time (sec)')

axs[3,2].plot(data['SHK_LAT'][start_time:end_time])
axs[3,2].set_title('SHK_LAT')
axs[3,2].set(xlabel = 'Time (sec)')
plt.subplots_adjust(left=None, bottom=None, right=None,
        top=None, wspace=0.3, hspace=0.3)
# # Hide x labels and tick labels for top plots and y ticks for right plots.
# for ax in axs.flat:
#      ax.label_outer()
plt.savefig('parameter_of_interest.tif')
plt.show()
#%% Data cleaning: fill NaN with adjecent value
for column in data.columns:
    if column in parameters:
        if data[column].isnull().values.any() == True:
            print(column)
            data[column]=data[column].bfill()

#%% Scatter plot of N2 Rate and other parameters data
# normalize all data between [0 and 1]
def normalize_data(x):
    normData = (x-np.min(x))/(np.max(x)-np.min(x))
    return normData
def scatter_plot(n_step, time_step, fig_size, sub_plot_row, sub_plot_col):
    # n_step: # of step
    # time_step : Time in second
    # sub_plot_row : plt.subplots(sub_plot_row,Sub_plot_col, fig_size = (_,_)) 
    # Sub_plot_col :
    time = np.arange(time_step/60,(time_step/60)*n_step+1,time_step/60)
    for i, parameter in enumerate(parameters):
        if parameter == 'N2_RATE':
            pass
        else:
            plt.figure(figsize=fig_size)
            for j in range(n_step):
                x = data.N2_RATE[j*time_step:(j+1)*time_step].values
                y = data[parameter][j*time_step:(j+1)*time_step].values
                norm_x = normalize_data(x)
                norm_y = normalize_data(y)
                plt.subplot(sub_plot_row,sub_plot_col,j+1)
                plt.scatter(norm_x,norm_y,marker=".")
                plt.title(str(int(time[j]))+' minute')
            plt.suptitle(parameter,fontsize=16)
            plt.subplots_adjust(left=None, bottom=None, right=None,
                    top=None, wspace=0.3, hspace=0.3)
            plt.show()
    
scatter_plot(n_step=30, time_step=600, fig_size=(12,9), sub_plot_row=5, sub_plot_col=6)  
#%% Measuring correlation by calculating Pearson Coeficent
n_step = 45 #Nummer of step
time_step = 900 # in second
def corr_plot(n_step,time_step):
    plt.figure(figsize=(12,9))
    for j,parameter in enumerate(parameters):
        if parameter == 'N2_RATE':
            pass
        else:
            corr_coefficients = []
            for i in range(n_step):
                x = N2data.N2_RATE[i*time_step:(i+1)*time_step].values
                y = data[parameter][i*time_step:(i+1)*time_step].values
                correlation_coefficient, p_value = stats.pearsonr(x, y)
                corr_coefficients.append(correlation_coefficient)
            plt.subplot(4,3,j)
            plt.plot(np.arange(time_step/60,(time_step/60)*n_step+1,time_step/60)
                     ,np.array(corr_coefficients),'-')
            plt.title(parameter)
            plt.ylabel('Corr. Coefficient')
    plt.xlabel('time (minute)')
    plt.subplots_adjust(left=None, bottom=None, right=None,
            top=None, wspace=0.3, hspace=0.3)
    #plt.savefig('pearson_corr_5hrs_step_20min.tif')
    plt.show()
corr_plot(n_step=20, time_step=1200)
#%% Measurring Corr. for each parameter with different time step
time_steps = [5,10,15,20]#,30,45]
def corr_plot_param_wise(max_steps, time_steps,fig_size, sub_plot_row, sub_plot_col):
    for i, parameter in enumerate(parameters):
        if parameter == 'N2_RATE':
            pass
        else:
            plt.figure(figsize = fig_size)
            for k,time_step in enumerate(time_steps):                
                corr_coefficients = []
                p_values = []
                n_step = int(max_steps/time_step)
                for j in range(n_step):
                    x = data.N2_RATE[j*time_step*60:(j+1)*time_step*60].values
                    #x = normalize_data(x)
                    y = data[parameter][j*time_step*60:(j+1)*time_step*60].values
                    #y = normalize_data(y)
                    correlation_coefficient, p_value = stats.pearsonr(x, y)
                    #correlation_coefficient, p_value = stats.kendalltau(x, y)
                    corr_coefficients.append(correlation_coefficient)   
                    p_values.append(p_value)
                plt.subplot(sub_plot_row,sub_plot_col,k+1)
                plt.plot(np.arange(time_step,(time_step)*n_step+1,time_step)
                         ,np.array(corr_coefficients),'-')
                plt.ylabel('Corr. Coefficient')
                plt.xlabel('time (minute)')
                plt.title(str(time_step)+' MINUTES')
            plt.suptitle(parameter,fontsize = 16)
            plt.subplots_adjust(left=None, bottom=None, right=None,
                    top=None, wspace=0.3, hspace=0.3)
        plt.show()
corr_plot_param_wise(max_steps=600, time_steps=time_steps, fig_size=(9,6), sub_plot_row=2,sub_plot_col=2)
#%%  Measurring Corr. for each parameter with different time step with slidind time
time_steps = [5,10,15,20]
def corr_param_wise_slid(max_steps,slid_step, time_steps,fig_size, sub_plot_row, sub_plot_col):
    for i, parameter in enumerate(parameters):
        if parameter == 'N2_RATE':
            pass
        else:
            plt.figure(figsize = fig_size)
            for k,time_step in enumerate(time_steps):                
                corr_coefficients = []
                p_values = []
                #n_step = int(max_steps/time_step)
                for j in range(max_steps):
                    x = data.N2_RATE[j*60*slid_step:time_step*60+j*60*slid_step].values
                    y = data[parameter][j*60*slid_step:time_step*60+j*60*slid_step].values
                    correlation_coefficient, p_value = stats.pearsonr(x, y)
                    corr_coefficients.append(correlation_coefficient)   
                    p_values.append(p_value)
                plt.subplot(sub_plot_row,sub_plot_col,k+1)
                plt.plot(corr_coefficients)
                plt.ylabel('Corr. Coefficient')
                plt.xlabel('time (minute)')
                plt.title(str(time_step)+' MINUTES')
            plt.suptitle(parameter,fontsize = 16)
            plt.subplots_adjust(left=None, bottom=None, right=None,
                    top=None, wspace=0.3, hspace=0.3)
        plt.show()
corr_param_wise_slid(max_steps=600,slid_step=0, time_steps=time_steps, fig_size=(9,6), sub_plot_row=2,sub_plot_col=2)
#%%











