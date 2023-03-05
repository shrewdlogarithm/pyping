import json,sqlite3;
import pandas as pd;
from datetime import datetime

dateform = '%Y-%m-%d %H:%M:%S'

dbname = "./data/pingdb.sqlite"

connection = sqlite3.connect(dbname, check_same_thread=False)
connection.row_factory = sqlite3.Row
connection.executescript("CREATE TABLE IF NOT EXISTS PINGS (dtime TEXT, pings TEXT);")

updated = True
def addping(dtime,pings):
    global updated
    connection.execute("INSERT INTO PINGS(dtime,pings) values(?,?)",(dtime,json.dumps(pings)))
    connection.commit()
    updated = True

df = None
totime = 0
def getdataframe(stime=None,etime=None):
    global activehosts,updated,df,totime
    def todict(obj):    
        robj = {"dtime": obj["dtime"]} | json.loads(obj["pings"])    
        return robj
    if updated:
        pings = connection.execute('SELECT * FROM pings WHERE (?1 is NULL or dtime >= ?1) and (?2 IS NULL or dtime <= ?2)',(stime,etime)).fetchall()
        if totime == 0:
            totime = datetime.strptime(pings[len(pings)-1]["dtime"],dateform) - datetime.strptime(pings[0]["dtime"],dateform)
        mpings = map(todict,pings)
        df = pd.DataFrame(mpings)
        updated = False
    return df

activehosts = []
getdataframe()
if df.empty:
    activehosts = ["8.8.8.8","yahoo.com"]
else:
    activehosts = df.columns.to_list()[1:]