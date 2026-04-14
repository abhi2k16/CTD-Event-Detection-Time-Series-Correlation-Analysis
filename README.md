# CTD Event Detection — Time Series Correlation Analysis

This project analyses correlations between N2 rate and downhole drilling parameters (vibration, shock, pressure, temperature, etc.) from CTD (Coiled Tubing Drilling) sensor data.

---

## Project Structure

```
ProgramFile/
├── main.py                          # Single entry point — runs the full pipeline
├── config.py                        # Shared config: parameters, data paths, data loader
├── plot_observed.py                 # Observed data overview plot
├── correlation_class.py             # correlation class with all correlation methods
├── noise_quantification.py          # Noise analysis functions (CV, JS divergence)
├── multi_axis_plot.py               # Multi-axis overlaid time series plot
├── outlier_analysis.py              # Outlier analysis: temperature vs IPRS_RAW
├── correlation_heatmap.py           # Seaborn correlation matrix heatmap
├── Corr_bw_TSs_data_class.py        # Original monolithic script (source file)
├── Corr_bw_TSs_data.py              # Earlier version with standalone functions
├── corr_mesurment_DTW_DynamicProg.py# DTW-based correlation measurement
├── FilterDesign_1.py                # Butterworth & Savitzky-Golay filter design demo
├── HMM_N2dataeventdetection.py      # Hidden Markov Model for N2 rate event detection
├── N2DataCorrelation.py             # N2 rate autocorrelation and seasonal decomposition
├── NoiseQunatificationByWT.py       # Noise quantification using Wavelet Transform (CWT)
├── scatter_Plot_ForChannelParam.py  # Scatter plots across multiple datasets + Dataiku utils
└── trial_codes.py                   # Experimental/trial code snippets and Dataiku workflows
```

---

## Modular Files (Refactored from `Corr_bw_TSs_data_class.py`)

### `main.py`
Single executable entry point. Runs the full pipeline in sequence:
1. Loads and cleans data
2. Plots observed parameters
3. Runs sliding window correlation analysis
4. Plots time series comparisons
5. Runs noise quantification
6. Generates multi-axis plot
7. Runs outlier analysis
8. Generates correlation heatmap

**Run with:**
```bash
python main.py
```

---

### `config.py`
Shared configuration used across all modules.

- `parameters` — list of all sensor channel names to analyse
- `DATA_PATH_56_5`, `DATA_PATH_56_7` — paths to the two CSV datasets
- `load_and_clean_data(path)` — loads CSV, backfills NaN values, removes negative values in `PTEMP_RAW` and `IPRS_RAW`

---

### `plot_observed.py`
Plots a 4×4 grid of all key parameters over a specified time window.

**Function:** `plot_observed(data, start_time=0, end_time=140000)`

| Argument | Description |
|---|---|
| `data` | Pandas DataFrame |
| `start_time` | Start index in seconds |
| `end_time` | End index in seconds |

---

### `correlation_class.py`
Contains the `correlation` class for computing and visualising correlations between N2 rate and other parameters.

**Methods:**

| Method | Description |
|---|---|
| `normalize_data(x)` | Min-max normalises a 1D array |
| `scatter_plot(data, n_step, time_step, fig_size, sub_plot_row, sub_plot_col)` | Scatter plots of N2 rate vs each parameter per time window |
| `corr_plot(data, n_step, time_step, fig_size)` | Pearson correlation coefficient over time |
| `corr_param(data, max_steps, time_steps, fig_size, sub_plot_row, sub_plot_col)` | Kendall-tau correlation for multiple time step sizes |
| `corr_slid(data, start_time, end_time, time_steps, fig_size, sub_plot_row, sub_plot_col)` | Sliding window Spearman correlation with dual-axis time series |
| `corr_slid_timeLag(data, end_time, time_steps, fig_size, sub_plot_row, sub_plot_col, TimeLags)` | Pearson correlation with multiple time lags |

---

### `noise_quantification.py`
Functions for quantifying signal noise using statistical and signal processing methods.

| Function | Description |
|---|---|
| `QuartileCOD(x)` | Quartile Coefficient of Dispersion (robust noise measure) |
| `Coeff_ofvariance(x)` | Standard Coefficient of Variation (std/mean) |
| `NoiseQuantification(data, corr_obj, x, time_step, end_time)` | Noise vs filtered signal comparison using cross-correlation and Jensen-Shannon divergence |
| `NoiseQuantificationCV(data, corr_obj, x, time_step, end_time)` | Noise quantification using QCoD across sliding windows |

---

### `multi_axis_plot.py`
Plots multiple drilling parameters on a single figure with independent y-axes (twin axes with outward offsets).

**Function:** `multi_axis_plot(data)`

Parameters plotted: `AZIM_RT_RAW`, `SHK_LAT`, `INCL_RT_RAW`, `WH_PRS`, `DEPT`, `CT_WGT`, `BVEL`, `GTF_RT_RAW`

---

### `outlier_analysis.py`
Plots temperature-related parameters (`TEMP_DNI_RAW`, `ATEMP_RAW`, `PTEMP_RAW`, `DAGR_Temp`) against `IPRS_RAW` at multiple zoom levels to identify outliers.

**Function:** `outlier_analysis(data, end_time)`

---

### `correlation_heatmap.py`
Computes and visualises a Pearson correlation matrix as a seaborn heatmap.

**Function:** `correlation_heatmap(data, parameters)`

---

## Other Scripts

### `Corr_bw_TSs_data_class.py`
Original monolithic script. All logic has been refactored into the modular files above. Kept as reference.

---

### `Corr_bw_TSs_data.py`
Earlier version of the correlation analysis using standalone functions instead of a class. Includes:
- `normalize_data(x)`
- `scatter_plot(...)` — scatter plots per time window
- `corr_plot(...)` — Pearson correlation over time
- `corr_plot_param_wise(...)` — per-parameter correlation with multiple time steps
- `corr_param_wise_slid(...)` — sliding window correlation

Uses `Pandas_dataframe_O_1011724_56-7.csv` as input.

---

### `corr_mesurment_DTW_DynamicProg.py`
Implements Dynamic Time Warping (DTW) from scratch to measure similarity between N2 rate and `APRS_RAW`.

- `dp(dist_mat)` — dynamic programming DTW path finder
- Visualises distance matrix, cost matrix, alignment path, and warped signals
- Uses `tslearn` and `scipy.spatial.distance`

---

### `FilterDesign_1.py`
Demonstrates Butterworth low-pass filter design using `scipy.signal`.

- Compares `lfilter` (causal) vs `filtfilt` (zero-phase) filtering
- Applied to synthetic noisy signal and real `WH_PRS` data

---

### `HMM_N2dataeventdetection.py`
Applies a Gaussian Hidden Markov Model (HMM) to detect operational states/events in N2 rate data.

- Uses `hmmlearn.hmm.GaussianHMM` with 5 hidden states
- Splits data into train/test sets
- Prints transition matrix, means, and covariances
- Plots predicted hidden states over time

**Dependency:** `hmmlearn`

---

### `N2DataCorrelation.py`
Autocorrelation and time series decomposition analysis of N2 rate.

- Seasonal decomposition (`statsmodels.tsa.seasonal.seasonal_decompose`)
- ACF / PACF plots for segmented time windows
- First-difference stationarity check
- Autocovariance computation and stem plot

**Dependency:** `statsmodels`

---

### `NoiseQunatificationByWT.py`
Noise quantification using Continuous Wavelet Transform (CWT) via the `obspy` library.

- Computes CWT scalogram for `VIB_LAT` first-difference signal
- Plots time series with N2 rate overlay and frequency-time scalogram

**Dependency:** `obspy`

---

### `scatter_Plot_ForChannelParam.py`
Scatter plots of `VIB_LAT` and `SHK_LAT` against `WOB_DH` and `N2_RATE` across multiple datasets (56-5, 08-5, 56-7), with flow rate filtering.

Also contains:
- `activity_data_plot(...)` — Dataiku-based activity-wise multi-run plot
- `sort_jobid_vib_level(...)` — sorts job IDs by vibration/shock level
- `job_id_with_activity(...)` — filters job IDs containing a specific activity
- `POOH_tooface_differece(...)` — computes toolface difference during POOH vs drilling

> Note: Functions using `dataiku.Dataset` require a Dataiku DSS environment.

---

### `trial_codes.py`
Experimental and prototype code. Contains:
- Wiper trip activity data extraction and shock/vibration plotting
- `activity_data_plot(...)` — multi-run activity plot with colour-coded vibration levels
- `sort_jobid_vib_level(...)` — job ID sorting by vibration threshold
- `POOH_tooface_differece(...)` — toolface delta analysis during POOH
- Outlier masking and colour-coded scatter/line plot examples

> Note: Requires Dataiku DSS environment for dataset access functions.

---

## Dependencies

```
pandas
numpy
matplotlib
scipy
statsmodels
seaborn
hmmlearn
obspy
tslearn
```

Install with:
```bash
pip install pandas numpy matplotlib scipy statsmodels seaborn hmmlearn obspy tslearn
```

---

## Data

| File | Description |
|---|---|
| `O.1011724.56-5.csv` | Primary dataset used in correlation and noise analysis |
| `O.1011724.56-7.csv` | Secondary dataset used in multi-axis plot and heatmap |
| `O.1011724.08-5.csv` | Third dataset used in scatter plot analysis |
| `Pandas_dataframe_O_1011724_56-7.csv` | Legacy CSV used in older scripts |

Update the paths in `config.py` before running.
