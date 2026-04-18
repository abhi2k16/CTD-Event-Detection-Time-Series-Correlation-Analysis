import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import spearmanr

DATA_PATH_56_5 = "*/O.1011724.56-5.csv"
DATA_PATH_56_7 = "*/O.1011724.56-7.csv"

parameters = [
    'N2_RATE', 'APRS_RAW', 'IPRS_RAW', 'WOB_DH', 'CT_WGT',
    'CIRC_PRS', 'WH_PRS', 'BVEL', 'FLWI', 'GTF_RT_RAW', 'VIB_LAT', 'SHK_LAT', 'HDTH',
    'TEMP_DNI_RAW', 'ATEMP_RAW', 'PTEMP_RAW', 'DAGR_Temp', 'DEPT', 'INCL_RT_RAW', 'AZIM_RT_RAW'
]


def load_and_clean_data(path):
    data = pd.read_csv(path)
    # Fill NaN with backfill
    for column in data.columns:
        if column in parameters:
            if data[column].isnull().values.any():
                data[column] = data[column].bfill()
    # PTEMP_RAW negative value removal
    for k in data[data['PTEMP_RAW'] < 0].index:
        j = 0
        while data['PTEMP_RAW'][k] < 0:
            k += 1
            j += 1
            if data['PTEMP_RAW'][k] > 0:
                data.loc[k - j, 'PTEMP_RAW'] = data.loc[k, 'PTEMP_RAW']
    # IPRS_RAW negative value removal
    for k in data[data['IPRS_RAW'] < 0].index:
        j = 0
        while data['IPRS_RAW'][k] < 0:
            k += 1
            j += 1
            if data['IPRS_RAW'][k] > 0:
                data.loc[k - j, 'IPRS_RAW'] = data.loc[k, 'IPRS_RAW']
    return data
