import pandas as pd
import numpy as np
import re
from fredapi import Fred
import time
from datetime import datetime, timedelta
from io import StringIO
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import yfinance as yf
import holidays
from dateutil.easter import easter
import urllib.request
from geopy.geocoders import Nominatim

from imsciences.mmm import dataprocessing

ims_proc = dataprocessing()

class datapull:
    
    def help(self):
        print("This is the help section. The functions in the package are as follows:")

        print("\n1. pull_fred_data")
        print("   - Description: Get data from FRED by using series id tokens.")
        print("   - Usage: pull_fred_data(week_commencing, series_id_list)")
        print("   - Example: pull_fred_data('mon', ['GPDIC1'])")

        print("\n2. pull_boe_data")
        print("   - Description: Fetch and process Bank of England interest rate data.")
        print("   - Usage: pull_boe_data(week_commencing)")
        print("   - Example: pull_boe_data('mon')")

        print("\n3. pull_oecd")
        print("   - Description: Fetch macroeconomic data from OECD for a specified country.")
        print("   - Usage: pull_oecd(country='GBR', week_commencing='mon', start_date: '2020-01-01')")
        print("   - Example: pull_oecd('GBR', 'mon', '2000-01-01')")

        print("\n4. get_google_mobility_data")
        print("   - Description: Fetch Google Mobility data for the specified country.")
        print("   - Usage: get_google_mobility_data(country, wc)")
        print("   - Example: get_google_mobility_data('United Kingdom', 'mon')")

        print("\n5. pull_seasonality")
        print("   - Description: Generate combined dummy variables for seasonality, trends, and COVID lockdowns.")
        print("   - Usage: pull_seasonality(week_commencing, start_date, countries)")
        print("   - Example: pull_seasonality('mon', '2020-01-01', ['US', 'GB'])")

        print("\n6. pull_weather")
        print("   - Description: Fetch and process historical weather data for the specified country.")
        print("   - Usage: pull_weather(week_commencing, start_date, country)")
        print("   - Example: pull_weather('mon', '2020-01-01', ['GBR'])")
        
        print("\n7. pull_macro_ons_uk")
        print("   - Description: Fetch and process time series data from the Beta ONS API.")
        print("   - Usage: pull_macro_ons_uk(aditional_list, week_commencing, sector)")
        print("   - Example: pull_macro_ons_uk(['HBOI'], 'mon', 'fast_food')")
        
        print("\n8. pull_yfinance")
        print("   - Description: Fetch and process time series data from the Beta ONS API.")
        print("   - Usage: pull_yfinance(tickers, week_start_day)")
        print("   - Example: pull_yfinance(['^FTMC', '^IXIC'], 'mon')")
        
        print("\n9. pull_sports_events")
        print("   - Description: Pull a veriety of sports events primaraly football and rugby.")
        print("   - Usage: pull_sports_events(start_date, week_commencing)")
        print("   - Example: pull_sports_events('2020-01-01', 'mon')")

    ###############################################################  MACRO ##########################################################################

    def pull_fred_data(self, week_commencing: str = 'mon', series_id_list: list[str] = ["GPDIC1", "Y057RX1Q020SBEA", "GCEC1"]) -> pd.DataFrame:
        '''
        Parameters
        ----------
        week_commencing : str
            specify the day for the week commencing, the default is 'sun' (e.g., 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')

        series_id_list : list[str]
            provide a list with IDs to download data series from FRED (link: https://fred.stlouisfed.org/tags/series?t=id). Default list is 
            ["GPDIC1", "Y057RX1Q020SBEA", "GCEC1"]
        
        Returns
        ----------
        pd.DataFrame
            Return a data frame with FRED data according to the series IDs provided
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
        fred_df_final = ims_proc.aggregate_daily_to_wc_wide(df=fred_series_df, 
                                                    date_column="OBS", 
                                                    group_columns=[], 
                                                    sum_columns=sum_columns,
                                                    wc=week_commencing,
                                                    aggregation="average")

        # Remove anything after the instance of any ':' in the column names and rename, except for 'OBS'
        fred_df_final.columns = ['OBS' if col == 'OBS' else 'macro_' + col.lower().split(':')[0].replace(' ', '_') for col in fred_df_final.columns]

        return fred_df_final
    
    def pull_boe_data(self, week_commencing="mon", max_retries=5, delay=5):
        """
        Fetch and process Bank of England interest rate data.

        Args:
            week_commencing (str): The starting day of the week for aggregation.
                                Options are "mon", "tue", "wed", "thur", "fri", "sat", "sun".
                                Default is "mon".
            max_retries (int): Maximum number of retries to fetch data in case of failure. Default is 5.
            delay (int): Delay in seconds between retry attempts. Default is 5.

        Returns:
            pd.DataFrame: A DataFrame with weekly aggregated Bank of England interest rates.
                        The 'OBS' column contains the week commencing dates in 'dd/mm/yyyy' format
                        and 'macro_boe_intr_rate' contains the average interest rate for the week.
        """
        # Week commencing dictionary
        day_dict = {"mon": 0, "tue": 1, "wed": 2, "thur": 3, "fri": 4, "sat": 5, "sun": 6}

        # URL of the Bank of England data page
        url = 'https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp'

        # Retry logic for HTTP request
        for attempt in range(max_retries):
            try:
                # Set up headers to mimic a browser request
                headers = {
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/91.0.4472.124 Safari/537.36"
                    )
                }
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Raise an exception for HTTP errors
                break
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay)
                else:
                    raise

        # Parse the HTML page
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the table on the page
        table = soup.find("table")  # Locate the first table
        table_html = str(table)  # Convert table to string
        df = pd.read_html(StringIO(table_html))[0]  # Use StringIO to wrap the table HTML

        # Rename and clean up columns
        df.rename(columns={"Date Changed": "OBS", "Rate": "macro_boe_intr_rate"}, inplace=True)
        df["OBS"] = pd.to_datetime(df["OBS"], format="%d %b %y")
        df.sort_values("OBS", inplace=True)

        # Create a daily date range
        date_range = pd.date_range(df["OBS"].min(), datetime.today(), freq="D")
        df_daily = pd.DataFrame(date_range, columns=["OBS"])

        # Adjust each date to the specified week commencing day
        df_daily["Week_Commencing"] = df_daily["OBS"].apply(
            lambda x: x - timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7)
        )

        # Merge and forward-fill missing rates
        df_daily = df_daily.merge(df, on="OBS", how="left")
        df_daily["macro_boe_intr_rate"] = df_daily["macro_boe_intr_rate"].ffill()

        # Group by week commencing and calculate the average rate
        df_final = df_daily.groupby("Week_Commencing")["macro_boe_intr_rate"].mean().reset_index()
        df_final["Week_Commencing"] = df_final["Week_Commencing"].dt.strftime('%d/%m/%Y')
        df_final.rename(columns={"Week_Commencing": "OBS"}, inplace=True)

        return df_final
    
    def pull_oecd(self, country: str = "GBR", week_commencing: str = "mon", start_date: str = "2020-01-01") -> pd.DataFrame:
        """
        Fetch and process time series data from the OECD API.

        Args:
            country (list): A string containing a 3-letter code the of country of interest (E.g: "GBR", "FRA", "USA", "DEU")
            week_commencing (str): The starting day of the week for aggregation. 
                                Options are "mon", "tue", "wed", "thur", "fri", "sat", "sun".
            start_date (str): Dataset start date in the format "YYYY-MM-DD"

        Returns:
            pd.DataFrame: A DataFrame with weekly aggregated OECD data. The 'OBS' column contains the week 
                        commencing dates, and other columns contain the aggregated time series values.
        """ 

        def parse_quarter(date_str):
            """Parses a string in 'YYYY-Q#' format into a datetime object."""
            year, quarter = date_str.split('-')
            quarter_number = int(quarter[1])
            month = (quarter_number - 1) * 3 + 1
            return pd.Timestamp(f"{year}-{month:02d}-01")

        # Generate a date range from 1950-01-01 to today
        date_range = pd.date_range(start=start_date, end=datetime.today(), freq='D')

        url_details = [
            ["BCICP",    "SDD.STES,DSD_STES@DF_CLI,",                       ".....",              "macro_business_confidence_index"],
            ["CCICP",    "SDD.STES,DSD_STES@DF_CLI,",                       ".....",              "macro_consumer_confidence_index"],
            ["N.CPI",    "SDD.TPS,DSD_PRICES@DF_PRICES_ALL,",               "PA._T.N.GY",         "macro_cpi_total"],        
            ["N.CPI",    "SDD.TPS,DSD_PRICES@DF_PRICES_ALL,",               "PA.CP041T043.N.GY",  "macro_cpi_housing"],
            ["N.CPI",    "SDD.TPS,DSD_PRICES@DF_PRICES_ALL,",               "PA.CP01.N.GY",       "macro_cpi_food"],
            ["N.CPI",    "SDD.TPS,DSD_PRICES@DF_PRICES_ALL,",               "PA.CP045_0722.N.GY", "macro_cpi_energy"],
            ["UNE_LF_M", "SDD.TPS,DSD_LFS@DF_IALFS_UNE_M,",                 "._Z.Y._T.Y_GE15.",   "macro_unemployment_rate"],
            ["EAR",      "SDD.TPS,DSD_EAR@DF_HOU_EAR,",                     ".Y..S1D",            "macro_private_hourly_earnings"],
            ["RHP",      "ECO.MPD,DSD_AN_HOUSE_PRICES@DF_HOUSE_PRICES,1.0", "",                   "macro_real_house_prices"],
            ["PRVM",     "SDD.STES,DSD_KEI@DF_KEI,4.0",                     "IX.C..",             "macro_manufacturing_production_volume"],
            ["TOVM",     "SDD.STES,DSD_KEI@DF_KEI,4.0",                     "IX...",              "macro_retail_trade_volume"],
            ["IRSTCI",   "SDD.STES,DSD_KEI@DF_KEI,4.0",                     "PA...",              "macro_interbank_rate"],
            ["IRLT",     "SDD.STES,DSD_KEI@DF_KEI,4.0",                     "PA...",              "macro_long_term_interest_rate"],
            ["B1GQ",     "SDD.NAD,DSD_NAMAIN1@DF_QNA,1.1",                  "._Z....GY.T0102",    "macro_gdp_growth_yoy"]
        ]

        # Create empty final dataframe
        oecd_df_final = pd.DataFrame()

        daily_df = pd.DataFrame({'OBS': date_range})
        value_columns = []

        # Iterate for each variable of interest
        for series_details in url_details:
            series = series_details[0]
            dataset_id = series_details[1]
            filter = series_details[2]
            col_name = series_details[3]

            # check if request was successful and determine the most granular data available
            for freq in ['M', 'Q', 'A']:
                
                if series in ["UNE_LF_M", "EAR"]:
                    data_url = f"https://sdmx.oecd.org/public/rest/data/OECD.{dataset_id}/{country}.{series}.{filter}.{freq}?startPeriod=1950-01"
                elif series in ["B1GQ"]:
                    data_url = f"https://sdmx.oecd.org/public/rest/data/OECD.{dataset_id}/{freq}..{country}...{series}.{filter}?startPeriod=1950-01"
                else:
                    data_url = f"https://sdmx.oecd.org/public/rest/data/OECD.{dataset_id}/{country}.{freq}.{series}.{filter}?startPeriod=1950-01"

                # Make the request to the OECD API for data
                data_response = requests.get(data_url)

                # Check if the request was successful
                if data_response.status_code != 200:
                    print(f"Failed to fetch data for series {series} with frequency '{freq}' for {country}: {data_response.status_code} {data_response.text}")
                    url_test = False
                    continue
                else:
                    url_test = True
                    break
            
            # get data for the next variable if url doesn't exist
            if url_test is False:
                continue

            root = ET.fromstring(data_response.content)

            # Define namespaces if necessary (the namespace is included in the tags)
            namespaces = {'generic': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic'}

            # Lists to store the data
            dates = []
            values = []

            # Iterate over all <Obs> elements and extract date and value
            for obs in root.findall('.//generic:Obs', namespaces):        

                # Extracting the time period (date)
                time_period = obs.find('.//generic:ObsDimension', namespaces).get('value')
                
                # Extracting the observation value
                value = obs.find('.//generic:ObsValue', namespaces).get('value')
                
                # Storing the data
                if time_period and value:
                    dates.append(time_period)
                    values.append(float(value))  # Convert value to float

            # Add variable names that were found to a list
            value_columns.append(col_name)

            # Creating a DataFrame
            data = pd.DataFrame({'OBS': dates, col_name: values})

            # Convert date strings into datetime format
            if freq == 'Q':
                data['OBS'] = data['OBS'].apply(parse_quarter)
            else:
                # Display the DataFrame
                data['OBS'] = data['OBS'].apply(lambda x: datetime.strptime(x, '%Y-%m'))

            # Sort data by chronological order
            data.sort_values(by='OBS', inplace=True)

            # Merge the data based on the observation date
            daily_df = pd.merge_asof(daily_df, data[['OBS', col_name]], on='OBS', direction='backward')


        # Ensure columns are numeric
        for col in value_columns:
            if col in daily_df.columns:
                daily_df[col] = pd.to_numeric(daily_df[col], errors='coerce').fillna(0)
            else:
                print(f"Column {col} not found in daily_df")

        # Aggregate results by week
        country_df = ims_proc.aggregate_daily_to_wc_wide(df=daily_df, 
                                                        date_column="OBS", 
                                                        group_columns=[], 
                                                        sum_columns=value_columns,
                                                        wc=week_commencing,
                                                        aggregation="average")
        
        oecd_df_final = pd.concat([oecd_df_final, country_df], axis=0, ignore_index=True)

        return oecd_df_final
    
    def get_google_mobility_data(self, country="United Kingdom", wc="mon") -> pd.DataFrame:
        """
        Fetch Google Mobility data for the specified country.
        
        Parameters:
        - country (str): The name of the country for which to fetch data.

        Returns:
        - pd.DataFrame: A DataFrame containing the Google Mobility data.
        """
        # URL of the Google Mobility Reports CSV file
        url = "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv"
        
        # Fetch the CSV file
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.status_code}")
        
        # Load the CSV file into a pandas DataFrame
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data, low_memory=False)
        
        # Filter the DataFrame for the specified country
        country_df = df[df['country_region'] == country]
        
        final_covid = ims_proc.aggregate_daily_to_wc_wide(country_df, "date", [],  ['retail_and_recreation_percent_change_from_baseline', 'grocery_and_pharmacy_percent_change_from_baseline',
                                                                                'parks_percent_change_from_baseline', 'transit_stations_percent_change_from_baseline',
                                                                                'workplaces_percent_change_from_baseline', 'residential_percent_change_from_baseline'], wc, "average")
        
        final_covid1 = ims_proc.rename_cols(final_covid, 'covid_')
        return final_covid1
        
    ###############################################################  Seasonality  ##########################################################################

    def pull_seasonality(self, week_commencing, start_date, countries):
        # ---------------------------------------------------------------------
        # 0. Setup: dictionary for 'week_commencing' to Python weekday() integer
        # ---------------------------------------------------------------------
        day_dict = {"mon": 0, "tue": 1, "wed": 2, "thur": 3, "fri": 4, "sat": 5, "sun": 6}

        # ---------------------------------------------------------------------
        # 1. Create daily date range from start_date to today
        # ---------------------------------------------------------------------
        date_range = pd.date_range(
            start=pd.to_datetime(start_date), 
            end=datetime.today(), 
            freq="D"
        )
        df_daily = pd.DataFrame(date_range, columns=["Date"])

        # ---------------------------------------------------------------------
        # 1.1 Identify "week_start" for each daily row, based on week_commencing
        # ---------------------------------------------------------------------
        df_daily['week_start'] = df_daily["Date"].apply(
            lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7)
        )

        # ---------------------------------------------------------------------
        # 2. Build a weekly index (df_weekly_start) with dummy columns
        # ---------------------------------------------------------------------
        df_weekly_start = df_daily[['week_start']].drop_duplicates().reset_index(drop=True)
        df_weekly_start.rename(columns={'week_start': "Date"}, inplace=True)
        
        # Set index to weekly "start of week"
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

        # ---------------------------------------------------------------------
        # 3. Public holidays (daily) from 'holidays' package + each holiday name
        # ---------------------------------------------------------------------
        for country in countries:
            country_holidays = holidays.CountryHoliday(
                country, 
                years=range(int(start_date[:4]), datetime.today().year + 1)
            )
            # Daily indicator: 1 if that date is a holiday
            df_daily[f"seas_holiday_{country.lower()}"] = df_daily["Date"].apply(
                lambda x: 1 if x in country_holidays else 0
            )
            # Create columns for specific holiday names
            for date_hol, name in country_holidays.items():
                col_name = f"seas_{name.replace(' ', '_').lower()}_{country.lower()}"
                if col_name not in df_daily.columns:
                    df_daily[col_name] = 0
                df_daily.loc[df_daily["Date"] == pd.Timestamp(date_hol), col_name] = 1

        # ---------------------------------------------------------------------
        # 3.1 Additional Special Days (Father's Day, Mother's Day, etc.)
        #     We'll add daily columns for each. 
        # ---------------------------------------------------------------------
        # Initialize columns
        extra_cols = [
            "seas_valentines_day", 
            "seas_halloween", 
            "seas_fathers_day_us_uk",
            "seas_mothers_day_us",
            "seas_mothers_day_uk",
            "seas_good_friday",
            "seas_easter_monday",
            "seas_black_friday",
            "seas_cyber_monday",
        ]
        for c in extra_cols:
            df_daily[c] = 0  # default zero

        # Helper: nth_weekday_of_month(year, month, weekday, nth=1 => first, 2 => second, etc.)
        # weekday: Monday=0, Tuesday=1, ... Sunday=6
        def nth_weekday_of_month(year, month, weekday, nth):
            """
            Returns date of the nth <weekday> in <month> of <year>.
            E.g. nth_weekday_of_month(2023, 6, 6, 3) => 3rd Sunday of June 2023.
            """
            # 1st day of the month
            d = datetime(year, month, 1)
            # What is the weekday of day #1?
            w = d.weekday()  # Monday=0, Tuesday=1, ... Sunday=6
            # If we want, e.g. Sunday=6, we see how many days to add
            delta = (weekday - w) % 7
            # This is the first <weekday> in that month
            first_weekday = d + timedelta(days=delta)
            # Now add 7*(nth-1) days
            return first_weekday + timedelta(days=7 * (nth-1))

        def get_good_friday(year):
            """Good Friday is 2 days before Easter Sunday."""
            return easter(year) - timedelta(days=2)

        def get_easter_monday(year):
            """Easter Monday is 1 day after Easter Sunday."""
            return easter(year) + timedelta(days=1)

        def get_black_friday(year):
            """
            Black Friday = day after US Thanksgiving, 
            and US Thanksgiving is the 4th Thursday in November.
            """
            # 4th Thursday in November
            fourth_thursday = nth_weekday_of_month(year, 11, 3, 4)  # weekday=3 => Thursday
            return fourth_thursday + timedelta(days=1)

        def get_cyber_monday(year):
            """Cyber Monday = Monday after US Thanksgiving, i.e. 4 days after 4th Thursday in Nov."""
            # 4th Thursday in November
            fourth_thursday = nth_weekday_of_month(year, 11, 3, 4)
            return fourth_thursday + timedelta(days=4)  # Monday after Thanksgiving

        # Loop over each year in range
        start_yr = int(start_date[:4])
        end_yr = datetime.today().year

        for yr in range(start_yr, end_yr + 1):
            # Valentines = Feb 14
            valentines_day = datetime(yr, 2, 14)
            # Halloween = Oct 31
            halloween_day  = datetime(yr, 10, 31)
            # Father's Day (US & UK) = 3rd Sunday in June
            fathers_day    = nth_weekday_of_month(yr, 6, 6, 3)  # Sunday=6
            # Mother's Day US = 2nd Sunday in May
            mothers_day_us = nth_weekday_of_month(yr, 5, 6, 2)
            mothering_sunday = easter(yr) - timedelta(days=21)
            # If for some reason that's not a Sunday (rare corner cases), shift to Sunday:
            while mothering_sunday.weekday() != 6:  # Sunday=6
                mothering_sunday -= timedelta(days=1)

            # Good Friday, Easter Monday
            gf = get_good_friday(yr)
            em = get_easter_monday(yr)

            # Black Friday, Cyber Monday
            bf = get_black_friday(yr)
            cm = get_cyber_monday(yr)

            # Mark them in df_daily if in range
            for special_date, col in [
                (valentines_day, "seas_valentines_day"),
                (halloween_day,  "seas_halloween"),
                (fathers_day,    "seas_fathers_day_us_uk"),
                (mothers_day_us, "seas_mothers_day_us"),
                (mothering_sunday, "seas_mothers_day_uk"),
                (gf, "seas_good_friday"),
                (em, "seas_easter_monday"),
                (bf, "seas_black_friday"),
                (cm, "seas_cyber_monday"),
            ]:
                # Convert to pd.Timestamp:
                special_ts = pd.Timestamp(special_date)

                # Only set if it's within your daily range
                if (special_ts >= df_daily["Date"].min()) and (special_ts <= df_daily["Date"].max()):
                    df_daily.loc[df_daily["Date"] == special_ts, col] = 1

        # ---------------------------------------------------------------------
        # 4. Add daily indicators for last day & last Friday of month
        #    Then aggregate them to weekly level using .max()
        # ---------------------------------------------------------------------
        # Last day of month (daily)
        df_daily["seas_last_day_of_month"] = df_daily["Date"].apply(
            lambda d: 1 if d == d.to_period("M").to_timestamp("M") else 0
        )

        # Last Friday of month (daily)
        def is_last_friday(date):
            # last day of the month
            last_day_of_month = date.to_period("M").to_timestamp("M")
            last_day_weekday = last_day_of_month.weekday()  # Monday=0,...Sunday=6
            # Determine how many days we go back from the last day to get Friday (weekday=4)
            if last_day_weekday >= 4:
                days_to_subtract = last_day_weekday - 4
            else:
                days_to_subtract = last_day_weekday + 3
            last_friday = last_day_of_month - pd.Timedelta(days=days_to_subtract)
            return 1 if date == last_friday else 0

        df_daily["seas_last_friday_of_month"] = df_daily["Date"].apply(is_last_friday)

        # ---------------------------------------------------------------------
        # 5. Weekly aggregation for holiday columns & monthly dummies
        # ---------------------------------------------------------------------
        # For monthly dummies, create a daily col "Month", then get_dummies
        df_daily["Month"] = df_daily["Date"].dt.month_name().str.lower()
        df_monthly_dummies = pd.get_dummies(
            df_daily, 
            prefix="seas", 
            columns=["Month"], 
            dtype=int
        )
        # Recalculate 'week_start' (already in df_daily, but just to be sure)
        df_monthly_dummies['week_start'] = df_daily['week_start']

        # Group monthly dummies by .sum() or .mean()—we often spread them across the week
        df_monthly_dummies = (
            df_monthly_dummies
            .groupby('week_start')
            .sum(numeric_only=True)    # sum the daily flags
            .reset_index()
            .rename(columns={'week_start': "Date"})
            .set_index("Date")
        )
        # Spread monthly dummies by 7 to distribute across that week
        monthly_cols = [c for c in df_monthly_dummies.columns if c.startswith("seas_month_")]
        df_monthly_dummies[monthly_cols] = df_monthly_dummies[monthly_cols] / 7

        # Group holiday & special-day columns by .max() => binary at weekly level
        df_holidays = (
            df_daily
            .groupby('week_start')
            .max(numeric_only=True)   # if any day=1 in that week, entire week=1
            .reset_index()
            .rename(columns={'week_start': "Date"})
            .set_index("Date")
        )

        # ---------------------------------------------------------------------
        # 6. Combine weekly start, monthly dummies, holiday flags
        # ---------------------------------------------------------------------
        df_combined = pd.concat([df_weekly_start, df_monthly_dummies], axis=1)
        df_combined = pd.concat([df_combined, df_holidays], axis=1)
        df_combined = df_combined.loc[:, ~df_combined.columns.duplicated()]

        # ---------------------------------------------------------------------
        # 7. Create weekly dummies for Week of Year & yearly dummies
        # ---------------------------------------------------------------------
        df_combined.reset_index(inplace=True)
        df_combined.rename(columns={"index": "old_index"}, inplace=True)  # just in case
        
        df_combined["Week"] = df_combined["Date"].dt.isocalendar().week
        df_combined = pd.get_dummies(df_combined, prefix="seas", columns=["Week"], dtype=int)
        
        df_combined["Year"] = df_combined["Date"].dt.year
        df_combined = pd.get_dummies(df_combined, prefix="seas", columns=["Year"], dtype=int)
        
        # ---------------------------------------------------------------------
        # 8. Add constant & trend
        # ---------------------------------------------------------------------
        df_combined["Constant"] = 1
        df_combined["Trend"] = df_combined.index + 1
        
        # ---------------------------------------------------------------------
        # 9. Rename Date -> OBS and return
        # ---------------------------------------------------------------------
        df_combined.rename(columns={"Date": "OBS"}, inplace=True)
        
        return df_combined

    def pull_weather(self, week_commencing, start_date, country_codes) -> pd.DataFrame:
        """
        Pull weather data for a given week-commencing day and one or more country codes.

        LOGIC:
        1) For non-US countries (AU, GB, DE, CA, ZA):
            - Mesonet => max_temp_f, min_temp_f -> compute mean_temp_f -> weekly average => 'avg_max_temp_f', etc.
            - Open-Meteo => precipitation_sum => 'avg_rain_sum', snowfall_sum => 'avg_snow_sum'.
            - Merge, then rename columns with prefix 'seas_{country}_'.

        2) For the US:
            - We have multiple <STATE>_ASOS networks (e.g. CA_ASOS, TX_ASOS).
            - For each state, fetch from Mesonet => max_temp_f, min_temp_f, precip_in, snow_in -> compute mean_temp_f -> weekly average => 'avg_max_temp_f', 'avg_rain_sum', 'avg_snow_sum', etc.
            - Rename columns for each state with prefix 'seas_us_{state}_'.
            - Merge all states (and countries) into a single DataFrame.

        :param week_commencing: A string in {"mon","tue","wed","thur","fri","sat","sun"}.
        :param country_codes: A list of 2-letter country codes or a single string, e.g. ["GB","US"].
        :return: A single Pandas DataFrame with weekly-aggregated data for all requested countries.
        """
        # ------------------------------------------------------------------ #
        # 0) Handle either a single code or list of codes
        # ------------------------------------------------------------------ #
        if isinstance(country_codes, str):
            country_codes = [country_codes]
        elif not isinstance(country_codes, (list, tuple)):
            raise ValueError("country_codes must be a list/tuple or a single string.")

        # --- Setup / Constants --- #
        day_dict = {"mon": 0, "tue": 1, "wed": 2, "thur": 3, "fri": 4, "sat": 5, "sun": 6}
        # Map each 2-letter code to a key
        country_dict = {
            "US": "US_STATES",
            "CA": "Canada",
            "AU": "AU__ASOS",
            "GB": "GB__ASOS",
            "DE": "DE__ASOS",
            "ZA": "ZA__ASOS"
        }

        # Station-based countries for Mesonet
        station_map = {
            "GB__ASOS": [
                "&stations=EGCC", "&stations=EGNM", "&stations=EGBB", "&stations=EGSH",
                "&stations=EGFF", "&stations=EGHI", "&stations=EGLC", "&stations=EGHQ",
                "&stations=EGAC", "&stations=EGPF", "&stations=EGGD", "&stations=EGPE",
                "&stations=EGNT"
            ],
            "AU__ASOS": [
                "&stations=YPDN", "&stations=YBCS", "&stations=YBBN", "&stations=YSSY",
                "&stations=YSSY", "&stations=YMEN", "&stations=YPAD", "&stations=YPPH"
            ],
            "DE__ASOS": [
                "&stations=EDDL", "&stations=EDDH", "&stations=EDDB", "&stations=EDDN",
                "&stations=EDDF", "&stations=EDDK", "&stations=EDLW", "&stations=EDDM"
            ],
            # Example: if ZA is also station-based, add it here.
            "ZA__ASOS": [
                # If you know the station codes, add them here:
                # e.g. "&stations=FACT", "&stations=FAJS", ...
            ],
            # "FR__ASOS" if you need France, etc.
        }

        # Non-US countries that also fetch RAIN & SNOW from Open-Meteo
        rainfall_city_map = {
            "GB__ASOS": [
                "Manchester", "Leeds", "Birmingham", "London","Glasgow",
            ],
            "AU__ASOS": [
                "Darwin", "Cairns", "Brisbane", "Sydney", "Melbourne", "Adelaide", "Perth"
            ],
            "DE__ASOS": [
                "Dortmund", "Düsseldorf", "Frankfurt", "Munich", "Cologne", "Berlin", "Hamburg", "Nuernberg"
            ],
            "ZA__ASOS": [
                "Johannesburg", "Cape Town", "Durban", "Pretoria"
            ],
        }

        # Canada sub-networks
        institute_vector = [
            "CA_NB_ASOS", "CA_NF_ASOS", "CA_NT_ASOS", "CA_NS_ASOS", "CA_NU_ASOS"
        ]
        stations_list_canada = [
            [
                "&stations=CYQM", "&stations=CERM", "&stations=CZCR",
                "&stations=CZBF", "&stations=CYFC", "&stations=CYCX"
            ],
            [
                "&stations=CWZZ", "&stations=CYDP", "&stations=CYMH", "&stations=CYAY",
                "&stations=CWDO", "&stations=CXTP", "&stations=CYJT", "&stations=CYYR",
                "&stations=CZUM", "&stations=CYWK", "&stations=CYWK"
            ],
            [
                "&stations=CYHI", "&stations=CZCP", "&stations=CWLI", "&stations=CWND",
                "&stations=CXTV", "&stations=CYVL", "&stations=CYCO", "&stations=CXDE",
                "&stations=CYWE", "&stations=CYLK", "&stations=CWID", "&stations=CYRF",
                "&stations=CXYH", "&stations=CYWY", "&stations=CWMT"
            ],
            [
                "&stations=CWEF", "&stations=CXIB", "&stations=CYQY", "&stations=CYPD",
                "&stations=CXNP", "&stations=CXMY", "&stations=CYAW", "&stations=CWKG",
                "&stations=CWVU", "&stations=CXLB", "&stations=CWSA", "&stations=CWRN"
            ],
            [
                "&stations=CYLT", "&stations=CWEU", "&stations=CWGZ", "&stations=CYIO",
                "&stations=CXSE", "&stations=CYCB", "&stations=CWIL", "&stations=CXWB",
                "&stations=CYZS", "&stations=CWJC", "&stations=CYFB", "&stations=CWUW"
            ]
        ]

        # US states and stations - each sub-network
        us_state_networks = {
            state: f"{state}_ASOS" for state in [
                "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "IA", "ID", "IL", "IN", 
                "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", 
                "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD", 
                "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"
            ]
        }
        
        us_stations_map = {
            "AL_ASOS": ["&stations=BHM", "&stations=HSV", "&stations=MGM", "&stations=MOB", "&stations=TCL"],
            "AR_ASOS": ["&stations=LIT", "&stations=FSM", "&stations=TXK", "&stations=HOT", "&stations=FYV"],
            "AZ_ASOS": ["&stations=PHX", "&stations=TUS", "&stations=FLG", "&stations=YUM", "&stations=PRC"],
            "CA_ASOS": ["&stations=LAX", "&stations=SAN", "&stations=SJC", "&stations=SFO", "&stations=FAT"],
            "CO_ASOS": ["&stations=DEN", "&stations=COS", "&stations=GJT", "&stations=PUB", "&stations=ASE"],
            "CT_ASOS": ["&stations=BDL", "&stations=HVN", "&stations=BDR", "&stations=GON", "&stations=HFD"],
            "DE_ASOS": ["&stations=ILG", "&stations=GED", "&stations=DOV"],
            "FL_ASOS": ["&stations=MIA", "&stations=TPA", "&stations=ORL", "&stations=JAX", "&stations=TLH"],
            "GA_ASOS": ["&stations=ATL", "&stations=SAV", "&stations=CSG", "&stations=MCN", "&stations=AGS"],
            "IA_ASOS": ["&stations=DSM", "&stations=CID", "&stations=DBQ", "&stations=ALO", "&stations=SUX"],
            "ID_ASOS": ["&stations=BOI", "&stations=IDA", "&stations=PIH", "&stations=SUN", "&stations=COE"],
            "IL_ASOS": ["&stations=ORD", "&stations=MDW", "&stations=PIA", "&stations=SPI", "&stations=MLI"],
            "IN_ASOS": ["&stations=IND", "&stations=FWA", "&stations=SBN", "&stations=EVV", "&stations=HUF"],
            "KS_ASOS": ["&stations=ICT", "&stations=FOE", "&stations=GCK", "&stations=HYS", "&stations=SLN"],
            "KY_ASOS": ["&stations=SDF", "&stations=LEX", "&stations=CVG", "&stations=PAH", "&stations=BWG"],
            "LA_ASOS": ["&stations=MSY", "&stations=SHV", "&stations=LFT", "&stations=BTR", "&stations=MLU"],
            "MA_ASOS": ["&stations=BOS", "&stations=ORH", "&stations=HYA", "&stations=ACK", "&stations=BED"],
            "MD_ASOS": ["&stations=BWI", "&stations=MTN", "&stations=SBY", "&stations=HGR", "&stations=ADW"],
            "ME_ASOS": ["&stations=PWM", "&stations=BGR", "&stations=CAR", "&stations=PQI", "&stations=RKD"],
            "MI_ASOS": ["&stations=DTW", "&stations=GRR", "&stations=FNT", "&stations=LAN", "&stations=MKG"],
            "MN_ASOS": ["&stations=MSP", "&stations=DLH", "&stations=RST", "&stations=STC", "&stations=INL"],
            "MO_ASOS": ["&stations=STL", "&stations=MCI", "&stations=SGF", "&stations=COU", "&stations=JLN"],
            "MS_ASOS": ["&stations=JAN", "&stations=GPT", "&stations=MEI", "&stations=PIB", "&stations=GLH"],
            "MT_ASOS": ["&stations=BIL", "&stations=MSO", "&stations=GTF", "&stations=HLN", "&stations=BZN"],
            "NC_ASOS": ["&stations=CLT", "&stations=RDU", "&stations=GSO", "&stations=ILM", "&stations=AVL"],
            "ND_ASOS": ["&stations=BIS", "&stations=FAR", "&stations=GFK", "&stations=ISN", "&stations=JMS"],
            "NE_ASOS": ["&stations=OMA"],
            "NH_ASOS": ["&stations=MHT", "&stations=PSM", "&stations=CON", "&stations=LEB", "&stations=ASH"],
            "NJ_ASOS": ["&stations=EWR", "&stations=ACY", "&stations=TTN", "&stations=MMU", "&stations=TEB"],
            "NM_ASOS": ["&stations=ABQ", "&stations=SAF", "&stations=ROW", "&stations=HOB", "&stations=FMN"],
            "NV_ASOS": ["&stations=LAS"],
            "NY_ASOS": ["&stations=JFK", "&stations=LGA", "&stations=BUF", "&stations=ALB", "&stations=SYR"],
            "OH_ASOS": ["&stations=CMH"],
            "OK_ASOS": ["&stations=OKC", "&stations=TUL", "&stations=LAW", "&stations=SWO", "&stations=PNC"],
            "OR_ASOS": ["&stations=PDX"],
            "PA_ASOS": ["&stations=PHL", "&stations=PIT", "&stations=ERI", "&stations=MDT", "&stations=AVP"],
            "RI_ASOS": ["&stations=PVD", "&stations=WST", "&stations=UUU"],
            "SC_ASOS": ["&stations=CHS", "&stations=CAE", "&stations=GSP", "&stations=MYR", "&stations=FLO"],
            "SD_ASOS": ["&stations=FSD", "&stations=RAP", "&stations=PIR", "&stations=ABR", "&stations=YKN"],
            "TN_ASOS": ["&stations=BNA", "&stations=MEM", "&stations=TYS", "&stations=CHA", "&stations=TRI"],
            "TX_ASOS": ["&stations=DFW", "&stations=IAH", "&stations=AUS", "&stations=SAT", "&stations=ELP"],
            "UT_ASOS": ["&stations=SLC", "&stations=OGD", "&stations=PVU", "&stations=SGU", "&stations=CNY"],
            "VA_ASOS": ["&stations=DCA", "&stations=RIC", "&stations=ROA", "&stations=ORF", "&stations=SHD"],
            "VT_ASOS": ["&stations=BTV", "&stations=MPV", "&stations=RUT", "&stations=VSF", "&stations=MVL"],
            "WA_ASOS": ["&stations=SEA", "&stations=GEG", "&stations=TIW", "&stations=VUO", "&stations=BFI"],
            "WI_ASOS": ["&stations=MKE", "&stations=MSN", "&stations=GRB", "&stations=EAU", "&stations=LSE"],
            "WV_ASOS": ["&stations=CRW", "&stations=CKB", "&stations=HTS", "&stations=MGW", "&stations=BKW"],
            "WY_ASOS": ["&stations=CPR", "&stations=JAC", "&stations=SHR", "&stations=COD", "&stations=RKS"],
        }
        # --- Date setup --- #
        date_object = datetime.strptime(start_date, "%Y-%m-%d")
        start_day = date_object.day
        start_month = date_object.month
        start_year = date_object.year
        formatted_date = f"{start_year:04d}-01-01"  # "2000-01-01"
        today = datetime.now()
        end_day, end_month, end_year = today.day, today.month, today.year

        # ------------------------------------------------------------------ #
        # Utility functions
        # ------------------------------------------------------------------ #
        def convert_f_to_c(series_f: pd.Series) -> pd.Series:
            """Convert Fahrenheit to Celsius."""
            return (series_f - 32) * 5.0 / 9.0

        def fetch_mesonet_data(network: str, stations: list) -> pd.DataFrame:
            """Fetch station-based data (daily) from Iowa Mesonet."""
            import csv

            station_query = ''.join(stations)
            url = (
                "https://mesonet.agron.iastate.edu/cgi-bin/request/daily.py?"
                f"network={network}{station_query}"
                f"&year1={start_year}&month1={start_month}&day1={start_day}"
                f"&year2={end_year}&month2={end_month}&day2={end_day}"
            )
            with urllib.request.urlopen(url) as f:
                df = pd.read_csv(f, dtype=str, quoting=csv.QUOTE_ALL)
            return df

        def fetch_canada_data() -> pd.DataFrame:
            """Canada uses multiple sub-networks. Combine them all."""
            import csv
            final_df = pd.DataFrame()
            for i, institute_temp in enumerate(institute_vector):
                station_query_temp = ''.join(stations_list_canada[i])
                mesonet_url = (
                    "https://mesonet.agron.iastate.edu/cgi-bin/request/daily.py?"
                    f"network={institute_temp}{station_query_temp}"
                    f"&year1={start_year}&month1={start_month}&day1={start_day}"
                    f"&year2={end_year}&month2={end_month}&day2={end_day}"
                )
                with urllib.request.urlopen(mesonet_url) as f:
                    temp_df = pd.read_csv(f, dtype=str, quoting=csv.QUOTE_ALL)

                if not temp_df.empty:
                    final_df = pd.concat([final_df, temp_df], ignore_index=True)
            return final_df

        def fetch_openmeteo_rain_snow(cities: list) -> pd.DataFrame:
            """
            Fetch daily precipitation_sum (rain) and snowfall_sum (snow) from Open-Meteo.
            Returns columns: ["date", "rain_sum", "snow_sum", "city"] for each day.
            We'll then do a weekly aggregator that yields avg_rain_sum, avg_snow_sum.
            """
            weather_data_list = []
            geolocator = Nominatim(user_agent="MyApp")

            for city in cities:
                loc = geolocator.geocode(city)
                if not loc:
                    print(f"Could not find location for {city}, skipping.")
                    continue

                url = "https://archive-api.open-meteo.com/v1/archive"
                params = {
                    "latitude": loc.latitude,
                    "longitude": loc.longitude,
                    "start_date": formatted_date,
                    "end_date": today.strftime("%Y-%m-%d"),
                    "daily": "precipitation_sum,snowfall_sum",
                    "timezone": "auto"
                }
                resp = requests.get(url, params=params)
                if resp.status_code != 200:
                    print(f"[ERROR] open-meteo returned status {resp.status_code} for city={city}")
                    continue
                try:
                    data_json = resp.json()
                except ValueError:
                    print(f"[ERROR] invalid JSON from open-meteo for city={city}")
                    continue

                daily_block = data_json.get("daily", {})
                if not {"time", "precipitation_sum", "snowfall_sum"}.issubset(daily_block.keys()):
                    print(f"[ERROR] missing required keys in open-meteo for city={city}")
                    continue

                df_temp = pd.DataFrame({
                    "date": daily_block["time"],
                    "rain_sum": daily_block["precipitation_sum"],
                    "snow_sum": daily_block["snowfall_sum"]
                })
                df_temp["city"] = city
                weather_data_list.append(df_temp)

            if weather_data_list:
                return pd.concat(weather_data_list, ignore_index=True)
            else:
                return pd.DataFrame()

        def weekly_aggregate_temp_mesonet(df: pd.DataFrame) -> pd.DataFrame:
            """
            For NON-US mesonet data, we only keep max_temp_f, min_temp_f,
            then compute mean_temp_f, plus Celsius, and do weekly average.
            """
            import pandas as pd

            # Convert day col
            if "day" not in df.columns:
                return pd.DataFrame()

            # Only keep relevant columns
            keep_cols = []
            for c in ["day", "max_temp_f", "min_temp_f"]:
                if c in df.columns:
                    keep_cols.append(c)
            df = df[keep_cols].copy()

            # Convert "None" => numeric
            for c in ["max_temp_f", "min_temp_f"]:
                if c in df.columns:
                    df[c] = df[c].replace("None", pd.NA)
                    df[c] = pd.to_numeric(df[c], errors="coerce")

            df["day"] = pd.to_datetime(df["day"], errors="coerce")
            df["mean_temp_f"] = (df["max_temp_f"] + df["min_temp_f"]) / 2
            df["max_temp_c"] = convert_f_to_c(df["max_temp_f"])
            df["min_temp_c"] = convert_f_to_c(df["min_temp_f"])
            df["mean_temp_c"] = convert_f_to_c(df["mean_temp_f"])

            # Group by "week_starting"
            df["week_starting"] = df["day"].apply(
                lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7)
                if pd.notnull(x) else pd.NaT
            )
            numeric_cols = df.select_dtypes(include='number').columns
            weekly = df.groupby("week_starting")[numeric_cols].mean()

            # Rename columns
            rename_map = {
                "max_temp_f": "avg_max_temp_f",
                "min_temp_f": "avg_min_temp_f",
                "mean_temp_f": "avg_mean_temp_f",
                "max_temp_c": "avg_max_temp_c",
                "min_temp_c": "avg_min_temp_c",
                "mean_temp_c": "avg_mean_temp_c",
            }
            weekly.rename(columns=rename_map, inplace=True)

            # Return as a DataFrame w/ index = week_starting
            return weekly

        def weekly_aggregate_rain_snow_openmeteo(df: pd.DataFrame) -> pd.DataFrame:
            """
            For NON-US, from open-meteo, we have daily columns 'date','rain_sum','snow_sum'.
            We'll do weekly average of each. -> 'avg_rain_sum', 'avg_snow_sum'.
            """
            import pandas as pd
            if "date" not in df.columns:
                return pd.DataFrame()

            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df["week_starting"] = df["date"].apply(
                lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7)
                if pd.notnull(x) else pd.NaT
            )

            # Convert to numeric
            for c in ["rain_sum", "snow_sum"]:
                if c in df.columns:
                    df[c] = pd.to_numeric(df[c], errors="coerce")

            numeric_cols = df.select_dtypes(include='number').columns
            weekly = df.groupby("week_starting")[numeric_cols].mean()

            rename_map = {
                "rain_sum": "avg_rain_sum",
                "snow_sum": "avg_snow_sum"
            }
            weekly.rename(columns=rename_map, inplace=True)
            return weekly

        def weekly_aggregate_us(df: pd.DataFrame) -> pd.DataFrame:
            """
            For US Mesonet data (per state), we keep max_temp_f, min_temp_f, precip_in, snow_in,
            then compute mean_temp_f & convert to celsius, group weekly.
            We'll rename:
            max_temp_f -> avg_max_temp_f
            min_temp_f -> avg_min_temp_f
            mean_temp_f -> avg_mean_temp_f
            precip_in -> avg_rain_sum
            snow_in -> avg_snow_sum
            """
            import pandas as pd
            if "day" not in df.columns:
                return pd.DataFrame()

            # Convert day
            df["day"] = pd.to_datetime(df["day"], errors="coerce")

            # Convert "None" => numeric
            for c in ["max_temp_f", "min_temp_f", "precip_in", "snow_in"]:
                if c in df.columns:
                    df[c] = df[c].replace("None", pd.NA)
                    df[c] = pd.to_numeric(df[c], errors="coerce")

            # Compute mean_temp_f, celsius
            df["mean_temp_f"] = (df["max_temp_f"] + df["min_temp_f"]) / 2
            df["max_temp_c"] = convert_f_to_c(df["max_temp_f"])
            df["min_temp_c"] = convert_f_to_c(df["min_temp_f"])
            df["mean_temp_c"] = convert_f_to_c(df["mean_temp_f"])

            # Weekly grouping
            df["week_starting"] = df["day"].apply(
                lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7)
                if pd.notnull(x) else pd.NaT
            )
            numeric_cols = df.select_dtypes(include='number').columns
            weekly = df.groupby("week_starting")[numeric_cols].mean()

            rename_map = {
                "max_temp_f": "avg_max_temp_f",
                "min_temp_f": "avg_min_temp_f",
                "mean_temp_f": "avg_mean_temp_f",
                "max_temp_c": "avg_max_temp_c",
                "min_temp_c": "avg_min_temp_c",
                "mean_temp_c": "avg_mean_temp_c",
                "precip_in": "avg_rain_sum",
                "snow_in": "avg_snow_sum"
            }
            weekly.rename(columns=rename_map, inplace=True)
            return weekly

        def rename_with_prefix(df: pd.DataFrame, prefix: str) -> pd.DataFrame:
            """Rename all columns except 'week_starting' or 'OBS' with the given prefix."""
            df2 = df.copy()
            new_cols = {}
            for col in df2.columns:
                if col not in ["week_starting", "OBS"]:
                    new_cols[col] = prefix + col
            df2.rename(columns=new_cols, inplace=True)
            return df2

        # ------------------------------------------------------------------ #
        # The final combined DataFrame
        # ------------------------------------------------------------------ #
        combined_df = pd.DataFrame()

        # ------------------------------------------------------------------ #
        # 1) Loop over each requested country
        # ------------------------------------------------------------------ #
        for country_code in country_codes:
            net = country_dict.get(country_code)
            if net is None:
                print(f"Warning: Invalid country_code '{country_code}' – skipping.")
                continue

            # =========================
            # 2) Special Logic for US
            # =========================
            if net == "US_STATES":
                for state_code, network_code in us_state_networks.items():
                    stations = us_stations_map.get(network_code, [])
                    if not stations:
                        print(f"[DEBUG] No stations for {network_code}, skipping.")
                        continue

                    raw_df = fetch_mesonet_data(network_code, stations)
                    if raw_df.empty:
                        print(f"[DEBUG] DataFrame empty for {network_code}, skipping.")
                        continue

                    weekly_state = weekly_aggregate_us(raw_df)
                    if weekly_state.empty:
                        print(f"[DEBUG] Aggregated weekly DataFrame empty for {network_code}, skipping.")
                        continue

                    weekly_state.reset_index(inplace=True)
                    weekly_state.rename(columns={"week_starting": "OBS"}, inplace=True)

                    # Now rename columns with prefix: seas_us_{statecode}_
                    prefix = f"seas_us_{state_code.lower()}_"
                    weekly_state = rename_with_prefix(weekly_state, prefix)

                    # Merge into combined
                    if combined_df.empty:
                        combined_df = weekly_state
                    else:
                        combined_df = pd.merge(combined_df, weekly_state, on="OBS", how="outer")

                # Done with the US. Move on to the next country in the loop
                continue

            # =======================================
            # 3) Logic for Non-US (AU, GB, DE, CA, ZA)
            # =======================================
            # A) Fetch temperature data from Mesonet
            if net == "Canada":
                raw_temp = fetch_canada_data()
            else:
                # e.g. "GB__ASOS", "AU__ASOS", "DE__ASOS", "ZA__ASOS" (if added)
                stations = station_map.get(net, [])
                if not stations and net != "ZA__ASOS":
                    # If we have no stations for net and it's not ZA,
                    # there's no data. (If ZA has stations, add them above.)
                    raw_temp = pd.DataFrame()
                else:
                    raw_temp = fetch_mesonet_data(net, stations)

            weekly_temp = pd.DataFrame()
            if not raw_temp.empty:
                # For these countries, we only keep max_temp_f, min_temp_f, mean_temp_f
                weekly_temp = weekly_aggregate_temp_mesonet(raw_temp)

            # B) Fetch rain+snow from Open-Meteo (only if we have an entry in rainfall_city_map)
            weekly_precip = pd.DataFrame()
            if net in rainfall_city_map:
                city_list = rainfall_city_map[net]
                df_rain_snow = fetch_openmeteo_rain_snow(city_list)
                if not df_rain_snow.empty:
                    weekly_precip = weekly_aggregate_rain_snow_openmeteo(df_rain_snow)

            # C) Merge the temperature data + precip/snow data on the weekly index
            if not weekly_temp.empty and not weekly_precip.empty:
                merged_df = pd.merge(weekly_temp, weekly_precip, left_index=True, right_index=True, how="outer")
            elif not weekly_temp.empty:
                merged_df = weekly_temp
            else:
                merged_df = weekly_precip

            if merged_df.empty:
                print(f"No data retrieved for country: {country_code}")
                continue

            # D) Convert index -> a column OBS
            merged_df.reset_index(inplace=True)
            merged_df.rename(columns={"week_starting": "OBS"}, inplace=True)

            # E) Rename with prefix = "seas_{country_code}_"
            prefix = f"seas_{country_code.lower()}_"
            merged_df = rename_with_prefix(merged_df, prefix)

            # F) Merge into combined_df
            if combined_df.empty:
                combined_df = merged_df
            else:
                combined_df = pd.merge(combined_df, merged_df, on="OBS", how="outer")

        # ------------------------------------------------------------------ #
        # 4) Sort final by OBS (optional)
        # ------------------------------------------------------------------ #
        if not combined_df.empty:
            combined_df.sort_values(by="OBS", inplace=True)

        return combined_df
        
    def pull_macro_ons_uk(self, cdid_list=None, week_start_day="mon", sector=None):
        """
        Fetches time series data for multiple CDIDs from the ONS API, converts it to daily frequency, 
        aggregates it to weekly averages, and renames variables based on specified rules.

        Parameters:
            cdid_list (list): A list of additional CDIDs to fetch (e.g., ['JP9Z', 'UKPOP']). Defaults to None.
            week_start_day (str): The day the week starts on (e.g., 'Monday', 'Sunday').
            sector (str): The sector for which the standard CDIDs are fetched (e.g., 'fast_food', 'retail').

        Returns:
            pd.DataFrame: A DataFrame with weekly frequency, containing a 'week_commencing' column 
                        and all series as renamed columns.
        """
        # Define CDIDs for sectors and defaults
        sector_cdids = {
            "fast_food": ["L7TD", "L78Q", "DOAD"],
            "default": ["D7G7", "MGSX", "UKPOP", "IHYQ", "YBEZ", "MS77"],
        }

        default_cdids = sector_cdids["default"]
        sector_specific_cdids = sector_cdids.get(sector, [])
        standard_cdids = list(set(default_cdids + sector_specific_cdids))  # Avoid duplicates

        # Combine standard CDIDs and additional CDIDs
        if cdid_list is None:
            cdid_list = []
        cdid_list = list(set(standard_cdids + cdid_list))  # Avoid duplicates

        base_search_url = "https://api.beta.ons.gov.uk/v1/search?content_type=timeseries&cdids="
        base_data_url = "https://api.beta.ons.gov.uk/v1/data?uri="
        combined_df = pd.DataFrame()

        # Map week start day to pandas weekday convention
        days_map = {"mon": 0, "tue": 1, "wed": 2, "thur": 3, "fri": 4, "sat": 5, "sun": 6}
        if week_start_day not in days_map:
            raise ValueError("Invalid week start day. Choose from: " + ", ".join(days_map.keys()))
        week_start = days_map[week_start_day]

        for cdid in cdid_list:
            try:
                # Search for the series
                search_url = f"{base_search_url}{cdid}"
                search_response = requests.get(search_url)
                search_response.raise_for_status()
                search_data = search_response.json()

                items = search_data.get("items", [])
                if not items:
                    print(f"No data found for CDID: {cdid}")
                    continue

                # Extract series name and latest release URI
                series_name = items[0].get("title", f"Series_{cdid}")
                latest_date = max(
                    datetime.fromisoformat(item["release_date"].replace("Z", "+00:00"))
                    for item in items if "release_date" in item
                )
                latest_uri = next(
                    item["uri"] for item in items
                    if "release_date" in item and datetime.fromisoformat(item["release_date"].replace("Z", "+00:00")) == latest_date
                )

                # Fetch the dataset
                data_url = f"{base_data_url}{latest_uri}"
                data_response = requests.get(data_url)
                data_response.raise_for_status()
                data_json = data_response.json()

                # Detect the frequency and process accordingly
                if "months" in data_json and data_json["months"]:
                    frequency_key = "months"
                elif "quarters" in data_json and data_json["quarters"]:
                    frequency_key = "quarters"
                elif "years" in data_json and data_json["years"]:
                    frequency_key = "years"
                else:
                    print(f"Unsupported frequency or no data for CDID: {cdid}")
                    continue

                # Prepare the DataFrame
                df = pd.DataFrame(data_json[frequency_key])

                # Parse the 'date' field based on frequency
                if frequency_key == "months":
                    df["date"] = pd.to_datetime(df["date"], format="%Y %b", errors="coerce")
                elif frequency_key == "quarters":
                    def parse_quarter(quarter_str):
                        year, qtr = quarter_str.split(" Q")
                        month = {"1": 1, "2": 4, "3": 7, "4": 10}[qtr]
                        return datetime(int(year), month, 1)
                    df["date"] = df["date"].apply(parse_quarter)
                elif frequency_key == "years":
                    df["date"] = pd.to_datetime(df["date"], format="%Y", errors="coerce")

                df["value"] = pd.to_numeric(df["value"], errors="coerce")
                df.rename(columns={"value": series_name}, inplace=True)

                # Combine data
                df = df.loc[:, ["date", series_name]].dropna().reset_index(drop=True)
                if combined_df.empty:
                    combined_df = df
                else:
                    combined_df = pd.merge(combined_df, df, on="date", how="outer")

            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for CDID {cdid}: {e}")
            except (KeyError, ValueError) as e:
                print(f"Error processing data for CDID {cdid}: {e}")

        if not combined_df.empty:
            min_date = combined_df["date"].min()
            max_date = datetime.today()
            date_range = pd.date_range(start=min_date, end=max_date, freq='D')
            daily_df = pd.DataFrame(date_range, columns=['date'])
            daily_df = pd.merge(daily_df, combined_df, on="date", how="left")
            daily_df = daily_df.ffill()

            # Aggregate to weekly frequency
            daily_df["week_commencing"] = daily_df["date"] - pd.to_timedelta((daily_df["date"].dt.weekday - week_start) % 7, unit='D')
            weekly_df = daily_df.groupby("week_commencing").mean(numeric_only=True).reset_index()

            def clean_column_name(name):
                name = re.sub(r"\(.*?\)", "", name)
                name = re.split(r":", name)[0]
                name = re.sub(r"\d+", "", name)
                name = re.sub(r"\b(annual|rate)\b", "", name, flags=re.IGNORECASE)
                name = re.sub(r"[^\w\s]", "", name)
                name = name.replace(" ", "_")
                name = re.sub(r"_+", "_", name)
                name = name.rstrip("_")
                return f"macro_{name.lower()}_uk"

            weekly_df.columns = [clean_column_name(col) if col != "week_commencing" else col for col in weekly_df.columns]
            weekly_df.rename(columns={"week_commencing": "OBS"}, inplace=True)

            weekly_df = weekly_df.fillna(0)

            return weekly_df
        else:
            print("No data available to process.")
            return pd.DataFrame()

    def pull_yfinance(self, tickers=None, week_start_day="mon"):
        """
        Fetches stock data for multiple tickers from Yahoo Finance, converts it to daily frequency, 
        aggregates it to weekly averages, and renames variables.

        Parameters:
            tickers (list): A list of additional stock tickers to fetch (e.g., ['AAPL', 'MSFT']). Defaults to None.
            week_start_day (str): The day the week starts on (e.g., 'Monday', 'Sunday').

        Returns:
            pd.DataFrame: A DataFrame with weekly frequency, containing an 'OBS' column 
                        and aggregated stock data for the specified tickers, with NaN values filled with 0.
        """
        # Define default tickers
        default_tickers = ["^FTSE", "GBPUSD=X", "GBPEUR=X", "^GSPC"]

        # Combine default tickers with additional ones
        if tickers is None:
            tickers = []
        tickers = list(set(default_tickers + tickers))  # Ensure no duplicates

        # Automatically set end_date to today
        end_date = datetime.today().strftime("%Y-%m-%d")
        
        # Mapping week start day to pandas weekday convention
        days_map = {"mon": 0, "tue": 1, "wed": 2, "thur": 3, "fri": 4, "sat": 5, "sun": 6}
        if week_start_day not in days_map:
            raise ValueError("Invalid week start day. Choose from: " + ", ".join(days_map.keys()))
        week_start = days_map[week_start_day]

        # Fetch data for all tickers without specifying a start date to get all available data
        data = yf.download(tickers, end=end_date, group_by="ticker", auto_adjust=True)
        
        # Process the data
        combined_df = pd.DataFrame()
        for ticker in tickers:
            try:
                # Extract the ticker's data
                ticker_data = data[ticker] if len(tickers) > 1 else data
                ticker_data = ticker_data.reset_index()

                # Ensure necessary columns are present
                if "Close" not in ticker_data.columns:
                    raise ValueError(f"Ticker {ticker} does not have 'Close' price data.")
                
                # Keep only relevant columns
                ticker_data = ticker_data[["Date", "Close"]]
                ticker_data.rename(columns={"Close": ticker}, inplace=True)

                # Merge data
                if combined_df.empty:
                    combined_df = ticker_data
                else:
                    combined_df = pd.merge(combined_df, ticker_data, on="Date", how="outer")

            except KeyError:
                print(f"Data for ticker {ticker} not available.")
            except Exception as e:
                print(f"Error processing ticker {ticker}: {e}")

        if not combined_df.empty:
            # Convert to daily frequency
            combined_df["Date"] = pd.to_datetime(combined_df["Date"])
            combined_df.set_index("Date", inplace=True)

            # Fill missing dates
            min_date = combined_df.index.min()
            max_date = combined_df.index.max()
            daily_index = pd.date_range(start=min_date, end=max_date, freq='D')
            combined_df = combined_df.reindex(daily_index)
            combined_df.index.name = "Date"
            combined_df = combined_df.ffill()

            # Aggregate to weekly frequency
            combined_df["OBS"] = combined_df.index - pd.to_timedelta((combined_df.index.weekday - week_start) % 7, unit="D")
            weekly_df = combined_df.groupby("OBS").mean(numeric_only=True).reset_index()

            # Fill NaN values with 0
            weekly_df = weekly_df.fillna(0)

            # Clean column names
            def clean_column_name(name):
                name = re.sub(r"[^\w\s]", "", name)
                return f"macro_{name.lower()}"

            weekly_df.columns = [clean_column_name(col) if col != "OBS" else col for col in weekly_df.columns]

            return weekly_df

        else:
            print("No data available to process.")
            return pd.DataFrame()
        
    def pull_sports_events(self, start_date="2020-01-01", week_commencing="mon"):
        """
        Combines scraping logic for:
        - UEFA Champions League and NFL from TheSportsDB (website-scraping approach)
        - FIFA World Cup, UEFA Euro, Rugby World Cup, Six Nations (via TheSportsDB API)

        Returns a single merged DataFrame with all event dummy variables.
        """

        ############################################################
        # 1) SCRAPE UEFA CHAMPIONS LEAGUE & NFL (YOUR FIRST FUNCTION)
        ############################################################
        def scrape_sports_events(start_date=start_date, week_commencing=week_commencing):
            sports = {
                "uefa_champions_league": {
                    "league_id": "4480",
                    "seasons_url": "https://www.thesportsdb.com/league/4480-UEFA-Champions-League?a=1#allseasons",
                    "season_url_template": "https://www.thesportsdb.com/season/4480-UEFA-Champions-League/{season}&all=1&view=",
                    "round_filters": ["quarter", "semi", "final"]
                },
                "nfl": {
                    "league_id": "4391",
                    "seasons_url": "https://www.thesportsdb.com/league/4391-NFL?a=1#allseasons",
                    "season_url_template": "https://www.thesportsdb.com/season/4391-NFL/{season}&all=1&view=",
                    "round_filters": ["quarter", "semi", "final"]
                }
            }

            headers = {"User-Agent": "Mozilla/5.0"}
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")

            # Create a full date range DataFrame
            full_date_range = pd.date_range(start=start_date, end=pd.to_datetime("today"))
            time_series_df = pd.DataFrame({"date": full_date_range})
            time_series_df["seas_uefa_champions_league"] = 0
            time_series_df["seas_nfl"] = 0

            for sport, details in sports.items():
                # Get available seasons
                response = requests.get(details["seasons_url"], headers=headers)
                if response.status_code != 200:
                    continue  # Skip this sport if the request fails

                soup = BeautifulSoup(response.text, "html.parser")

                # Extract season names
                seasons = []
                for link in soup.find_all("a", href=True):
                    href = link["href"]
                    if "season" in href and sport.replace("_", "-") in href.lower():
                        season_name = href.split("/")[-1]  # e.g. "2023-2024"
                        try:
                            season_start_year = int(season_name.split("-")[0])
                            season_start_date = datetime(season_start_year, 1, 1)
                            if season_start_date >= start_date_dt:
                                seasons.append(season_name)
                        except ValueError:
                            continue

                # Scrape matches for filtered seasons
                filtered_matches = []
                for season in seasons:
                    season_url = details["season_url_template"].format(season=season)
                    season_response = requests.get(season_url, headers=headers)
                    if season_response.status_code != 200:
                        continue

                    season_soup = BeautifulSoup(season_response.text, "html.parser")
                    for row in season_soup.find_all("tr"):
                        cols = row.find_all("td")
                        if len(cols) >= 5:
                            match_date = cols[0].text.strip()
                            round_name = cols[1].text.strip().lower()
                            try:
                                match_date_dt = datetime.strptime(match_date, "%d %b %y")
                                if (match_date_dt >= start_date_dt 
                                    and any(r in round_name for r in details["round_filters"])):
                                    filtered_matches.append(match_date_dt)
                            except ValueError:
                                continue

                # Convert matches into time series format
                df_sport = pd.DataFrame({"date": filtered_matches})
                if df_sport.empty:
                    continue

                col_name = "seas_nfl" if sport == "nfl" else "seas_uefa_champions_league"
                time_series_df.loc[time_series_df["date"].isin(df_sport["date"]), col_name] = 1

            # Aggregate by week commencing
            day_offsets = {
                'mon': 'W-MON',
                'tues': 'W-TUE',
                'wed': 'W-WED',
                'thurs': 'W-THU',
                'fri': 'W-FRI',
                'sat': 'W-SAT',
                'sun': 'W-SUN'
            }
            if week_commencing.lower() not in day_offsets:
                raise ValueError(f"Invalid week_commencing value: {week_commencing}. Must be one of {list(day_offsets.keys())}.")

            time_series_df = (time_series_df
                            .set_index("date")
                            .resample(day_offsets[week_commencing.lower()])
                            .max()
                            .reset_index())

            time_series_df.rename(columns={"date": "OBS"}, inplace=True)
            time_series_df.fillna(0, inplace=True)

            return time_series_df

        ############################################################
        # 2) FETCH FIFA WC, UEFA EURO, RUGBY, SIX NATIONS (2ND FUNC)
        ############################################################
        def fetch_events(start_date=start_date, week_commencing=week_commencing):
            # Initialize date range
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.today()
            date_range = pd.date_range(start=start_date_obj, end=end_date_obj)
            df = pd.DataFrame({'OBS': date_range}).set_index('OBS')

            # Define columns for sports
            event_columns = {
                'seas_fifa_world_cup': {
                    'league_id': 4429, 'start_year': 1950, 'interval': 4
                },
                'seas_uefa_european_championship': {
                    'league_id': 4502, 'start_year': 1960, 'interval': 4, 'extra_years': [2021]
                },
                'seas_rugby_world_cup': {
                    'league_id': 4574, 'start_year': 1987, 'interval': 4
                },
                'seas_six_nations': {
                    'league_id': 4714, 'start_year': 2000, 'interval': 1
                },
            }

            # Initialize columns
            for col in event_columns.keys():
                df[col] = 0

            def fetch_league_events(league_id, column_name, start_year, interval, extra_years=None):
                extra_years = extra_years or []
                # Fetch seasons
                seasons_url = f"https://www.thesportsdb.com/api/v1/json/3/search_all_seasons.php?id={league_id}"
                seasons_response = requests.get(seasons_url)
                if seasons_response.status_code != 200:
                    return  # Skip on failure

                seasons_data = seasons_response.json().get('seasons', [])
                for season in seasons_data:
                    season_name = season.get('strSeason', '')
                    if not season_name.isdigit():
                        continue

                    year = int(season_name)
                    # Check if the year is valid for this competition
                    if year in extra_years or (year >= start_year and (year - start_year) % interval == 0):
                        # Fetch events
                        events_url = f"https://www.thesportsdb.com/api/v1/json/3/eventsseason.php?id={league_id}&s={season_name}"
                        events_response = requests.get(events_url)
                        if events_response.status_code != 200:
                            continue

                        events_data = events_response.json().get('events', [])
                        for event in events_data:
                            event_date_str = event.get('dateEvent')
                            if event_date_str:
                                event_date = datetime.strptime(event_date_str, '%Y-%m-%d')
                                if event_date in df.index:
                                    df.loc[event_date, column_name] = 1

            # Fetch events for all defined leagues
            for column_name, params in event_columns.items():
                fetch_league_events(
                    league_id=params['league_id'],
                    column_name=column_name,
                    start_year=params['start_year'],
                    interval=params['interval'],
                    extra_years=params.get('extra_years', [])
                )

            # Resample by week
            day_offsets = {
                'mon': 'W-MON',
                'tues': 'W-TUE',
                'wed': 'W-WED',
                'thurs': 'W-THU',
                'fri': 'W-FRI',
                'sat': 'W-SAT',
                'sun': 'W-SUN'
            }

            if week_commencing.lower() not in day_offsets:
                raise ValueError(
                    f"Invalid week_commencing value: {week_commencing}. "
                    f"Must be one of {list(day_offsets.keys())}."
                )

            df = df.resample(day_offsets[week_commencing.lower()]).max()
            df = df.reset_index()
            return df

        ###################################################
        # 3) CALL BOTH, THEN MERGE ON "OBS" & FILL WITH 0s
        ###################################################
        df_uefa_nfl = scrape_sports_events(start_date, week_commencing)
        df_other_events = fetch_events(start_date, week_commencing)

        # Merge on "OBS" column (outer join to preserve all dates in range)
        final_df = pd.merge(df_uefa_nfl, df_other_events, on='OBS', how='outer')

        # Fill any NaNs with 0 for event columns
        # (Only fill numeric columns or everything except 'OBS')
        for col in final_df.columns:
            if col != 'OBS':
                final_df[col] = final_df[col].fillna(0)

        # Sort by date just in case
        final_df.sort_values(by='OBS', inplace=True)
        final_df.reset_index(drop=True, inplace=True)

        return final_df
