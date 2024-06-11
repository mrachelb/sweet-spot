
import pandas as pd
import numpy as np
import holidays
from datetime import datetime
import requests




# function to transform weather variables


def weather_data(df:pd.DataFrame):
    weather_URL = "https://archive-api.open-meteo.com/v1/archive"

    params_BE = {
	"latitude": 52.52,
	"longitude": 13.41,
	"start_date": "2017-07-01",
	"end_date": "2024-06-05",
	"daily": ["temperature_2m_mean", "sunshine_duration", "precipitation_hours"],
	"timezone": "Europe/Berlin"}

    params_HH = {
	"latitude": 53.5507,
	"longitude": 9.993,
	"start_date": "2017-07-01",
	"end_date": "2024-06-05",
	"daily": ["temperature_2m_mean", "sunshine_duration", "precipitation_hours"],
	"timezone": "Europe/Berlin"}

    weather_BE = requests.get(url =weather_URL,params=params_BE).json()
    weather_BE = pd.DataFrame(weather_BE.get("daily"))
    weather_BE = weather_BE.rename(columns = {"time":"date"})

    weather_HH = requests.get(url =weather_URL,params=params_HH).json()
    weather_HH = pd.DataFrame(weather_HH.get("daily"))
    weather_HH = weather_HH.rename(columns = {"time":"date"})

    df_new = df.copy().reset_index()

    merged_BE = pd.merge(left = df_new[df_new["Location_name"] == "Berlin"], right = weather_BE, on = "date")
    merged_HH = pd.merge(left = df_new[df_new["Location_name"] == "Hamburg"], right = weather_HH, on = "date")

    df_new = pd.concat([merged_BE, merged_HH]).sort_values(by = "index").reset_index(drop = True).drop("index", axis = 1)

    return df_new





# OLD weather transformations


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



# calculating total amount

def calculate_total_amount(dataframe):
    item_name = dataframe['item_name']
    amount = dataframe['amount']
    
    if any(str(i) in item_name for i in [4, 6, 12]):
        if '4' in item_name:
            return amount * 4
        elif '6' in item_name:
            return amount * 6
        elif '12' in item_name:
            return amount * 12
    elif any(month in item_name for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']):
        return amount * 6
    elif 'box' in item_name.lower():
        return amount * 4
    else:
        return amount * 1