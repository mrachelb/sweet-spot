
from statsmodels.tsa.stattools import adfuller

# create function for adjusted r-squared

def adj_r2(r2, x):
    adjr2 =round(1 - ((1 -r2) * (len(x) - 1) / (len(x) - x.shape[1] - 1)),3)
    return adjr2 


# Advanced Dickey-Fuller test to check for stationarity

def adf_test_p_values (df):
    p_vals = []
    for store in df["store_name"].unique():
        store_df = df[df["store_name"] == store]
        p = adfuller(store_df["total_amount"], autolag="AIC")[1]
        p_vals.append((store, p))
    return (p_vals)


