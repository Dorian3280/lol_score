import requests
import pandas as pd
import matplotlib.pyplot as plt
from secret import API_KEY
from data import DATA
from loggingFunc import *
import matplotlib.pyplot as plt
import numpy as np
import sys

def get_server(server):
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

def get_info(server: str, ig):
    
    server, continent = get_server(server)
    res = requests.get(f"https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{ig}?api_key={API_KEY}")
    if res.status_code != 200:
        loggingError(res.status_code, get_info.__name__, ig)
        raise Exception

    return res.json()["puuid"], continent

def get_recent_games(puuid, continent):
    nb = 80
    res = requests.get(f"https://{continent}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count={nb}&api_key={API_KEY}")
    if res.status_code != 200:
        loggingError(res.status_code, get_recent_games.__name__)
        raise Exception

    return res.json()

def get_json_from_api(continent, g):

    """
    Operation GET from the Riot Api, return all information about a game
    country : where the game have been played
    g : the id of the game
    """

    res = requests.get(f"https://{continent}.api.riotgames.com/lol/match/v5/matches/{g}?api_key={API_KEY}")
    if res.status_code != 200:
        loggingError(res.status_code, get_json_from_api.__name__)
        raise Exception
    return res.json()

def extract_data_from_json(json, index, columns) -> list:
    
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

def get_df_from_json(games, champ, puuid, continent) -> pd.DataFrame:

    datas = []
    for g in games:
        json = get_json_from_api(continent, g)
        index = json['metadata']['participants'].index(puuid)
        
        # Remove outliers
        if json['info']["participants"][index]['championName'] != champ: continue
        if json['info']["participants"][index]['teamPosition'] not in DATA[champ]["role"]: continue
        if (json['info']["participants"][index]['gameEndedInEarlySurrender'] | json['info']["participants"][index]['gameEndedInSurrender']) and (json['info']['gameDuration'] < 1350): continue
        try:
            if json['challenges']['hadAfkTeammate'] > 0:
                continue
        except KeyError: pass
        
        res = extract_data_from_json(json, index, DATA[champ]["columns"])
        datas.append(res)
            
    return pd.DataFrame(data=datas, columns=["win", "gameDuration"] + DATA[champ]["columns"])

# def convertToIntOrFloat(x) -> int | float: pour la 3.10
def convert_to_int_or_float(x):
    try: return int(x)
    except ValueError: return float(x)

def gen(n):
    for i in n:
        yield i

def get_params(champ) -> dict[str: list]:

    generator = gen(open('./data/params.txt', 'r'))
    
    while True:
        str = next(generator)
        if champ in str:
            stats = str.strip().split(';')
            stats.pop(0)
            return {s.split(',')[0]: list(map(convert_to_int_or_float, s.split(',')[1:])) for s in stats}

def add_score(df, champ) -> pd.DataFrame:
    params = get_params(champ)
    df["score"] = df.apply(lambda x: sum([v[0]*((x[k]-v[1])/(v[2]-v[1])) for k, v in params.items()]), axis=1)
    return df

def get_your_score(ig, server, champ) -> pd.DataFrame:
    puuid, continent = get_info(server, ig)
    games = get_recent_games(puuid, continent)
    df = get_df_from_json(games, champ, puuid, continent)
    df = add_score(df, champ)
    loggingInfo(f'{ig} ({server}) as {champ}')
    return df

ig = sys.argv[1].replace('_', ' ')
server = sys.argv[2].upper()
champ = sys.argv[3].title()

get_your_score(ig, server, champ)
