import requests
import pandas as pd

api_key = "RGAPI-08720709-f17f-40ca-abe5-7b320b90eb06"
puid = '7UM4XmIs5HB3C6ZKAjFCoywvVltMf9gfaqecUmY9LJXMUN2aQo421-OdZwC_V5fhs3jgpKo8eA1nQA'

def dfFromAboveDiamond():
    queues = ['challenger', 'grandmaster', 'master']
    list = []
    for i in queues:
        response = requests.get(f"https://euw1.api.riotgames.com/lol/league/v4/{i}leagues/by-queue/RANKED_SOLO_5x5?api_key={api_key}")
        json = response.json()['entries']
        df = pd.DataFrame.from_dict(json)
        df.insert(4, 'tier', i)
        list.append(df)

    return pd.concat(list)

def dfFromDiamond1(nbr):
    list = []
    for i in range(1, nbr):
        response = requests.get(f"https://euw1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/I?page={i}&api_key={api_key}")
        json = response.json()
        df = pd.DataFrame.from_dict(json)
        list.append(df)
    
    return pd.concat(list)

def concatDfs(dfs):
    return pd.concat([*dfs]).reset_index(drop=True)

def update(df):
    df = df.dropna(axis=1)
    df = df.drop(['veteran', 'inactive', 'freshBlood', 'hotStreak'], axis=1)
    df['totalgames'] = df.apply(lambda x: x['wins'] + x['losses'], axis=1)
    df['winrate'] = df.apply(lambda x: round(x['wins'] / x['totalgames'] * 100, 1), axis=1)

games = requests.get(f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puid}/ids?start=0&count=100&api_key={api_key}").json()

list = []
for i in games:
    json = requests.get(f"https://europe.api.riotgames.com/lol/match/v5/matches/{i}?api_key={api_key}").json()
    list.append(pd.DataFrame.from_dict(json))

concatDfs(list)

