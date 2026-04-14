# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%% import data
# Parameter to be analys:N2_rate, Depth, IPRS_RAW,WOB_DH,TOB_DH,CT_WGT,CIRC_PRS,WH_PRS,BVEL
# FLWI, GTF_RAW, VIB_LAT, SHK_LAT,TEMP_DNI_RAW, ATEMP_RAW, PTEMP_RAW, DAGR_Temp
parameters = ['N2_RATE','APRS_RAW','IPRS_RAW','WOB_DH','CT_WGT',
              'CIRC_PRS','WH_PRS','BVEL','FLWI','GTF_RT_RAW','VIB_LAT','SHK_LAT','HDTH',
              'TEMP_DNI_RAW', 'ATEMP_RAW', 'PTEMP_RAW', 'DAGR_Temp','DEPT','INCL_RT_RAW',
              'AZIM_RT_RAW'] 
#data = pd.read_csv("Pandas_dataframe_O_1011724_56-7.csv")
data1 = pd.read_csv("C:/Users/AKumar340/OneDrive - SLB/2024/CTD_EventDetection/Data/O.1011724.56-5.csv")
data2 = pd.read_csv("C:/Users/AKumar340/OneDrive - SLB/2024/CTD_EventDetection/Data/O.1011724.08-5.csv")
data3 = pd.read_csv("C:/Users/AKumar340/OneDrive - SLB/2024/CTD_EventDetection/Data/O.1011724.56-7.csv")
#%% make single dataframe
data = [data1, data2, data3]
data_list = []
for df in data:
    data_list.append(df[['FLWI','WOB_DH','N2_RATE','VIB_LAT','SHK_LAT']])    
data_final= pd.concat(data_list, ignore_index=True)
data_final = data_final[(data_final['FLWI']>1.6*42)&(data_final['FLWI']<2.6*42)
                       &(data_final['WOB_DH']>-0.5)]
#%% scatter plot 
variables = ['VIB_LAT','SHK_LAT']
for var in variables:
    print(var)
    if var == 'VIB_LAT':
        scale = 6
    else:
        scale = 1
    plt.figure(figsize=(15,10))
    plt.subplot(1,2,1)
    points = plt.scatter(data_final.WOB_DH, data_final.FLWI/42, 
                             s=data_final[var]*scale,c=data_final[var],cmap="jet", lw=0)
    plt.colorbar(points)
    plt.xlabel('WOB_DH(kpounds)')
    plt.ylabel('FLWI(bpm)')
    plt.title('WOB Vs FLWI Vs '+var)
    plt.subplot(1,2,2)
    points = plt.scatter(data_final.N2_RATE, data_final.FLWI/42, 
                             s=data_final[var]*scale,c=data_final[var],cmap="jet")
    plt.colorbar(points)
    plt.xlabel('N2_RATE(scf/min)')
    plt.title('N2 Vs FLWI Vs '+var)
plt.show()
#%%
import pandas as pd
import numpy as np
import time

# Create a large DataFrame with 100,000 rows
data = {
    'ID': np.arange(1, 11),
    'Name': ['Person' + str(i) for i in range(1, 11)],
    'Age': np.random.randint(20, 60, size=10)
}

df = pd.DataFrame(data)

# Check the size of the DataFrame
print("DataFrame shape:", df.shape)
#%%
# Using iterrows() to iterate over rows
start_time = time.time()

for index, row in df.iterrows():
    # Perform some operation (e.g., print first 5 values for demonstration)
    if index < 5:
        print(f"ID: {index} {row['ID']}, Name: {row['Name']}, Age: {row['Age']}")
        #print(df['Name'])

elapsed_time = time.time() - start_time
print(f"\nTime taken using iterrows(): {elapsed_time:.4f} seconds")
#%%