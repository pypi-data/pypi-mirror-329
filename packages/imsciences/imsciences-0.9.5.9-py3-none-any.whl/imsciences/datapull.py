import pandas as pd
import calendar
import requests
import os
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import datetime
import re
import pandas as pd
from imsciences import *
from fredapi import Fred
import time
from datetime import datetime
from datafunctions import dataprocessing

class datapull:
    
    def pull_help(self):
        print("This is the help section. The functions in the package are as follows:")

        print("\n1. pull_fred_data")
        print("   - Description: Get data from FRED by using series id tokens.")
        print("   - Usage: pull_fred_data(week_commencing, series_id_list)")
        print("   - Example: pull_fred_data('sun', ['GPDIC1', 'Y057RX1Q020SBEA', 'GCEC1', 'ND000333Q', 'Y006RX1Q020SBEA'])")
    
    ###############################################################  MACRO ##########################################################################

    def pull_fred_data(self, week_commencing: str = 'mon', series_id_list: list[str] = ["GPDIC1", "Y057RX1Q020SBEA", "GCEC1", "ND000333Q", "Y006RX1Q020SBEA"]) -> pd.DataFrame:
        '''
        Parameters
        ----------
        week_commencing : str
            specify the day for the week commencing, the default is 'sun' (e.g., 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')

        series_id_list : list[str]
            provide a list with IDs to download data series from FRED (link: https://fred.stlouisfed.org/tags/series?t=id). Default list is 
            ["GPDIC1", "Y057RX1Q020SBEA", "GCEC1", "ND000333Q", "Y006RX1Q020SBEA"]
        
        Returns
        ----------
        pd.DataFrame
            Return a data frame with FRED data according to the series IDs provided

        Example
        ----------
        pull_fred_data("mon", ["GCEC1", "SP500"])
        '''
        # Fred API
        fred = Fred(api_key='76f5f8156145fdb8fbaf66f1eb944f8a')

        # Fetch the metadata for each series to get the full names
        series_names = {series_id: fred.get_series_info(series_id).title for series_id in series_id_list}

        # Download data from series id list
        fred_series = {series_id: fred.get_series(series_id) for series_id in series_id_list}

        # Data processing
        date_range = {'OBS': pd.date_range("1950-01-01", datetime.today().strftime('%Y-%m-%d'), freq='d')}
        fred_series_df = pd.DataFrame(date_range)

        for series_id, series_data in fred_series.items():
            series_data = series_data.reset_index()
            series_data.columns = ['OBS', series_names[series_id]]  # Use the series name as the column header
            fred_series_df = pd.merge_asof(fred_series_df, series_data, on='OBS', direction='backward')

        # Handle duplicate columns
        for col in fred_series_df.columns:
            if '_x' in col:
                base_col = col.replace('_x', '')
                fred_series_df[base_col] = fred_series_df[col].combine_first(fred_series_df[base_col + '_y'])
                fred_series_df.drop([col, base_col + '_y'], axis=1, inplace=True)

        # Ensure sum_columns are present in the DataFrame
        sum_columns = [series_names[series_id] for series_id in series_id_list if series_names[series_id] in fred_series_df.columns]

        # Aggregate results by week
        fred_df_final = dataprocessing.aggregate_daily_to_wc_wide(self, df=fred_series_df, 
                                                    date_column="OBS", 
                                                    group_columns=[], 
                                                    sum_columns=sum_columns,
                                                    wc=week_commencing,
                                                    aggregation="average")

        # Remove anything after the instance of any ':' in the column names and rename, except for 'OBS'
        fred_df_final.columns = ['OBS' if col == 'OBS' else 'macro_' + col.lower().split(':')[0].replace(' ', '_') for col in fred_df_final.columns]

        return fred_df_final
    
    def pull_boe_data(self, week_commencing="mon", max_retries=30, delay=5):
        """
        Fetch and process Bank of England interest rate data.

        Args:
            week_commencing (str): The starting day of the week for aggregation. 
                                Options are "mon", "tue", "wed", "thur", "fri", "sat", "sun". 
                                Default is "sun".
            max_retries (int): Maximum number of retries to fetch data in case of failure. Default is 30.
            delay (int): Delay in seconds between retry attempts. Default is 5.

        Returns:
            pd.DataFrame: A DataFrame with weekly aggregated Bank of England interest rates. 
                        The 'OBS' column contains the week commencing dates in 'dd/mm/yyyy' format 
                        and 'macro_boe_intr_rate' contains the average interest rate for the week.
        """
        # Week commencing dictionary
        day_dict = {"mon": 0, "tue": 1, "wed": 2, "thur": 3, "fri": 4, "sat": 5, "sun": 6}
        
        # Function to fetch the data with retries
        def fetch_data_with_retries(url, max_retries, delay):
            for attempt in range(max_retries):
                try:
                    html_table = pd.read_html(url)[0]
                    return html_table
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                    else:
                        raise
        
        # Import HTML data from Bank of England rate
        url = 'https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp'
        html_table = fetch_data_with_retries(url, max_retries, delay)
        
        df = pd.DataFrame(html_table)
        df.rename(columns={"Date Changed": "OBS", "Rate": "macro_boe_intr_rate"}, inplace=True)
        
        # Change date column to datetime and find the corresponding week to the date
        df["OBS"] = pd.to_datetime(df["OBS"], format="%d %b %y")
        df.sort_values("OBS", axis=0, inplace=True)
        
        # Create a daily date range and find the week commencing for that day
        date_range = pd.date_range(df["OBS"].iloc[0], datetime.today(), freq="d")
        df_daily = pd.DataFrame(date_range, columns=["OBS"])
        
        # Adjust each date to the specified week commencing day
        df_daily['Week_Commencing'] = df_daily["OBS"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))
        
        # Outer merge the daily date range on the boe dataframe and forward fill in the blanks
        df_final = df_daily.merge(df, on='OBS', how="left")
        df_final["macro_boe_intr_rate"].ffill(inplace=True)
        
        # Group by the week start date and get the mean of the interest rates for each week
        df_final = df_final.groupby('Week_Commencing')['macro_boe_intr_rate'].mean().reset_index()
        
        df_final['Week_Commencing'] = df_final['Week_Commencing'].dt.strftime('%d/%m/%Y')
        df_final.rename(columns={'Week_Commencing': 'OBS'}, inplace=True)
        
        return df_final

    def pull_ons_data(self, series_list, week_commencing):
        """
        Fetch and process time series data from the ONS API.

        Args:
            series_list (list): A list of dictionaries where each dictionary represents a time series.
                                Each dictionary should have the keys 'series_id' and 'dataset_id'.
            week_commencing (str): The starting day of the week for aggregation. 
                                Options are "mon", "tue", "wed", "thur", "fri", "sat", "sun".

        Returns:
            pd.DataFrame: A DataFrame with weekly aggregated ONS data. The 'OBS' column contains the week 
                        commencing dates and other columns contain the aggregated time series values.
        """ 
        # Generate a date range from 1950-01-01 to today
        date_range = pd.date_range(start="1950-01-01", end=datetime.today(), freq='D')
        daily_df = pd.DataFrame(date_range, columns=['OBS'])
        
        # Keep track of the renamed value columns
        value_columns = []

        for series in series_list:
            series_id = series['series_id']
            dataset_id = series['dataset_id']
            
            # Construct the URL for data
            data_url = f"https://api.ons.gov.uk/timeseries/{series_id}/dataset/{dataset_id}/data"
            
            # Make the request to the ONS API for data
            data_response = requests.get(data_url)
            
            # Check if the request was successful
            if data_response.status_code != 200:
                print(f"Failed to fetch data for series {series_id}: {data_response.status_code} {data_response.text}")
                continue
            
            # Parse the JSON response for data
            data = data_response.json()
            
            # Attempt to extract the name of the time series from the data response
            series_name = data.get('description', {}).get('title', 'Value')
            
            # Determine the most granular time series data available
            if 'months' in data and data['months']:
                time_series_data = data['months']
            elif 'quarters' in data and data['quarters']:
                time_series_data = data['quarters']
            elif 'years' in data and data['years']:
                time_series_data = data['years']
            else:
                print("No time series data found in the response")
                continue
            
            # Create a DataFrame from the time series data
            df = pd.DataFrame(time_series_data)
            
            # Handle different frequencies in the data
            if 'date' in df.columns:
                if any(df['date'].str.contains('Q')):  
                    df['date'] = pd.PeriodIndex(df['date'], freq='Q').to_timestamp()
                else:  
                    df['date'] = pd.to_datetime(df['date'])
            
            df = df.rename(columns={'date': 'OBS', 'value': series_name})
            
            # Rename the value column
            new_col_name = 'macro_' + series_name.lower().replace(':', '').replace(' ', '_').replace('-', '_')
            df = df.rename(columns={series_name: new_col_name})
            
            # Track the renamed value column
            value_columns.append(new_col_name)
            
            # Merge the data based on the observation date
            daily_df = pd.merge_asof(daily_df, df[['OBS', new_col_name]], on='OBS', direction='backward')
                
        # Ensure columns are numeric
        for col in value_columns:
            if col in daily_df.columns:
                daily_df[col] = pd.to_numeric(daily_df[col], errors='coerce').fillna(0)
            else:
                print(f"Column {col} not found in daily_df")
        
        # Aggregate results by week
        ons_df_final = dataprocessing.aggregate_daily_to_wc_wide(self, df=daily_df, 
                                                    date_column="OBS", 
                                                    group_columns=[], 
                                                    sum_columns=value_columns,
                                                    wc=week_commencing,
                                                    aggregation="average")
        
        return ons_df_final
    
    ###############################################################  Seasonality  ##########################################################################

    def pull_combined_dummies(self, week_commencing):
        # Week commencing dictionary
        day_dict = {"mon": 0, "tue": 1, "wed": 2, "thur": 3, "fri": 4, "sat": 5, "sun": 6}
        
        # Create daily date range dataframe
        date_range = pd.date_range(datetime.datetime(2015, 1, 1), datetime.date.today(), freq="d")
        df_daily = pd.DataFrame(date_range, columns=["Date"])

        # Create weekly date range dataframe
        df_daily['week_start'] = df_daily["Date"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))
        df_weekly_start = df_daily[['week_start']].drop_duplicates().reset_index(drop=True)
        df_weekly_start.rename(columns={'week_start': "Date"}, inplace=True)
        
        df_weekly_start.index = np.arange(1, len(df_weekly_start) + 1)
        df_weekly_start.set_index("Date", inplace=True)
        
        # Create individual weekly dummies
        dummy_columns = {}
        for i in range(len(df_weekly_start)):
            col_name = f"dum_{df_weekly_start.index[i].strftime('%Y_%m_%d')}"
            dummy_columns[col_name] = [0] * len(df_weekly_start)
            dummy_columns[col_name][i] = 1
        
        df_dummies = pd.DataFrame(dummy_columns, index=df_weekly_start.index)
        df_weekly_start = pd.concat([df_weekly_start, df_dummies], axis=1)
        
        # Create monthly dummies
        df_daily["Month"] = df_daily["Date"].dt.month_name().str.lower()
        df_monthly_dummies = pd.get_dummies(df_daily, prefix="seas", columns=["Month"])
        df_monthly_dummies['week_start'] = df_daily["Date"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))
        df_monthly_dummies = df_monthly_dummies.groupby('week_start').sum(numeric_only=True).reset_index().rename(columns={'week_start': "Date"})
        
        df_monthly_dummies.set_index("Date", inplace=True)
        df_monthly_dummies = df_monthly_dummies / 7
        
        # Combine weekly and monthly dataframes
        df_combined = pd.concat([df_weekly_start, df_monthly_dummies], axis=1)
        
        # Create weekly dummies
        df_combined.reset_index(inplace=True)
        df_combined["Week"] = df_combined["Date"].dt.isocalendar().week
        df_combined = pd.get_dummies(df_combined, prefix="wk", columns=["Week"])
        
        # Create yearly dummies
        df_combined["Year"] = df_combined["Date"].dt.year
        df_combined = pd.get_dummies(df_combined, prefix="seas", columns=["Year"])
        
        # Add constant
        df_combined["Constant"] = 1
        
        # Add trend
        df_combined["Trend"] = df_combined.index + 1
        
        # Set date as index
        df_combined.set_index("Date", inplace=True)
        
        # Create COVID lockdown dummies
        lockdown_periods = [
            # Lockdown 1
            ("2020-03-23", "2020-05-24"),
            # Lockdown 2
            ("2020-11-05", "2020-12-02"),
            # Lockdown 3
            ("2021-01-04", "2021-03-08")
        ]
        
        df_covid = pd.DataFrame(date_range, columns=["Date"])
        df_covid["national_lockdown"] = 0
        
        for start, end in lockdown_periods:
            df_covid.loc[(df_covid["Date"] >= start) & (df_covid["Date"] <= end), "national_lockdown"] = 1
        
        df_covid['week_start'] = df_covid["Date"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))
        df_covid.drop("Date", axis=1, inplace=True)
        df_covid.rename(columns={"week_start": "OBS"}, inplace=True)
        df_national_lockdown_total = df_covid.groupby('OBS').sum(numeric_only=True)
        df_national_lockdown_total.rename(columns={"national_lockdown": "covid_national_lockdown_total"}, inplace=True)
        
        df_national_lockdown_1 = df_national_lockdown_total.copy(deep=True)
        df_national_lockdown_2 = df_national_lockdown_total.copy(deep=True)
        df_national_lockdown_3 = df_national_lockdown_total.copy(deep=True)

        df_national_lockdown_1.loc[df_national_lockdown_1.index > "2020-05-24"] = 0
        df_national_lockdown_1.rename(columns={"covid_national_lockdown_total": "covid_national_lockdown_1"}, inplace=True)

        df_national_lockdown_2.loc[df_national_lockdown_2.index < "2020-11-05"] = 0
        df_national_lockdown_2.loc[df_national_lockdown_2.index > "2020-12-02"] = 0                          
        df_national_lockdown_2.rename(columns={"covid_national_lockdown_total": "covid_national_lockdown_2"}, inplace=True)

        df_national_lockdown_3.loc[df_national_lockdown_3.index < "2021-01-04"] = 0
        df_national_lockdown_3.rename(columns={"covid_national_lockdown_total": "covid_national_lockdown_3"}, inplace=True)

        df_final_covid = pd.concat([df_national_lockdown_total, df_national_lockdown_1, df_national_lockdown_2, df_national_lockdown_3], axis=1)
        df_final_covid.reset_index(inplace=True)
        df_final_covid.rename(columns={"index": "OBS"}, inplace=True)
        
        # Create seasonal indicators for the last day and last Friday of the month
        min_date = '2019-12-29'
        max_date = datetime.date.today().strftime('%Y-%m-%d')
        date_range_seas = pd.date_range(start=min_date, end=max_date)
        
        df_seas = pd.DataFrame(date_range_seas, columns=['Date'])
        df_seas['Last_Day_of_Month'] = df_seas['Date'].apply(lambda x: 1 if x == x.to_period('M').to_timestamp('M') else 0)
        
        def is_last_friday(date):
            last_day_of_month = date.to_period('M').to_timestamp('M')
            last_day_weekday = last_day_of_month.dayofweek
            if last_day_weekday >= 4:
                days_to_subtract = last_day_weekday - 4
            else:
                days_to_subtract = last_day_weekday + 3
            last_friday = last_day_of_month - pd.Timedelta(days=days_to_subtract)
            return 1 if date == last_friday else 0
        
        df_seas['Last_Friday_of_Month'] = df_seas['Date'].apply(is_last_friday)
        
        df_seas['week_start'] = df_seas["Date"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))
        df_seas = df_seas.groupby('week_start').sum(numeric_only=True).reset_index().rename(columns={'week_start': "Date"})
        df_seas.set_index("Date", inplace=True)
        
        # Combine all dataframes
        df_combined = df_combined.reset_index().rename(columns={"Date": "OBS"})
        df_final_combined = pd.merge(df_combined, df_final_covid, how='left', left_on='OBS', right_on='OBS')
        df_final_combined = pd.merge(df_final_combined, df_seas, how='left', left_on='OBS', right_on='Date')

        # Fill any NaN values with 0
        df_final_combined.fillna(0, inplace=True)
        
        return df_final_combined
