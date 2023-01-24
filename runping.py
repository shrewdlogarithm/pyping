from flask import Flask,request
import time,datetime,multitasking,signal,pandas as pd
from ping3 import ping
import common

pingdb = common.pingdb
to = 4 # timeout for ping
dl = 6 # delay between attempts (added to timeout)
colors = ["Red","Blue","Green","Yellow"]

def handler(signum, frame):
    multitasking.killall
    common.writedb()  
signal.signal(signal.SIGINT, handler)

@multitasking.task 
def doping(dt,host,to):
    pg = ping(host, timeout=to)
    if (pg is not None):
        pt = max(int(pg*1000),.1)
    else:
        pt = to*1000
    if (host not in pingdb):
        pingdb[host] = {}
    pingdb[host][dt] = pt

@multitasking.task 
def runping():
    while 1==1:
        dt = datetime.datetime.now().strftime(common.dateform)
        for host in common.hosts:
            doping(dt,host,to)
        time.sleep(to+dl)
        common.writedb()

runping()

## Flask Server
app = Flask(__name__,
            static_url_path='', 
            static_folder='./public')

@app.route("/")
def hello():
    return app.send_static_file('index.html')

@app.route("/data", methods=['GET', 'POST'])
def data():
    dcol = 0
    hrstoshow = int(request.json["hrstoshow"])
    daysago = int(request.json["daysago"])
    df = pd.DataFrame(pingdb)
    labels=df.index.to_list()
    totime = datetime.datetime.strptime(labels[len(labels)-1],common.dateform) - datetime.datetime.strptime(labels[0],common.dateform)
    etime = datetime.datetime.now() - datetime.timedelta(hours = daysago*24)
    stime = etime - datetime.timedelta(hours = hrstoshow)    
    dff = df.loc[stime.strftime(common.dateform):etime.strftime(common.dateform)]
    data = {
        "totallength": totime.days*24 + int(totime.seconds/60/60),
        "labels": dff.index.to_list(),
        "datasets": []
    }
    for col in dff:
        ds = {
            "label": col,
            "data": dff[col].to_dict(),
            "borderColor": colors[dcol],
            "borderWidth": 1
        }
        dcol = dcol + 1
        data["datasets"].append(ds)
    return data

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)