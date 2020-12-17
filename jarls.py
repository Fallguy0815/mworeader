from bs4 import BeautifulSoup
import requests
import numpy as np
import constants
import random

sep = "\r\n"

statistics = {
    'name': 'Name',
    'rank': 'Rank',
    'prank': 'Percentile',
    'gplayed': 'Games played',
    'wlr': 'W/L',
    'sr': 'Survive Rate',
    'kd': 'K/D',
    'avgscore': 'Average Score'
}

def debugOutputString(text):
    if (constants.debugOutputConsole == 1):
        print(text)

def queryStructure(pilotnames):
    structured = np.array(pilotnames)
    flat = structured.flatten()
    filtered = list(filter(None, flat))
    if (constants.debugFakeInput == 1):
        pilotstats = {}
        for name in filtered:
            dict = {}
            dict['name'] = name
            dict['rank'] =  str(random.randint(1,50000))
            dict['prank'] = str(round(random.random()*100.0)) + "%"
            pilotstats[name] = dict.copy()
        return pilotstats
    else:
        return queryList(filtered)
    

def queryList(pilotsflat):
    debugOutputString(pilotsflat)
    allpilots = sep.join(pilotsflat)
    ploads = {'u':allpilots}
    
    resp = requests.get('https://leaderboard.isengrim.org/search',params=ploads)
    pilotstats = {}
    
    

    if (resp.status_code == 200):
        if (constants.debugOutputFiles == 1):
            with open(constants.finalTime + "/jarl_request.txt", "w") as q:
                q.write(resp.url)
            with open(constants.finalTime + "/jarl_response.txt", "w") as r:
                    r.write(resp.text)
        soup = BeautifulSoup(resp.text, "lxml")
        tds = soup.find_all("td", attrs={"class": "name"})
        for td in tds:
            at = td.find("a").text.strip().replace('\xa0', '\x20')
            if at in pilotsflat:
                dict = {}
                debugOutputString("statistics for " + at)
                parent = td.parent
                for key in statistics:
                    resolved = parent.find("td", attrs={"class": key}).text
                    dict[key] = resolved
                    debugOutputString(statistics[key] + ": " + resolved)
                pilotstats[at] = dict.copy()
            else:
                pilotstats[at] = {'error': "unresolved"}                
    return pilotstats
    