from flask import Flask,request
from datetime import datetime,timedelta
import time,multitasking,signal,pandas as pd
from ping3 import ping
import common

to = 4 # timeout for ping
dl = 6 # delay between attempts (added to timeout)
colors = ["Red","Blue","Green","Orange","LightBlue","BLACK"]

def handler(signum, frame):
    multitasking.killall
    common.writedb()  
signal.signal(signal.SIGINT, handler) 

@multitasking.task 
def runping():
    while 1==1:
        dt = datetime.now().strftime(common.dateform)
        pings = {}
        for host in common.activehosts:
            pg = ping(host, timeout=to)
            # if pg == False:
            #     common.pingdb[host]["active"] = False
            # else:
            if (pg is not None):
                pt = max(int(pg*1000),.1)
            else:
                pt = to*1000
            pings[host] = pt
        common.addping(dt,pings)
        time.sleep(to+dl)

runping()

## Flask Server
app = Flask(__name__,
            static_url_path='', 
            static_folder='./svelte/public')

@app.route("/")
def hello():
    return app.send_static_file('index.html')

@app.route("/data", methods=['GET', 'POST'])
def data():
    dcol = 0
    hrstoshow = int(request.json["hrstoshow"])
    daysago = int(request.json["daysago"])
    etime = datetime.now() -timedelta(hours = daysago*24)
    stime = etime - timedelta(hours = hrstoshow)    
    df = common.getdataframe(stime,etime)
    df = df.set_index("dtime")
    df.fillna(0, inplace=True)
    # this needs to be ALL the data - not just the selected range...
    labels = df.index.sort_values().to_list()
    data = {
        "activehosts": common.activehosts,
        "totallength": common.totime.days*24 + int(common.totime.seconds/60/60),
        "labels": labels,
        "datasets": []
    }
    for col in df:
        ds = {
            "label": col,
            "data": df[col].sort_index().to_dict(),
            "borderColor": colors[dcol],
            "borderWidth": 1
        }
        dcol = (dcol + 1) % len(colors)

        data["datasets"].append(ds)
    return data

@app.route("/addhost", methods=['POST'])
def addhost():
    if request.method == 'POST':
        host = request.data.decode('UTF-8')
        common.activehosts.append(host)
    return("")

@app.route("/toglhost", methods=['POST'])
def toglhost():
    if request.method == 'POST':
        host = request.data.decode('UTF-8')
        if host in common.activehosts:
            common.activehosts.remove(host)
        else:
            common.activehosts.append(host)
    return("OK")
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)