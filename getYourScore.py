import requests, sys
import pandas as pd
import matplotlib.pyplot as plt
from secret import API_KEY
from data import DATA
from loggingFunc import *


def pieWinrate(df):
    plt.figure()
    plt.title("Winrate")
    percent = df['winrate'].mean()*100
    labels = ['win', 'lose']
    plt.pie([percent, 100-percent], labels=labels, autopct='%1.0f%%')
    plt.legend()
    plt.show()

def formatScore(nbr):
    level = ""
    if nbr < 0.2:
        level = "C'est pas vraiment pas ouf.."
    elif nbr < 0.4:
        level = "Ça vaaaaaaa"
    elif nbr < 0.6:
        level = "Il s'en sort bien !"
    elif nbr < 0.8:
        level = "Trop fort"
    else:
        level = "Il est juste gifted en faite"
    return f"T'es a {nbr:.0%} de performance. {level}"

def getInfo(server: str, ig):
    servers = ['na1', 'br1', 'la1', 'la2', 'eun1', 'euw1', 'ru', 'oc1', 'kr', 'jp1']
    index = servers.index(server)

    if 0 <= index <= 3: continent = 'americas' 
    if 4 <= index <= 6: continent = 'europe' 
    else: continent = 'asia'
    res = requests.get(f"https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{ig}?api_key={API_KEY}")
    if res.status_code != 200:
        error(res.status_code, res.json()["status_code"]["message"], __name__, __file__)
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
        error(res.status_code, res.json()["status_code"]["message"], __name__, __file__)
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

# Type the champpion name in command line after execution of the .py file - python getYourScore.py [Pseudo] [server] [Champion]
ig = sys.argv[1]
server = sys.argv[2]
champ = sys.argv[3]

puuid, continent = getInfo(server, ig)
games = getRecentGames(puuid, continent)
df = getDFfromJson(games, champ, puuid, continent)
params = getParams(champ)
score = getScore(df, champ)
info(f'{ig} from {continent} get his score on {champ}')
print(score)
