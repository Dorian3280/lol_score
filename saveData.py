import glob, os, time, requests, shutil, sys
import pandas as pd
from loggingFunc import *
from secret import API_KEY
from data import DATA


def get_recent_games(puuid, country, count):

    """
    Operation GET from the Riot Api, return all the recent games from a player
    puuid : his id
    country : from where he comes from
    count : start index of games
    """

    res = requests.get(f"https://{country}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start={count*20}&count=20&api_key={API_KEY}")
    
    if res.status_code != 200:
        loggingError(res.status_code, get_recent_games.__name__)
        raise Exception
    return res.json()

def get_json_from_api(country, g):

    """
    Operation GET from the Riot Api, return informations about a game
    country : where the game have been played
    g : the id of the game
    """

    res = requests.get(f"https://{country}.api.riotgames.com/lol/match/v5/matches/{g}?api_key={API_KEY}")
    if res.status_code != 200:
        loggingError(res.status_code, get_json_from_api.__name__)
        raise Exception
    return res.json()

def extract_data_from_json(json, index, columns):
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

def get_df_from_json(champ, count):

    """
    Some operations to get all informations I get from API to Dataframes
    Loop over players I get in data.py
    Loop over their last games
    Select games where they played the champ
    Some extracting from json
    Return a dataframe
    """

    datas = []
    error = False
    
    for p in DATA[champ]["players"]:
        try:
            games = get_recent_games(p["puuid"], p["country"], count)
        except Exception:
            error = True
            break
        
        for g in games:
            try:
                json = get_json_from_api(p['country'], g)
            except Exception:
                error = True
                break
            index = json['metadata']['participants'].index(p["puuid"])
            # Remove outliers
            if json['info']["participants"][index]['championName'] != champ: continue
            if json['info']["participants"][index]['teamPosition'] not in DATA[champ]["role"]: continue
            if (json['info']["participants"][index]['gameEndedInEarlySurrender'] | json['info']["participants"][index]['gameEndedInSurrender']) \
            and (json['info']['gameDuration'] < 1350): continue
            
            try: 
                if json['challenges']['hadAfkTeammate'] > 0:
                    continue
            except KeyError: pass
            
            datas.append(extract_data_from_json(json, index, DATA[champ]["columns"]))
            
    return pd.DataFrame(data=datas, columns=["win", "gameDuration"] + DATA[champ]["columns"]), not error

def save_data(champ):
    
    try: os.mkdir(champ)
    except FileExistsError: pass

    # Riot API has limit request, can't exceed a certain amount of request per minute, so I have to slow down the execution
    count = 0
    process = True
    while process and count < 5:
        df, process = get_df_from_json(champ, count)
        if df.empty:
            quit()
        df.to_csv(f"{champ}/{count}.txt", index=False, header=(count==0))
        count += 1
        # time.sleep(10)

    # Reassemble all datas file into a single one
    try:
        filenames = [file for file in glob.glob(fr"{champ}/*")]
        if not filenames:
            raise Exception
        with open(f'data/{champ}.txt', 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    outfile.write(infile.read())
            
            loggingInfo(f'{champ} datas added')

    except Exception:
        print('Nothing...')

    # Delete trash
    shutil.rmtree(champ)

champ = sys.argv[1].title()

save_data(champ)