import requests

import json
import struct
import numpy as np

import warnings

import concurrent.futures as futures


hsession = None
URL = None
PROBLEM_HEADERS = {"Content-Type":"application/octet-stream","x-api-key":""}

THREADPOOL = futures.ThreadPoolExecutor(max_workers=2)

USE_CLOUD = False

def connect(key=None,url="https://api.cobi.tech"):
    global USE_CLOUD
    USE_CLOUD = True
    global URL,hsession,PROBLEM_HEADERS
    URL = url
    hsession = requests.Session()
    if key!=None:
        PROBLEM_HEADERS["x-api-key"]=key
    else:
        warnings.warn("no api key provided, requesting free demo key")
        kres = hsession.get(URL+"/newkey")
        if kres.status_code==200:
            key = kres.text
            PROBLEM_HEADERS["x-api-key"]=key
        else:
            raise(RuntimeError("cannot retrieve free demo key"))


def convert_adjacency(adj,config={}):
    try:
        adj = np.asarray(adj)
    except:
        raise(TypeError("adjacency matrix for QUBO must be array-like"))
    shape = adj.shape

    if len(shape)!=2:
        raise(ValueError("adjacency matrix must be 2d array"))
    if shape[0]!=shape[1]:
        raise(ValueError("adjacency matrix must be square"))
    size = shape[0]

    #send_data= struct.pack('i',size)
    config["size"]=size
    send_data = bytes(json.dumps(config),'utf-8')
    
    for x in range(size):
        w = adj[x,x]
        if w!=0:
            send_data=send_data+struct.pack('hhf',x,x,w)

    for x in range(size):
        for y in range(x+1,size):
            w = adj[x,y]+adj[y,x]
            if w!=0:
                send_data = send_data+struct.pack('hhf',x,y,w)
    return send_data

def make_request(data):
    res = hsession.post(URL+"/problem",headers=PROBLEM_HEADERS,data=data)
    if res.status_code==200:
        return res.text
    elif res.status_code==429:
        raise(RuntimeError("too many requests on this api key"))
    else:
        raise(RuntimeError(f"Server Error: {res.status_code}: {res.text}"))


def parse_response(ans):
    ans = json.loads(ans)["content"]
    spin_string,en_string = ans.split(",")
    energy = float(en_string.split(":")[1])
    spins = [1 if c == "1" else 0 for c in spin_string]
    return spins,energy

def send_problem(adj,config={}):
    data = convert_adjacency(adj,config)
    
    res = make_request(data)
    return parse_response(res)


def solve_async(adj,config={}):
    return THREADPOOL.submit(send_problem,adj,config)
