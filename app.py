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

@app.get("/API/most_recent")
async def most_recent():
    cursor.execute("SELECT * FROM plotting WHERE date = (SELECT MAX(date) FROM plotting)")
    plotting = cursor.fetchall()
    return(plotting)







