import fileinput, sys
import pandas as pd
from loggingFunc import *
from data import DATA


def calc(json, index, c):
    
    if c == 'kills':
        return json['info']['gameDuration']
    if c == 'deaths':
        return json['info']["participants"][index]['deaths']
    if c == 'kills':
        return json['info']["participants"][index]['kills']
    if c == 'csPerMinute':
        return round((json['info']["participants"][index]['totalMinionsKilled'] + json['info']["participants"][index]['neutralMinionsKilled']) / (json['info']['gameDuration'] / 60), 1)
    if c == 'dmgPerMinute':
        return round(json['info']["participants"][index]['totalDamageDealtToChampions'] / (json['info']['gameDuration'] / 60))
    if c == 'win':
        return int(json['info']["participants"][index]['win'])

def returnParams(df: pd.DataFrame, champ):
    params = {}
    columns = DATA[champ]["columns"]
    weight = round(1/len(columns), 1)
    statDf = df.describe()
    csPerMinute = statDf.loc['mean']['csPerMinute']
    dmgPerMinute = statDf.loc['mean']['dmgPerMinute']
    
    for c in columns:
        if c == "kills": params[c] = weight, 0, statDf.loc['75%']['kills']
        if c == "deaths": params[c] = weight, 10, 0
        if c == "csPerMinute": params[c] = weight, round(csPerMinute * 0.6, 1), round(csPerMinute * 1.5, 1)
        if c == "dmgPerMinute": params[c] = weight, round(dmgPerMinute * 0.6), round(dmgPerMinute * 1.5)
    
    # tuple(weight, minPerformance, maxPerformance)
    return params

def updateParams(champ, params: dict):
    fi = fileinput.input(f'data/params.txt', inplace=True)
    for line in fi:
        if line.find(champ) != -1:
            line = f'''{champ};{';'.join(f"{k},{','.join(map(str, v))}" for k, v in params.items())}\n'''
        sys.stdout.write(line)
    loggingInfo(f"{champ} parameters updated")
    fi.close()

# Type the champpion name in command line after execution of the .py file
# python calcParams.py [Champion name]
champ = sys.argv[1].title()

df = pd.read_csv(f"data/{champ}.txt")
if df.empty:
    loggingError(404, 'calcParams')
    quit()
params = returnParams(df, champ)
updateParams(champ, params)
