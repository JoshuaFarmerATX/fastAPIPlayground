import pymysql
from collections import OrderedDict
from pymysql.cursors import DictCursorMixin, Cursor
from pprint import pprint
from fastapi import FastAPI
import uvicorn

mydb = pymysql.connect(
    'localhost',
    'josh',
    'root',
    'Covid'
    )

class OrderedDictCursor(DictCursorMixin, Cursor):
    dict_type = OrderedDict

cursor = mydb.cursor(OrderedDictCursor)

app = FastAPI()

@app.get("/")
def home():
    return "API Access OK"

# API Route 1: Most Recent Totals for Every Country Worldwide
@app.get("/API/most_recent")
async def most_recent():
    cursor.execute("SELECT iso3 AS ISO3, country_region AS Country, date AS 'Last Update', confirmed AS Cases, deaths AS Deaths, recovered AS Recovered FROM plotting WHERE date = (SELECT MAX(date) FROM plotting)")
    return(cursor.fetchall())

# API Route 2: Most Recent Confirmed Cases for Every Country Worldwide
@app.get("/API/most_recent/cases")
async def most_recent_cases():
    cursor.execute("SELECT iso3 AS ISO3, country_region AS Country, confirmed AS Cases, date AS 'Last Update' FROM plotting WHERE date = (SELECT MAX(date) FROM plotting)")
    return(cursor.fetchall())

# API Route 3: Most Recent Deaths for Every Country Worldwide
@app.get("/API/most_recent/deaths")
async def most_recent_deaths():
    cursor.execute("SELECT iso3 AS ISO3, country_region AS Country, deaths AS Deaths, date AS 'Last Update' FROM plotting WHERE date = (SELECT MAX(date) FROM plotting)")
    return(cursor.fetchall())

# API Route 4: Most Recent Number of Recoveries for Every Country Worldwide
@app.get("/API/most_recent/recovered")
async def most_recent_recovered():
    cursor.execute("SELECT iso3 AS ISO3, country_region AS Country, recovered AS Recovered, date AS 'Last Update' FROM plotting WHERE date = (SELECT MAX(date) FROM plotting)")
    return(cursor.fetchall())

# API Route 5: Most Recent Totals by Country
@app.get("/API/most_recent/{iso3_code}")
async def most_recent_by_country(iso3_code):
    cursor.execute(f"SELECT iso3 AS ISO3, country_region AS Country, date AS 'Last Update', confirmed AS Cases, deaths AS Deaths, recovered AS Recovered FROM plotting WHERE date = (SELECT MAX(date) FROM plotting) AND iso3 = '{iso3_code}'")
    return(cursor.fetchall())

# API Route 6: Most Recent Cases by Country
@app.get("/API/most_recent/cases/{iso3_code}")
async def most_recent_cases_by_country(iso3_code):
    cursor.execute(f"SELECT iso3 AS ISO3, country_region AS Country, confirmed AS Cases, date AS 'Last Update' FROM plotting WHERE date = (SELECT MAX(date) FROM plotting) AND iso3 = '{iso3_code}'")
    return(cursor.fetchall())

# API Route 7: Most Recent Dead by Country
@app.get("/API/most_recent/dead/{iso3_code}")
async def most_recent_dead_by_country(iso3_code):
    cursor.execute(f"SELECT iso3 AS ISO3, country_region AS Country, deaths AS Deaths, date AS 'Last Update' FROM plotting WHERE date = (SELECT MAX(date) FROM plotting) AND iso3 = '{iso3_code}'")
    return(cursor.fetchall())

# API Route 8: Most Recent Recovered by Country
@app.get("/API/most_recent/recovered/{iso3_code}")
async def most_recent_recovered_by_country(iso3_code):
    cursor.execute(f"SELECT iso3 AS ISO3, country_region AS Country, recovered AS Recovered, date AS 'Last Update' FROM plotting WHERE date = (SELECT MAX(date) FROM plotting) AND iso3 = '{iso3_code}'")
    return(cursor.fetchall())

# API Route 9: Global Timeseries
@app.get("/API/timeseries")
async def global_timeseries():
    cursor.execute(f"SELECT MAX(date) 'Total Results as of Date', SUM(confirmed) AS Cases, SUM(deaths) AS Deaths, SUM(recovered) AS Recovered FROM plotting GROUP BY date")
    return(cursor.fetchall())

# API Route 10: Global TImeseries for Cases
@app.get("/API/timeseries/cases")
async def global_timeseries_cases():
    cursor.execute(f"SELECT MAX(date) 'Total Results as of Date', SUM(confirmed) AS Cases FROM plotting GROUP BY date")
    return(cursor.fetchall())

# API Route 11: Global TImeseries for Deaths
@app.get("/API/timeseries/deaths")
async def global_timeseries_deaths():
    cursor.execute(f"SELECT MAX(date) 'Total Results as of Date', SUM(deaths) AS Deaths FROM plotting GROUP BY date")
    return(cursor.fetchall())

# API Route 12: Global TImeseries for Recovered
@app.get("/API/timeseries/recovered")
async def global_timeseries_recovered():
    cursor.execute(f"SELECT MAX(date) 'Total Results as of Date', SUM(recovered) AS Recovered FROM plotting GROUP BY date")
    return(cursor.fetchall())

# API Route 13: Timeseries by Country
@app.get("/API/timeseries/{iso3_code}")
async def timeseries_by_country(iso3_code):
    cursor.execute(f"SELECT iso3 AS ISO3, country_region AS Country, date as 'Total Results as of Date', confirmed AS Cases, deaths AS Deaths, recovered AS Recovered FROM plotting WHERE iso3 = '{iso3_code}'")
    return(cursor.fetchall())

# API Route 14: Timeseries of Cases by Country
@app.get("/API/timeseries/cases/{iso3_code}")
async def timeseries_of_cases_by_country(iso3_code):
    cursor.execute(f"SELECT iso3 AS ISO3, country_region AS Country, date as 'Total Results as of Date', confirmed AS Cases FROM plotting WHERE iso3 = '{iso3_code}'")
    return(cursor.fetchall())


# API Route 15: Timeseries of Deaths by Country
@app.get("/API/timeseries/deaths/{iso3_code}")
async def timeseries_of_deaths_by_country(iso3_code):
    cursor.execute(f"SELECT iso3 AS ISO3, country_region AS Country, date as 'Total Results as of Date', deaths AS Deaths FROM plotting WHERE iso3 = '{iso3_code}'")
    return(cursor.fetchall())

# API Route 16: Timeseries of Deaths by Country
@app.get("/API/timeseries/recovered/{iso3_code}")
async def timeseries_of_recovered_by_country(iso3_code):
    cursor.execute(f"SELECT iso3 AS ISO3, country_region AS Country, date as 'Total Results as of Date', recovered AS Recovered FROM plotting WHERE iso3 = '{iso3_code}'")
    return(cursor.fetchall())

# API Route 17: Totals for Every Country Worldwide as of Particular Date
@app.get("/API/bydate/{asof_date}")
async def global_timeseries(asof_date):
    cursor.execute(f"SELECT date AS 'Total Results as of Date', SUM(confirmed) AS Cases, SUM(deaths) AS Deaths, SUM(recovered) AS Recovered FROM plotting WHERE date = '{asof_date}' GROUP BY date")
    return(cursor.fetchall())

# API Route 18: Confirmed Cases for Every Country Worldwide as of Particular Date
@app.get("/API/bydate/cases/{asof_date}")
async def global_timeseries(asof_date):
    cursor.execute(f"SELECT date AS 'Total Results as of Date', SUM(confirmed) AS Cases FROM plotting WHERE date = '{asof_date}' GROUP BY date")
    return(cursor.fetchall())

# API Route 19: Deaths for Every Country Worldwide as of Particular Date
@app.get("/API/bydate/deaths/{asof_date}")
async def global_timeseries(asof_date):
    cursor.execute(f"SELECT date AS 'Total Results as of Date', SUM(deaths) AS Deaths FROM plotting WHERE date = '{asof_date}' GROUP BY date")
    return(cursor.fetchall())

# API Route 20: Recovered for Every Country Worldwide as of Particular Date
@app.get("/API/bydate/recovered/{asof_date}")
async def global_timeseries(asof_date):
    cursor.execute(f"SELECT date AS 'Total Results as of Date', SUM(recovered) AS Recovered FROM plotting WHERE date = '{asof_date}' GROUP BY date")
    return(cursor.fetchall())

# API Route 21: Specific Country Totals as of a particular date
@app.get("/API/bydate/countrytotals/{iso3_code}/{asof_date}")
async def country_totals_by_date(iso3_code, asof_date):
    cursor.execute(f"SELECT iso3 AS ISO3, country_region AS Country, date AS 'Last Update', confirmed AS Cases, deaths AS Deaths, recovered AS Recovered FROM plotting WHERE iso3 = '{iso3_code}' AND date = '{asof_date}'")
    return(cursor.fetchall())

# API Route 22: Specific Country Cases as of a particular date
@app.get("/API/bydate/countrycases/{iso3_code}/{asof_date}")
async def country_total_cases_by_date(iso3_code, asof_date):
    cursor.execute(f"SELECT iso3 AS ISO3, country_region AS Country, date AS 'Last Update', confirmed AS Cases FROM plotting WHERE iso3 = '{iso3_code}' AND date = '{asof_date}'")
    return(cursor.fetchall())

# API Route 23: Specific Country Deaths as of a particular date
@app.get("/API/bydate/countrydeaths/{iso3_code}/{asof_date}")
async def country_total_deaths_by_date(iso3_code, asof_date):
    cursor.execute(f"SELECT iso3 AS ISO3, country_region AS Country, date AS 'Last Update', deaths AS Deaths FROM plotting WHERE iso3 = '{iso3_code}' AND date = '{asof_date}'")
    return(cursor.fetchall())

# API Route 24: Specific Country Recoveries as of a particular date
@app.get("/API/bydate/countryrecoveries/{iso3_code}/{asof_date}")
async def country_total_recovered_by_date(iso3_code, asof_date):
    cursor.execute(f"SELECT iso3 AS ISO3, country_region AS Country, date AS 'Last Update', recovered AS Recovered FROM plotting WHERE iso3 = '{iso3_code}' AND date = '{asof_date}'")
    return(cursor.fetchall())

# API Route 25: Most Recent Worldwide Totals
@app.get("/API/global_totals/most_recent")
async def most_recent_global_total():
    cursor.execute(f"SELECT MAX(date) 'Total Results as of Date', SUM(confirmed) AS Cases, SUM(deaths) AS Deaths, SUM(recovered) AS Recovered FROM plotting WHERE date = (SELECT MAX(date) FROM plotting) GROUP BY date")
    return(cursor.fetchall())

# API Route 26: Most Recent Worldwide Total Cases
@app.get("/API/global_totals/cases/most_recent")
async def most_recent_global_total_cases():
    cursor.execute(f"SELECT MAX(date) 'Total Results as of Date', SUM(confirmed) AS Cases FROM plotting WHERE date = (SELECT MAX(date) FROM plotting) GROUP BY date")
    return(cursor.fetchall())

# API Route 27: Most Recent Worldwide Total Deaths
@app.get("/API/global_totals/deaths/most_recent")
async def most_recent_global_total_deaths():
    cursor.execute(f"SELECT MAX(date) 'Total Results as of Date', SUM(deaths) AS Deaths FROM plotting WHERE date = (SELECT MAX(date) FROM plotting) GROUP BY date")
    return(cursor.fetchall())

# API Route 28: Most Recent Worldwide Total Recovered
@app.get("/API/global_totals/recovered/most_recent")
async def most_recent_global_total_recovered():
    cursor.execute(f"SELECT MAX(date) 'Total Results as of Date', SUM(recovered) AS Recovered FROM plotting WHERE date = (SELECT MAX(date) FROM plotting) GROUP BY date")
    return(cursor.fetchall())

# API Route 29: Worldwide Totals as of a specific date
@app.get("/API/global_totals_bydate/{asof_date}")
async def most_recent_global_total(asof_date):
    cursor.execute(f"SELECT MAX(date) 'Total Results as of Date', SUM(confirmed) AS Cases, SUM(deaths) AS Deaths, SUM(recovered) AS Recovered FROM plotting WHERE date = '{asof_date}' GROUP BY date")
    return(cursor.fetchall())

# API Route 30: Worldwide Total Cases as of a specific date
@app.get("/API/global_total_cases_bydate/{asof_date}")
async def most_recent_global_total_cases(asof_date):
    cursor.execute(f"SELECT MAX(date) 'Total Results as of Date', SUM(confirmed) AS Cases FROM plotting WHERE date = '{asof_date}' GROUP BY date")
    return(cursor.fetchall())

# API Route 31: Worldwide Total Deaths as of a specific date
@app.get("/API/global_total_deaths_bydate/{asof_date}")
async def most_recent_global_total_deaths(asof_date):
    cursor.execute(f"SELECT MAX(date) 'Total Results as of Date', SUM(deaths) AS Deaths FROM plotting WHERE date = '{asof_date}' GROUP BY date")
    return(cursor.fetchall())

# API Route 32: Worldwide Total Recovered as of a specific date
@app.get("/API/global_total_recovered_bydate/{asof_date}")
async def most_recent_global_total_recovered(asof_date):
    cursor.execute(f"SELECT MAX(date) 'Total Results as of Date', SUM(recovered) AS Recovered FROM plotting WHERE date = '{asof_date}' GROUP BY date")
    return(cursor.fetchall())