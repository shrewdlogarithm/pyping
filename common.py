import os,json

dateform = '%Y-%m-%d-%H:%M:%S'

hostlist = "[" + os.getenv('HOSTS','\"8.8.8.8\",\"90.207.238.97\",\"steampowered.com\"') + "]"
print(hostlist)
hosts = json.loads(hostlist)
dbname = "./data/pingdb.json"

def loadjson(jfile,dflt):
    try:
        with open(jfile) as json_file:
            retf = json.load(json_file)
    except:
        retf = dflt
    return retf

def writedb():
    with open(dbname, 'w') as json_file:
        json.dump(pingdb, json_file, indent=4,default=str)  

pingdb = loadjson(dbname,{})
