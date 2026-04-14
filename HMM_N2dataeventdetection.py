import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from hmmlearn import hmm
#%%
data = pd.read_csv("Pandas_dataframe_O_1011724_56-7.csv")
N2data = data[['TIME','N2_RATE']]
# Convert the datetime from str to datetime object.
N2data["TIME"] = pd.to_datetime(data["TIME"])
# Plot the daily gold prices as well as the daily change.
plt.figure(figsize = (15, 10))
plt.plot(N2data["TIME"], N2data["N2_RATE"])
plt.xlabel("datetime")
plt.ylabel("N2_TARE")
plt.grid(True)
#%% Use the daily change in gold price as the observed measurements X.
X = N2data[["N2_RATE"]].values
# Split data into train and test
def train_test_split(df,train_percent = 0.8, seed = None):
    np.random.seed(seed)
    permutation = np.random.permutation(df.index)
    m = len(df.index)
    train_end = int(train_percent * m )
    print(train_end)
    train = df.loc[permutation[:train_end]]
    test = df.loc[permutation[train_end:]]
    return train, test

X_train, X_test = train_test_split(data, train_percent=0.8)
x_train_N2data = X_train[["N2_RATE"]].values
x_test_N2data = X_test[["N2_RATE"]].values

#%% Build the HMM model and fit to the gold price change data.
model = hmm.GaussianHMM(n_components = 5, covariance_type = "spherical", n_iter = 50, random_state = 42)
model.fit(x_train_N2data)
# Predict the hidden states corresponding to observed X.
Z = model.predict(x_test_N2data)
states = pd.unique(Z)
print("Unique states:")
print(states)

print("\nStart probabilities:")
print(model.startprob_)

print("\nTransition matrix:")
print(model.transmat_)

print("\nGaussian distribution means:")
print(model.means_)

print("\nGaussian distribution covariances:")
print(model.covars_)
#%%
plt.figure(figsize = (15, 10))
for i in states:
    want = (Z == i)
    x = X_test["TIME"].iloc[want]
    y = X_test["N2_RATE"].iloc[want]
    plt.plot(x, y, '.')
plt.legend(states, fontsize=16)
plt.grid(True)
plt.xlabel("TIME", fontsize=16)
plt.ylabel("N2_RATE", fontsize=16)
plt.show()
#%%