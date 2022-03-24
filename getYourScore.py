import requests, sys, re
import pandas as pd
import matplotlib.pyplot as plt
from secret import API_KEY
from data import DATA
from loggingFunc import *

def getServer(server):
    servers = {
        'EUW': ('euw1', 'europe'),
        'EUNE': ('eun1', 'europe'),
        'RU': ('ru', 'europe'),
        'NA': ('na1', 'americas'), 
        'BR': ('br1', 'americas'),
        'LAN': ('la1', 'americas'),
        'OCE': ('oc1', 'asia'),
        'KR': ('kr', 'asia'),
        'JP': ('jp1', 'asia')
    }
    
    return servers[server]

def pieWinrate(df):
    plt.figure()
    plt.title("Winrate")
    percent = df['winrate'].mean()*100
    labels = ['win', 'lose']
    plt.pie([percent, 100-percent], labels=labels, autopct='%1.0f%%')
    plt.legend()
    plt.show()

def getInfo(server: str, ig):
    
    server, continent = getServer(server)
    res = requests.get(f"https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{ig}?api_key={API_KEY}")
    if res.status_code != 200:
        loggingError(res.status_code, getInfo.__name__, ig)
        raise Exception

    return res.json()["puuid"], continent

def getRecentGames(puuid, continent):
    nb = 20
    res = requests.get(f"https://{continent}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count={nb}&api_key={API_KEY}")
    if res.status_code != 200:
        loggingError(res.status_code, getRecentGames.__name__)
        raise Exception

    return res.json()

def getJsonFromApi(continent, g):

    """
    Operation GET from the Riot Api, return all information about a game
    country : where the game have been played
    g : the id of the game
    """

    res = requests.get(f"https://{continent}.api.riotgames.com/lol/match/v5/matches/{g}?api_key={API_KEY}")
    if res.status_code != 200:
        loggingError(res.status_code, getJsonFromApi.__name__)
        raise Exception
    return res.json()

def extractDataFromJson(json, index, columns):
    
    res = []
    res.append(int(json['info']["participants"][index]['win']))
    res.append(json['info']['gameDuration'])
    
    for c in columns:
        if c == 'kills':
            res.append(json['info']["participants"][index]['kills'])
        if c == 'deaths':
            res.append(json['info']["participants"][index]['deaths'])
        if c == 'csPerMinute':
            res.append(round((json['info']["participants"][index]['totalMinionsKilled'] + json['info']["participants"][index]['neutralMinionsKilled']) / (json['info']['gameDuration'] / 60), 1))
        if c == 'dmgPerMinute':
            res.append(round(json['info']["participants"][index]['totalDamageDealtToChampions'] / (json['info']['gameDuration'] / 60)))
    
    return res

def getDFfromJson(games, champ, puuid, continent):

    """
    Some operations to get all informations I get from API to Dataframes
    Loop over players I get in data.py
    Loop over their last games
    Choose their games where they played the champ
    Some formatting
    Get into one dataframe
    """

    datas = []
    for g in games:
        json = getJsonFromApi(continent, g)
        index = json['metadata']['participants'].index(puuid)
        
        # Remove outliers
        if json['info']["participants"][index]['championName'] != champ: continue
        if json['info']["participants"][index]['teamPosition'] != DATA[champ]["role"]: continue
        if (json['info']["participants"][index]['gameEndedInEarlySurrender'] | json['info']["participants"][index]['gameEndedInSurrender']) and (json['info']['gameDuration'] < 1350): continue
        
        try: 
            if json['challenges']['hadAfkTeammate'] > 0:
                continue
        except KeyError: pass
        
        datas.append(extractDataFromJson(json, index, DATA[champ]["columns"]))
            
    return pd.DataFrame(data=datas, columns=["win", "gameDuration"] + DATA[champ]["columns"])

def convertToIntOrFloat(x):
    try: return int(x)
    except ValueError: return float(x)

def gen(n):
    for i in n:
        yield i
        
def getParams(champ):

    generator = gen(open('./data/params.txt', 'r'))
    
    while True:
        str = next(generator)
        if champ in str:
            stats = str.strip().split(';')
            stats.pop(0)
            return {s.split(',')[0]: list(map(convertToIntOrFloat, s.split(',')[1:])) for s in stats}

def calcScore(params, df):
    s = 0
    for k, v in params.items():
        n = df[k].mean()
        s += v[0]*((n-v[1])/(v[2]-v[1]))
    return s*100

def getScore(df, champ):
    params = getParams(champ)
    return calcScore(params, df)

# Type the champpion name in command line after execution of the .py file
# python getYourScore.py [Pseudo] [server] [Champion]
ig = sys.argv[1]
server = sys.argv[2].upper()
champ = sys.argv[3].title()

try:
    puuid, continent = getInfo(server, ig)
    games = getRecentGames(puuid, continent)
    df = getDFfromJson(games, champ, puuid, continent)
    score = getScore(df, champ)
except Exception:
    quit()
    
def getEvolution(ig, champ):
    generator = gen(open('debug.log', 'r'))
    evolution = []
    try:
        while line := next(generator):
            if ig in line and champ in line: evolution.append(int(re.search(r'\d{1,2}(?=%)', line).group()))
    except:
        return evolution
    
try:
    lastScore = getEvolution(ig, champ)[-1]
except IndexError:
    lastScore = None
    

def formatScore(nbr, last):
    
    if last is None: return f"{nbr:.0%}"
    
    evolution = (nbr-last)/last
    return f"{nbr/100:.0%} ({evolution:+.0%})"

loggingInfo(f'{ig} ({server}) as {champ} -> {formatScore(score, lastScore)}')
