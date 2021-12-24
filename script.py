import requests
import os
import json as JSON

def getServers(amount, options = {}, extras = {}):
    chunkList = chunks(amount)
    serverList = []
    skip = 0

    for i in chunkList:
        obj = getUrl(chunkList[i], skip, options.tags, options.query)
        skip += obj.skip
        url = obj.url

        res = req2await(url)
        list = JSON.parse(res).results
        serverList = serverList.concat(list)
    serverList = parseServers(serverList, extras)
    return serverList

def parseServers(json, extras):
    if extras.simplify == True:
        SL = simplify(json)
    else:
        SL = json

    if extras.sort == True:
        SL.sort(compare)

    if extras.filter == True and extras.filterSize > 0:
        L = [x for x in SL if x['members'] > extras.filterSize]
    else:
        L = SL

    if extras.write == True and extras.file is not None:
        write(extras.file, L)

    return L

def req2await(url):
    res = requests.get(url)
    if (res is not None):
        return res.text
    else:
        return None

def chunks(amount, split = 1000):
    chunks = []
    while (amount > split):
        chunks.push(split)
        amount -= split
    chunks.push(amount)
    return chunks

def write(file, array):
    f = open(file, "w")
    f.write(JSON.stringify(array))
    f.close()

def compare(a, b):
    if (a.members < b.members):
        return 1
    if (a.members > b.members):
        return -1
    return 0

def simplify(json):
    SL = []
    for s in json:
        SL.append({
            "_id": json[s].id,
            "name": json[s].name,
            "members": json[s].memberCount
        })
    return SL

def getUrl(a, s = 0, t = None, q = None):
    tags = ""
    query = ""
    if (t != None):
        tags = "tags=" + t + "&"
    if (q != None):
        query = "q=" + q + "&"
    return {
        "url": "https://top.gg/api/client/entities/search?${query}${tags}platform=discord&entityType=server&amount=${a}&skip=${s}".format(query, tags, a, s),
        "skip": a
    }