# shock dropped zero durring wipertrip activity
import pandas as pd
import matplotlib.pyplot as plt
#motor_data_activity_wipertrip = []
activities = ['wiper trip']
q = 0 # number of dataset
for activity in activities:
    plt.figure(figsize=(20,15))
    for i in range(len(ls_motor_avl)):
        motor_data_activity_wipertrip_current = []
        if q < 5:
            print('Run No: '+str(i))
        #for i in range(2):
            ctd_partitions_motor = []
            ctd_data_plot_motor = []
            for n in range(1):
                run_id = ls_motor_avl[i]
                run_to_process = run_id
                print(run_id)
                ctd_partitions = dataiku.Dataset("ctd_partitions")
                ctd_partitions.add_read_partitions(run_to_process)
                ctd_partitions = ctd_partitions.get_dataframe()
                data = ctd_partitions[['Start Time','End Time','Activity']]
                ctd_partitions_motor.append(data)
                dataset_for_plot = dataiku.Dataset("dataset_for_plots")
                dataset_for_plot.add_read_partitions(run_to_process)
                dataset_for_plot_df = dataset_for_plot.get_dataframe()
                data_m = dataset_for_plot_df[['TIME','VIB_LAT','SHK_LAT','FLWI','N2_RATE','DEPT','DHTH']]
                ctd_data_plot_motor.append(data_m)
            ctd_partitions_motor_df = pd.concat(ctd_partitions_motor,ignore_index = True)
            ctd_data_plot_motor_df = pd.concat(ctd_data_plot_motor, ignore_index = True)
            ctd_data_plot_motor_df = ctd_data_plot_motor_df.reset_index()
            ctd_data_plot_motor_df['TIME'] = pd.to_datetime(ctd_data_plot_motor_df['TIME'])
            ctd_data_plot_motor_df.index = ctd_data_plot_motor_df['TIME']
            activity_motor=ctd_partitions_motor_df[ctd_partitions_motor_df['Activity'] == activity]
            for r,s in activity_motor.iterrows():
                start_time = s['Start Time']
                end_time = s['End Time']
                data_activity = ctd_data_plot_motor_df[start_time:end_time]

            activity_motor_timediff = (activity_motor['End Time'] - activity_motor['Start Time']).dt.total_seconds()
            activity_motor_timediff = activity_motor_timediff.values
            print(ctd_data_plot_motor_df.shape)
            for j in range(ctd_data_plot_motor_df.shape[0]):
                for k in range(activity_motor.shape[0]):
                    if ctd_data_plot_motor_df['TIME'].iloc[j] == activity_motor['Start Time'].iloc[k]:
                        print(f"Match found: ctd_data_plot_motor_df['TIME'].iloc[{j}] == activity_motor['Start Time'].iloc[{k}]")
                        for m in range(int(activity_motor_timediff[k])):
                            if j+m > ctd_data_plot_motor_df.shape[0]:
                                pass
                            elif j+m <= 0:
                                pass
                            else:
                                data_motor = ctd_data_plot_motor_df.loc[j+m-1,['VIB_LAT','SHK_LAT','N2_RATE','FLWI','DEPT','DHTH']].tolist()
                                motor_data_activity_wipertrip_current.append(data_motor)
            wipertrip_plot_data = pd.DataFrame(motor_data_activity_wipertrip_current,columns = ['VIB_LAT','SHK_LAT','N2_RATE','FLWI','DEPT','DHTH'])
            if wipertrip_plot_data['SHK_LAT'].any() == 0.0:
                if (wipertrip_plot_data['SHK_LAT']==0.0).sum() > 0: 
                    q = q+1
                    wipertrip_plot_data = wipertrip_plot_data[wipertrip_plot_data['SHK_LAT']<= 60]
                    plt.subplot(6,1,q)
                    plt.plot(wipertrip_plot_data['SHK_LAT'])
                    plt.title(str(run_id))
                else: 
                    pass
    plt.show()
#motor_data_activity_wipertrip_df = pd.DataFrame(motor_data_activity_wipertrip,columns = ['VIB_LAT','SHK_LAT','N2_RATE','FLWI'])  
# 
#activities = ['drilloff']
activities = ['wiper trip']
def activity_data_plot(activities, p, partitioner_data, main_data):
    n = 0 # number of dataset
    p = p #number of plot upper limit
    q = p-8 #number of plot lower limit
    for activity in activities:
        for i in range(len(ls_turbine_avl)):
            motor_data_activity_wipertrip_current = []
            if i < q:
                pass
            elif i < p:
                #print('Run No: '+str(i))
                ctd_partitions_motor = []
                ctd_data_plot_motor = []
                for j in range(1):
                    run_id = ls_motor_avl[i]
                    run_to_process = run_id
                    print(run_id)
                    ctd_partitions = dataiku.Dataset(partitioner_data)
                    ctd_partitions.add_read_partitions(run_to_process)
                    ctd_partitions = ctd_partitions.get_dataframe()
                    data = ctd_partitions[['Start Time','End Time','Activity']]
                    ctd_partitions_motor.append(data)
                    dataset_for_plot = dataiku.Dataset(main_data)
                    dataset_for_plot.add_read_partitions(run_to_process)
                    dataset_for_plot_df = dataset_for_plot.get_dataframe()
                    data_m = dataset_for_plot_df[['TIME','VIB_LAT','SHK_LAT','FLWI','N2_RATE','DEPT','HDTH','BVEL']]
                    ctd_data_plot_motor.append(data_m)
                ctd_partitions_motor_df = pd.concat(ctd_partitions_motor,ignore_index = True)
                ctd_data_plot_motor_df = pd.concat(ctd_data_plot_motor, ignore_index = True)
                ctd_data_plot_motor_df = ctd_data_plot_motor_df.reset_index()
                ctd_data_plot_motor_df['TIME'] = pd.to_datetime(ctd_data_plot_motor_df['TIME'])
                ctd_data_plot_motor_df.index = ctd_data_plot_motor_df['TIME']
                activity_motor=ctd_partitions_motor_df[ctd_partitions_motor_df['Activity'] == activity]
                #print(activity_motor)
                activity_data_df = pd.DataFrame(columns = ['VIB_LAT','SHK_LAT','FLWI','N2_RATE','DEPT','HDTH','BVEL'])
                activity_data_append = []
                for r,s in activity_motor.iterrows():
                    start_time = s['Start Time']
                    end_time = s['End Time']
                    data_activity = ctd_data_plot_motor_df[start_time:end_time]
                    activity_data_append.append(data_activity)
                if len(activity_data_append) == 0:
                    pass
                else:
                    activity_data_df = pd.concat(activity_data_append,ignore_index = True)
                n = n+1
                #print(activity_data_df)
                activity_data_df = activity_data_df[(activity_data_df['SHK_LAT'] < 300.0)]
                if n == 1:
                    fig, ax1 = plt.subplots(p-q,1, figsize = (20,25))
                ax1[n-1].plot(activity_data_df['SHK_LAT'], color = 'blue',)
                ax1[n-1].set_ylabel('SHK_LAT',color = 'blue')
                ax1[n-1].tick_params(axis = 'y', colors = 'blue')
                ax1[n-1].set_title(str(run_id))
                ax2 = ax1[n-1].twinx()
                ax2.plot(activity_data_df['DEPT'],color = 'green')
                ax2.set_ylabel('DEPT',color = 'green')
                ax2.tick_params(axis = 'y', colors = 'green')
                ax3 = ax1[n-1].twinx()
                ax3.plot(activity_data_df['BVEL'],color = 'red')
                ax3.set_ylabel('BVEL',color = 'red')
                ax3.tick_params(axis = 'y', colors = 'red')
                ax3.spines['right'].set_position(('outward',60))
        plt.show()   
#%%
import pandas as pd
import numpy as np

# Sample DataFrame
data = {
    'A': [100, 200, 3000, -6000, 700, 800, 9000, -12000, 500, 4500],
    'B': [50, -1000, 500, 7000, -800, 12000, 300, -5000, 400, -9000],
    'C': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # No outliers
}
df = pd.DataFrame(data)

# Specify the columns to check for outliers
columns_to_check = ['A']

# Replace values greater than 5000 or less than -5000 with NaN in the specified columns
df[['A']] = df[['A']].mask((df[['A']] > 5000) | (df[['A']] < -5000))

# Display the updated DataFrame
print(df)
#%%           
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sample DataFrame
data = {
    'x': range(10),
    'y': [5, 15, 25, 35, 8, 50, 55, 20, 30, 45]
}
df = pd.DataFrame(data)

# Define the color conditions
# For example: Red for y < 20, Green for 20 <= y <= 40, and Blue for y > 40
colors = np.where(df['y'] < 20, 'red', np.where(df['y'] <= 40, 'green', 'blue'))

# Plot the data with different colors based on the value ranges
plt.scatter(df['x'], df['y'], color=colors)

# Add labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Plot with Different Value Ranges in Different Colors')

# Show the plot
plt.show()
for condition, color in [((df['y'] < 20), 'red'), 
                         ((df['y'] <= 40) & (df['y'] >= 20), 'green'), 
                         (df['y'] > 40, 'blue')]:
    plt.plot(df['x'][condition], df['y'][condition], color=color)

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Line Plot with Different Value Ranges in Different Colors')
plt.show()

#####################################################################################
# sort the jobs_id number in order of shock/vib. label
def sort_jobid_vib_level(activities, partitioner_data, main_data, parameter, run_type_data):
    # Activity wise data plot for multiple jobs at a time
    # parameter : VIB_LAT/SHK_LAT
    # partitioner_data : Dataset after partition
    # main data : non-partition data
    # run_type : ls_motor_avl/ls_turbine_avl for motor/turbine.[eg. ls_motor_avl is the list of jobs id for motor]
    sorted_job_id = []
    for activity in activities:
        for i in range(len(run_type_data)):
            #print('Run No: '+str(i))
            ctd_partitions_motor = []
            ctd_data_plot_motor = []
            for j in range(1):
                run_id = run_type_data[i]
                run_to_process = run_id
                #print(run_id)
                ctd_partitions = dataiku.Dataset(partitioner_data)
                ctd_partitions.add_read_partitions(run_to_process)
                ctd_partitions = ctd_partitions.get_dataframe()
                data = ctd_partitions[['Start Time','End Time','Activity']]
                ctd_partitions_motor.append(data)
                dataset_for_plot = dataiku.Dataset(main_data)
                dataset_for_plot.add_read_partitions(run_to_process)
                dataset_for_plot_df = dataset_for_plot.get_dataframe()
                data_m = dataset_for_plot_df[['TIME','VIB_LAT','SHK_LAT','FLWI','N2_RATE','DEPT','HDTH','BVEL',
                                             'WOB_DH_CALC']]
                ctd_data_plot_motor.append(data_m)
            ctd_partitions_motor_df = pd.concat(ctd_partitions_motor,ignore_index = True)
            ctd_data_plot_motor_df = pd.concat(ctd_data_plot_motor, ignore_index = True)
            ctd_data_plot_motor_df = ctd_data_plot_motor_df.reset_index()
            ctd_data_plot_motor_df['TIME'] = pd.to_datetime(ctd_data_plot_motor_df['TIME'])
            ctd_data_plot_motor_df.index = ctd_data_plot_motor_df['TIME']
            activity_motor=ctd_partitions_motor_df[ctd_partitions_motor_df['Activity'] == activity]
            #print(activity_motor)
            activity_data_df = pd.DataFrame(columns = ['VIB_LAT','SHK_LAT','FLWI','N2_RATE','DEPT','HDTH','BVEL',
                                                      'WOB_DH_CALC'])
            activity_data_append = []
            for r,s in activity_motor.iterrows():
                start_time = s['Start Time']
                end_time = s['End Time']
                data_activity = ctd_data_plot_motor_df[start_time:end_time]
                activity_data_append.append(data_activity)
            if len(activity_data_append) == 0:
                pass
            else:
                activity_data_df = pd.concat(activity_data_append,ignore_index = True)
            if parameter == 'SHK_LAT':
                    activity_data_df[[parameter]] = activity_data_df[['SHK_LAT']].mask(
                        (activity_data_df[parameter] > 300.0))
            elif parameter == 'VIB_LAT':
                activity_data_df[[parameter]] = activity_data_df[[parameter]].mask(
                    (activity_data_df[parameter] > 50.0))
                if (activity_data_df[parameter] > 20).any():
                    print(run_to_process)
                    sorted_job_id.append(run_to_process)
    print(len(sorted_job_id))
    return sorted_job_id
###################################################################################################################################
def activity_data_plot(activities, p, partitioner_data, main_data, parameter, run_type_data):
    # Activity wise data plot for multiple jobs at a time
    # parameter : VIB_LAT/SHK_LAT
    # partitioner_data : Dataset after partition
    # main data : non-partition data
    # run_type : ls_motor_avl/ls_turbine_avl for motor/turbine.[eg. ls_motor_avl is the list of jobs id for motor]
    n = 0
    p = p #number of plot upper limit
    q = p-5 #number of plot lower limit
    for activity in activities:
        for i in range(len(run_type_data)):
            if i < q:
                pass
            elif i < p:
                #print('Run No: '+str(i))
                ctd_partitions_motor = []
                ctd_data_plot_motor = []
                for j in range(1):
                    run_id = run_type_data[i]
                    run_to_process = run_id
                    print(run_id)
                    ctd_partitions = dataiku.Dataset(partitioner_data)
                    ctd_partitions.add_read_partitions(run_to_process)
                    ctd_partitions = ctd_partitions.get_dataframe()
                    data = ctd_partitions[['Start Time','End Time','Activity']]
                    ctd_partitions_motor.append(data)
                    dataset_for_plot = dataiku.Dataset(main_data)
                    dataset_for_plot.add_read_partitions(run_to_process)
                    dataset_for_plot_df = dataset_for_plot.get_dataframe()
                    data_m = dataset_for_plot_df[['TIME','VIB_LAT','SHK_LAT','FLWI','N2_RATE','DEPT','HDTH','BVEL',
                                                 'WOB_DH_CALC']]
                    ctd_data_plot_motor.append(data_m)
                ctd_partitions_motor_df = pd.concat(ctd_partitions_motor,ignore_index = True)
                ctd_data_plot_motor_df = pd.concat(ctd_data_plot_motor, ignore_index = True)
                ctd_data_plot_motor_df = ctd_data_plot_motor_df.reset_index()
                ctd_data_plot_motor_df['TIME'] = pd.to_datetime(ctd_data_plot_motor_df['TIME'])
                ctd_data_plot_motor_df.index = ctd_data_plot_motor_df['TIME']
                activity_motor=ctd_partitions_motor_df[ctd_partitions_motor_df['Activity'] == activity]
                #print(activity_motor)
                activity_data_df = pd.DataFrame(columns = ['VIB_LAT','SHK_LAT','FLWI','N2_RATE','DEPT','HDTH','BVEL',
                                                          'WOB_DH_CALC'])
                activity_data_append = []
                for r,s in activity_motor.iterrows():
                    start_time = s['Start Time']
                    end_time = s['End Time']
                    data_activity = ctd_data_plot_motor_df[start_time:end_time]
                    activity_data_append.append(data_activity)
                if len(activity_data_append) == 0:
                    pass
                else:
                    activity_data_df = pd.concat(activity_data_append,ignore_index = True)
                activity_data_df[['WOB_DH_CALC']] = activity_data_df[['WOB_DH_CALC']].mask(
                    (activity_data_df[['WOB_DH_CALC']] > 5000) | (activity_data_df[['WOB_DH_CALC']] < -5000))
                n = n+1
                if n == 1:
                    fig, ax1 = plt.subplots(p-q,1, figsize = (18,23))
                if parameter == 'SHK_LAT':
                    activity_data_df[[parameter]] = activity_data_df[['SHK_LAT']].mask(
                        (activity_data_df[parameter] > 300.0)|
                        (activity_data_df[parameter] < 5.0))
                    for condition, color in [((activity_data_df[parameter] < 50), 'lime'),
                        ((activity_data_df[parameter] > 50), 'blue'),
                        ((activity_data_df[parameter] > 100), 'aqua')]:
                        ax1[0].plot(activity_data_df[parameter][condition],'.', color =  color)
                elif parameter == 'VIB_LAT':
                    activity_data_df[[parameter]] = activity_data_df[['VIB_LAT']].mask(
                        (activity_data_df[parameter] > 50.0))
                    for condition, color in [((activity_data_df[parameter] < 10), 'lime'),
                            ((activity_data_df[parameter] > 10), 'blue'),
                            ((activity_data_df[parameter] > 15), 'aqua')]:
                        ax1[n-1].plot(activity_data_df[parameter][condition],'.', color =  color)
                ax1[n-1].set_ylabel(parameter)
                #ax1[n-1].set_ylabel(parameter,color =  color)
                #ax1[n-1].tick_params(axis = 'y', colors =  color)
                ax1[n-1].set_title(run_id)
                ax2 = ax1[n-1].twinx()
                ax2.plot(activity_data_df['DEPT'],color = 'green')
                ax2.set_ylabel('DEPT(ft)',color = 'green')
                ax2.tick_params(axis = 'y', colors = 'green')
                ax3 = ax1[n-1].twinx()
                ax3.plot(activity_data_df['BVEL'],color = 'red')
                ax3.set_ylabel('BVEL(ft/min)',color = 'red')
                ax3.tick_params(axis = 'y', colors = 'red')
                ax3.spines['right'].set_position(('outward',60))
                ax4 = ax1[n-1].twinx()
                ax4.plot(activity_data_df['FLWI']/42,color = 'xkcd:plum')
                ax4.set_ylabel('FLWI(bpm)',color = 'xkcd:plum')
                ax4.tick_params(axis = 'y', colors = 'xkcd:plum')
                ax4.spines['right'].set_position(('outward',120))
                ax5 = ax1[n-1].twinx()
                ax5.plot(activity_data_df['WOB_DH_CALC']/1000,color = 'xkcd:magenta')
                ax5.set_ylabel('WOB_DH(klbf)',color = 'xkcd:magenta')
                ax5.tick_params(axis = 'y', colors = 'xkcd:magenta')
                ax5.spines['right'].set_position(('outward',180))
        plt.show()

# extract the job_id which contains particular activity [eg., wiper trip]
def job_id_with_activity(activity, partitioner_data, run_type_data):
    jobID_with_activity = []
    for job_id in enumerate(run_type_data):
        run_to_process = run_id
        #print(run_id)
        ctd_partitions = dataiku.Dataset(partitioner_data)
        ctd_partitions.add_read_partitions(run_to_process)
        ctd_partitions = ctd_partitions.get_dataframe()
        data = ctd_partitions[['Start Time','End Time','Activity']]
        if (data['Activity'] == 'wiper trip').any():
            jobID_with_activity.append(job_id)
    return jobID_with_activity
#%% ######################################################################
def POOH_tooface_differece(activity, main_data, partitioner_data, job_id):
    """
    activity : 'wiper trip' etc
    main_data : unpartitioned data
    partitioner_data: data after partitioner
    """
    POOH_data_all = pd.DataFrame()
    partition_data_append = []
    main_data_append = []
    partition_data = dataiku.Dataset(partition_data)
    partition_data.add_read_partitions(job_id)
    partition_data = partition_data.get_dataframe()
    partition_data = partitioner_data[['Start Time','End Time','Activity']]
    partition_data_append.append(partition_data)
    partitioner_data_df = pd.concat(partition_data_append, ignore_index= False)
    main_data = dataiku.Dataset(main_data)
    main_data.add_read_partitions(job_id)
    main_data = main_data.get_dataframe()
    main_data = main_data[['TIME','VIB_LAT','SHK_LAT','FLWI','N2_RATE','DEPT','HDTH','BVEL','WOB_DH_CALC','DIFFPRES','APRS_RAW','IPRS_RAW','GTF_RT_RAW']]
    main_data_append.append(main_data)
    main_data = pd.concat(main_data_append, ignore_index= False)
    drilloff_endindices = []
    POOH_endindices = []
    RIH_endindices  = []
    activity_data = partitioner_data_df[partitioner_data_df['Activity'] == activity]
    for r,s in activity_data.iterrows():
        drilloff_endtime = s['Start Time'] - pd.Timedelta(seconds=1)
        drilloff_endindex = main_data[main_data['TIME'] == str(drilloff_endtime)].index[0]
        drilloff_endindices.append(drilloff_endindex)
        activity_endtime = s['End Time']
        activity_endindex = main_data[main_data['TIME'] == str(activity_endtime)].index[0]
        n = 0
        while main_data['BVEL'][drilloff_endindex+n] <= 0:
            n += 1
        POOH_endindex = drilloff_endindex + n -1
        POOH_endindices.append(POOH_endindex)
        if main_data['BVEL'][activity_endindex] >= 0:
            RIH_endindex = activity_endindex
            RIH_endindices.append(RIH_endindex)
    drilling_data = main_data[abs(main_data['HDTH'] - main_data['DEPT']) < 0.5]
    fig, ax1 = plt.subplots(len(drilloff_endindices),1, figsize = (15,15))
    for i,drilloff_endindex in enumerate(drilloff_endindices):
        POOH_data = main_data.iloc[drilloff_endindex:POOH_endindices[i]]
        drilling_data4POOH = drilling_data[(drilling_data['DEPT'] >= main_data['DEPT'].iloc[POOH_endindices[i]])
                                        &(drilling_data['DEPT'] <= main_data['DEPT'].iloc[drilloff_endindices[i]])]
        POOH_data = POOH_data[POOH_data['DEPT'] >= drilling_data4POOH['DEPT'].min()]
        drilling_data4POOH_downsample = pd.DataFrame()
        temp_data_POOH_append = []
        for j in range(len(POOH_data['DEPT'])):
            temp_data_POOH = drilling_data4POOH.iloc[(drilling_data4POOH['DEPT'] - POOH_data['DEPT'].iloc[j]).abs().argsort()[:1]]
            temp_data_POOH_append.append(temp_data_POOH)
        if len(temp_data_POOH_append) == 0:
            pass
        else:
            drilling_data4POOH_downsample = pd.concat(temp_data_POOH_append, ignore_index=False) 
        delta_toolface_POOH = []
        for j in range(len(POOH_data)):
            temp_delta_toolface1 = abs(POOH_data['GTF_RT_RAW'].iloc[j] - drilling_data4POOH_downsample['GTF_RT_RAW'].iloc[j])
            temp_delta_toolface2 = abs(POOH_data['GTF_RT_RAW'].iloc[j] - drilling_data4POOH_downsample['GTF_RT_RAW'].iloc[j] + 360) 
            temp_delta_toolface3 = abs(POOH_data['GTF_RT_RAW'].iloc[j] - drilling_data4POOH_downsample['GTF_RT_RAW'].iloc[j] - 360)
            delta_toolface_POOH.append(min(temp_delta_toolface1,temp_delta_toolface2, temp_delta_toolface3))
        delta_toolface_POOH_data = pd.DataFrame(delta_toolface_POOH,columns=['POOH_TF_DIFF'])  
        delta_toolface_POOH_data = delta_toolface_POOH_data.reset_index()
        delta_toolface_POOH_data.index = POOH_data.index
        POOH_data['POOH_TF_DIFF'] = delta_toolface_POOH_data['POOH_TF_DIFF']
        POOH_data_all = pd.concat([POOH_data_all, POOH_data], axis=0, ignore_index= False)
        ax1[i].plot(POOH_data['DEPT'],'r')
        ax1[i].set_ylabel('POOH Depth(ft)', color = 'red')
        ax1[i].tick_params(axis = 'y', color = 'red')
        ax1[i].set_xlabel('Time(s)')
        ax2 = ax1[i].twinx()
        ax2.plot(delta_toolface_POOH_data['POOH_TF_DIFF'],'b')
        ax2.set_ylabel('TF_DIFF(degree)', color = 'blue')
        ax2.tick_params(axis = 'y', colors = 'blue')
        ax2.grid(True)
        #ax2.spines['right'].set_position(('outward',60))
        ax3 = ax1[i].twinx()
        ax3.plot(POOH_data['VIB_LAT'],'green')
        ax3.set_ylabel('VIB_LAT(g)', color = 'green')
        ax3.tick_params(axis = 'y', colors = 'green')
        ax3.spines['right'].set_position(('outward',50))
        ax4 = ax1[i].twinx()
        ax4.plot(POOH_data['IPRS_RAW'],'xkcd:goldenrod')
        ax4.set_ylabel('Internal Press(psi)', color = 'xkcd:goldenrod')
        ax4.tick_params(axis = 'y', colors = 'xkcd:goldenrod')
        ax4.spines['right'].set_position(('outward',100))
    plt.show()
    print(drilloff_endindices,POOH_endindices,RIH_endindices)
    #return POOH_data_all