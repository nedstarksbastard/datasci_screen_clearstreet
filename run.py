import pandas as pd
import geopy
import folium
import pandas_datareader.data as web
from pandas.tseries.offsets import BDay
from geopy.extra.rate_limiter import RateLimiter

urls = {
    "start":"https://raw.githubusercontent.com/clear-street/datasci-screening-nedstarksbastard/fizi_screen/data/start.csv?token=ADXBUQYU2LDRT7DTNLZEWQS6A6K7U",
    "trade":"https://raw.githubusercontent.com/clear-street/datasci-screening-nedstarksbastard/fizi_screen/data/trades.csv?token=ADXBUQZKQ56AHBMLLSQ4RLK6A6LMC",
    "table":"https://raw.githubusercontent.com/clear-street/datasci-screening-nedstarksbastard/fizi_screen/data/table.html?token=ADXBUQ34M63OTOGHA7QOSCC6A6LKA"
}

# 1. Read files into Pandas directly from Github
df_sod = pd.read_csv(urls["start"], names=["Symbol", "Position"])
df_intra_day = pd.read_csv(urls["trade"], names=["Symbol", "Position"])

# 2. sum the start of day portfolio with the trades that have occurred during the day
df_intra_day_agg = df_intra_day.groupby("Symbol").sum().reset_index()
df_eod = df_sod.set_index('Symbol').add(df_intra_day_agg.set_index('Symbol'), fill_value=0).reset_index()
# df_eod[["POS"]].applymap('{:,.2f}'.format)  #in case formatting needed
df_eod["Position"] = df_eod["Position"].astype('int64')     # cast as int for readability
df_eod.to_csv('data/eod.csv', header=False, index=False)

# 3. get the the number of shares owned at the end of the day in each sector
df_info = pd.read_html(urls["table"])[0]
df_sectrs = pd.merge(df_info, df_eod, on="Symbol").groupby('GICS Sector')['Position'].sum().reset_index()
df_sectrs.to_csv('data/sector.csv', header=False, index=False)


# 4. other interesting things you can do with this data

# ################Un-comment this section out to generate coordinates############################

# locator = geopy.Nominatim(user_agent="myGeocoder")
# geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
#
# hqs = df_info["Headquarters Location"].unique()
# d = dict(zip(hqs, pd.Series(hqs).apply(geocode)))
# df_info["Location Info"] = df_info["Headquarters Location"].map(d)
#
# df_info['Point'] = df_info['Location Info'].apply(lambda loc: tuple(loc.point) if loc else None)
# df_info[['Latitude', 'Longitude', 'Altitude']] = pd.DataFrame(df_info['Point'].tolist(), index=df_info.index)
# df_info = df_info.drop(["Location Info", "Point"], axis=1)

####################################################################


# Reading from pre-generated csv file
df_loc = pd.read_csv('data/location.csv', names=['Symbol', 'Latitude', 'Longitude', 'Altitude'])
df_info = pd.merge(df_info, df_loc, on="Symbol")


# generate the geographical map
df_info = df_info.dropna(subset=['Latitude'])
hq_map = folium.Map(location=[44.950404, -93.101503], tiles='cartodbpositron',zoom_start=12)
df_info.apply(lambda row: folium.CircleMarker(location=[row["Latitude"], row["Longitude"]]).add_to(hq_map), axis=1)
hq_map.save('data/map.html')


# ################Uncomment this section get the close prices on last business day for each symbol#################

# last_biz_day = pd.datetime.today() - BDay()
# df_sym_close = web.DataReader(df_info['Symbol'].to_list(), 'yahoo', last_biz_day.strftime("%Y/%m/%d")).iloc[0]['Close'].reset_index()
# df_sym_close.columns = ["Symbol", "Close"]

####################################################################


# Reading from pre-generated csv file
df_sym_close = pd.read_csv('data/close_price.csv', names=['Symbol', 'Close'])


df_eod = pd.merge(df_eod, df_sym_close, on="Symbol")
df_eod["Total"] = df_eod["Position"] * df_eod["Close"]


