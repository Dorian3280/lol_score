import glob, os, time, requests, shutil, sys
import pandas as pd
from secret import API_KEY
from data import DATA

def getJsonFromlolApi(country, g):

    """
    Operation GET from the Riot Api, return all information about a game
    country : where the game have been played
    g : the id of the game
    """

    res = requests.get(f"https://{country}.api.riotgames.com/lol/match/v5/matches/{g}?api_key={API_KEY}")
    if res.status_code != 200: raise Exception
    return res.json()

def getRecentGames(puuid, country, count):

    """
    Operation GET from the Riot Api, return all the recent games from a player
    puuid : his id
    country : from where he comes from
    count : start index of games
    """

    res = requests.get(f"https://{country}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start={count*20}&count=20&api_key={API_KEY}")
    
    if res.status_code != 200: raise Exception
    return res.json()

def getDFfromJson(champ, count):

    """
    Some operations to get all informations I get from API to Dataframes
    Loop over players I get in data.py
    Loop over their last games
    Choose their games where they played the champ
    Some formatting
    Get into one dataframe
    """

    array = []
    error = False
    for p in DATA[champ]["players"]:
        try:
            games = getRecentGames(p["puuid"], p["country"], count)
        except Exception:
            print('games')
            error = True
            break
        
        for g in games:
            try:
                json = getJsonFromlolApi(p['country'], g)
            except Exception:
                print('game')
                error = True
                break
            index = json['metadata']['participants'].index(p["puuid"])
            player = json['info']['participants'][index]
            if player['championName'] != champ: continue
            if player['teamPosition'] != DATA[champ]["role"]: continue
            try: player['hadAfkTeammate'] = player['challenges']['hadAfkTeammate']
            except KeyError: player['hadAfkTeammate'] = 0
            player['gameDuration'] = json['info']['gameDuration']
            player['CsPerMinute'] = round((player['totalMinionsKilled'] + player['neutralMinionsKilled']) / (player['gameDuration'] / 60), 1)
            player['dmgPerMinute'] = round(player['totalDamageDealtToChampions'] / (player['gameDuration'] / 60))
            array.append(pd.DataFrame({x: [player[x]] for x in DATA[champ]["columns"]}))

    return pd.concat(array).reset_index(drop=True), not error

# Type the champion name in command line after execution of the .py file - python saveDate.py [Champion name]
champ = sys.argv[1].title()
count = 0
process = True

# Create a directory to store datas
try: os.mkdir(champ)
except FileExistsError: pass

# Riot API has limit request, can't exceed a certain amount of request per minute, so I has to slow down the execution
while process and count != 5:
    df, process = getDFfromJson(champ, count)
    df.to_csv(f"{champ}/{count}.txt", index=False, header=(count==0))
    count += 1
    time.sleep(120)

# Reassemble all datas file into a single one
try:
    filenames = [file for file in glob.glob(fr"{champ}/*")]
    if not filenames:
        raise Exception
    with open(f'data/{champ}.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                outfile.write(infile.read())

except Exception:
    print('Nothing...')

# Delete trash
shutil.rmtree(champ)
