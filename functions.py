
import pandas as pd
import numpy as np
import holidays
from datetime import datetime

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

# school holidays

def hol_school (df,h_s):
    df['date'] =pd.to_datetime(df['date'])
    start =pd.to_datetime(h_s["Beginn"], format ="%d.%m.%Y").to_frame()
    end =pd.to_datetime(h_s["Ende"], format ="%d.%m.%Y").to_frame()
    h_s =pd.concat([start,end], axis =1)
    def gen_range(row):
        return pd.date_range(start=row['Beginn'], end=row['Ende'])
    h_s['date'] =h_s.apply(gen_range, axis=1)
    h_s_exp =h_s.explode('date').reset_index(drop=True).drop(["Beginn","Ende"], axis =1)
    h_s_exp["hol_school"] =1
    df =pd.merge(left=df,right=h_s_exp, how="left", on="date").fillna(0)
    return df

# public holidays 

def hol_pub (df):
    hol_ber =holidays.Germany(years=range(2017, 2024), prov='BE')
    hol_dates =sorted(hol_ber.keys())
    h_p =pd.DataFrame(hol_dates, columns=['date'])
    h_p['date'] =pd.to_datetime(h_p['date'])
    h_p["hol_pub"] =1
    df =pd.merge(left=df,right=h_p, how="left",  on="date").fillna(0)
    return df