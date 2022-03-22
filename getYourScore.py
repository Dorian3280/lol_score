import requests, sys
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

def formatScore(nbr):
    return f"{nbr:.0%}"

def getInfo(server: str, ig):
    
    server, continent = getServer(server)
    res = requests.get(f"https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{ig}?api_key={API_KEY}")
    if res.status_code != 200:
        loggingError(res, getInfo.__name__)
        raise Exception

    return res.json()["puuid"], continent

def getRecentGames(puuid, continent):
    nb = 20
    return requests.get(f"https://{continent}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count={nb}&api_key={API_KEY}").json()

def getJsonFromlolApi(continent, g):

    """
    Operation GET from the Riot Api, return all information about a game
    country : where the game have been played
    g : the id of the game
    """

    res = requests.get(f"https://{continent}.api.riotgames.com/lol/match/v5/matches/{g}?api_key={API_KEY}")
    if res.status_code != 200:
        loggingError(res, getJsonFromlolApi.__name__)
        raise Exception
    return res.json()

def getDFfromJson(games, champ, puuid, continent):

    """
    Some operations to get all informations I get from API to Dataframes
    Loop over players I get in data.py
    Loop over their last games
    Choose their games where they played the champ
    Some formatting
    Get into one dataframe
    """

    array = []
    for g in games:
        try:
            json = getJsonFromlolApi(continent, g)
        except Exception:
            break
        index = json['metadata']['participants'].index(puuid)
        player = json['info']['participants'][index]
        if player['championName'] != champ: continue
        if player['teamPosition'] != DATA[champ]["role"]: continue
        try: player['hadAfkTeammate'] = player['challenges']['hadAfkTeammate']
        except KeyError: player['hadAfkTeammate'] = 0
        player['gameDuration'] = json['info']['gameDuration']
        player['CsPerMinute'] = round((player['totalMinionsKilled'] + player['neutralMinionsKilled']) / (player['gameDuration'] / 60), 1)
        player['dmgPerMinute'] = round(player['totalDamageDealtToChampions'] / (player['gameDuration'] / 60))
        
        array.append(pd.DataFrame({x: [player[x]] for x in DATA[champ]["columns"]}))
        
    return pd.concat(array).reset_index(drop=True)

def getParams(champ):
    def gen(n):
        for i in n:
            yield i

    generator = gen(open('./data/params.txt', 'r'))
    
    while True:
        str = next(generator)
        if champ in str:
            stats = str.strip().split(';')
            stats.pop(0)
            return {s.split(',')[0]: list(map(float, s.split(',')[1:])) for s in stats}

def calcScore(params, df):
    s = 0
    for k, v in params.items():
        n = df[k].mean()
        s += v[0]*((n-v[1])/(v[2]-v[1]))
    return float(s)

def getScore(df, champ):
    params = getParams(champ)
    s = calcScore(params, df)
    return s

# Type the champpion name in command line after execution of the .py file
# python getYourScore.py [Pseudo] [server] [Champion]
ig = sys.argv[1]
server = sys.argv[2]
champ = sys.argv[3]

puuid, continent = getInfo(server, ig)
games = getRecentGames(puuid, continent)
df = getDFfromJson(games, champ, puuid, continent)
params = getParams(champ)
score = getScore(df, champ)
loggingInfo(f'{ig} from {continent.title()} gets {formatScore(score)} on {champ}')
