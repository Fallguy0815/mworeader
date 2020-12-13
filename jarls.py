from bs4 import BeautifulSoup
import requests
import numpy as np
import debug_reader

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

def queryStructure(pilotnames):
    structured = np.array(pilotnames)
    flat = structured.flatten()
    filtered = list(filter(None, flat))
    return queryList(filtered)
    

def queryList(pilotsflat):
    print(pilotsflat)    
    allpilots = sep.join(pilotsflat)
    ploads = {'u':allpilots}
    
    resp = requests.get('https://leaderboard.isengrim.org/search',params=ploads)
    pilotstats = {}
    
    

    if (resp.status_code == 200):
        if (debug_reader.debug_mode):
            with open(debug_reader.final_time + "/jarl_request.txt", "w") as q:
                q.write(resp.url)
            with open(debug_reader.final_time + "/jarl_response.txt", "w") as r:
                    r.write(resp.text)
        soup = BeautifulSoup(resp.text, "lxml")
        tds = soup.find_all("td", attrs={"class": "name"})
        for td in tds:
            at = td.find("a").text.strip().replace('\xa0', '\x20')
            if at in pilotsflat:
                dict = {}
                if (debug_reader.debug_mode):
                    print("statistics for " + at)
                parent = td.parent
                for key in statistics:
                    resolved = parent.find("td", attrs={"class": key}).text
                    dict[key] = resolved
                    # DEBUG
                    if(debug_reader.debug_mode):
                        print(statistics[key] + ": " + resolved)
                pilotstats[at] = dict.copy()
            else:
                pilotstats[at] = {'error': "unresolved"}                
    return pilotstats
    