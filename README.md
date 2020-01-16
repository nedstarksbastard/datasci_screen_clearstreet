
## Problem

1. Read `start.csv`, `trades.csv`, and `table.html` into Pandas directly from Github.

2. Create an end of day file, `eod.csv`, that sums the start of day portfolio with the trades that have occurred during the day. This represents the start of day portfolio for the next day.

3. We have provided a scraped `.html` file that gives you the ticker, sector, and headquarters location of several companies. Produce a `sector.csv` file that shows the number of shares owned at the end of the day in each sector.

4. That wasn't so bad, right? What are some other interesting things you can do with this data? Maybe plot the headquarters locations using a geolocation API, or tell us how much money those trades would have made with today's market data? Entirely up to you.

Don't hesitate to ask if you have any questions, and good luck :)


## Solution Notes

The project contains three source files:
1. **run.py** -- contains the sequential code. This will generate the eod.csv, sector.csv and map.html (4). Due to the long 
time taken in fetching geographical information and also the financial data for last business day, I have commented
out the code blocks that do those tasks and instead read from pre-generated csv files (location.csv, close_price.csv). 
I have done some performance improvements such as only fetching the unique addresses but more can be done. If you would 
like to run the actual code just uncomment the code blocks as described in the file

2. **run.ipynb** -- jupyter notebook with much the same code. This way you can run individual code blocks and also use
pre-generated data files to fetch geographical and financial data

3. **requirements.txt** -- requirement file for building the virtual env. All libraries besides pandas are for part 4

The project contains 5 new data files under the data folder:

1. **close_price.csv** - contains close-price for last-business day (12/20/2019) for the Symbols. Generated using `pandas_datareader`

2. **eod.csv** - contains end-of-day positions for Symbols as required for the task 2

3. **location.csv** - contains geographical coordinates for the Symbol headquarters. Generated using `geopy`

4. **map.html** - open this in browser to see the map of all headquarters. Generated using `folium`

5. **sector.csv** - contains number of shares owned at the end of the day in each sector as required for task 3

To build and run the script on windows and using virtual environment

```
pip install virtualenv
cd datasci-screening-nedstarksbastard
virtualenv venv
\venv\Scripts\activate.bat
pip install -r requirements.txt
\venv\Scripts\python.exe run.py
```
To run jupyter notebook
```
\venv\Scripts\jupyter-notebook.exe
```
