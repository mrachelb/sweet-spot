
import pandas as pd
import numpy as np


# function to transform weather variables

def transform_weather_temp(df, variable:str):
    df = df.iloc[:,[1,3]]
    df["date"] = df["MESS_DATUM"].apply(lambda x: pd.to_datetime(str(x), format = "%Y%m%d%H"))
    df[(df["date"].dt.date >= pd.to_datetime('2017-07-01').date()) &
        (df["date"].dt.time >= pd.to_datetime("08:00:00").time()) &
        (df["date"].dt.time <= pd.to_datetime("20:00:00").time()) ]
    df["date"] = df["date"].dt.date
    df = df.groupby("date").mean().reset_index().loc[:,["date",variable]]
    df["date"] = df["date"].apply(lambda x: pd.Timestamp(x))
    return df


def transform_weather_prec_sunshine(df, variable:str):
    df = df.iloc[:,[1,3]]
    df["date"] = df["MESS_DATUM"].apply(lambda x: pd.to_datetime(str(x), format = "%Y%m%d%H"))
    df[(df["date"].dt.date >= pd.to_datetime('2017-07-01').date()) &
        (df["date"].dt.time >= pd.to_datetime("08:00:00").time()) &
        (df["date"].dt.time <= pd.to_datetime("20:00:00").time()) ]
    df["date"] = df["date"].dt.date
    df = df.groupby("date").sum().reset_index().loc[:,["date",variable]]
    df["date"] = df["date"].apply(lambda x: pd.Timestamp(x))
    return df