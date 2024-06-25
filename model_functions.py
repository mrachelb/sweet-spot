
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


# Create train and test datasets for the different stores

def store_dataset (train, test):

    # Training set 

    groups = train[-train["store_name"].isin(["Neuer Kamp","Altona","Jungfernstieg","Hamburg Hauptbahnhof","KaDeWe"])].groupby("store_name")[["days_back","month","total_amount","lag1"]]

    group_dict = {i:j for i, j in groups}

    for store in group_dict:
        globals()[store.lower()] = group_dict[store]

    for store in group_dict:
        globals()[f'{store.lower()}_y'] = group_dict[store]['total_amount']


    # Test set

    groups_test = test[-test["store_name"].isin(["Neuer Kamp","Altona","Jungfernstieg","Hamburg Hauptbahnhof","KaDeWe"])].groupby("store_name")[["days_back","month","total_amount","lag1"]]

    group_dict_test = {i:j for i, j in groups_test}

    for store in group_dict_test:
        globals()[f"{store.lower()}_test"] = group_dict_test[store]

    for store in group_dict_test:
        globals()[f'{store.lower()}_y_test'] = group_dict_test[store]['total_amount']
    
    return danziger, danziger_test