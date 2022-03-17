import fileinput, sys
import pandas as pd
from loggingFunc import *

def dropOutliers(df):
    df.drop(df[df['hadAfkTeammate'] > 0].index, inplace=True)
    df.drop(df[(df['gameEndedInSurrender'] | df['gameEndedInSurrender']) & (df['gameDuration'] < 1350)].index, inplace=True)

def returnParams(df: pd.DataFrame):
    params = {}
    weight = 4
    relevantdf = df.describe()
    meanScoreCreeps = relevantdf.loc['mean']['CsPerMinute']
    meanDmg = relevantdf.loc['mean']['dmgPerMinute']
    params['kills'] = 1/weight, 0, relevantdf.loc['75%']['kills']
    params['deaths'] = 1/weight, 10, 0
    params['CsPerMinute'] = 1/weight, round(meanScoreCreeps * 0.6, 1), round(meanScoreCreeps * 1.5, 1)
    params['dmgPerMinute'] = 1/weight, round(meanDmg * 0.6), round(meanDmg * 1.5)
    
    # tuple(weigth, minPerformorance, maxPerformance)
    return params

def updateParams(champ, params: dict):
    fi = fileinput.input(f'data/params.txt', inplace=True)
    for line in fi:
        if line.find(champ) != -1:
            line = f'''{champ};{';'.join(f"{k},{','.join(map(str, v))}" for k, v in params.items())}\n'''
        sys.stdout.write(line)
    info(f'Parameters of {champ} updated')
    fi.close()

# Type the champpion name in command line after execution of the .py file - python calcParams.py [Champion name]
champ = sys.argv[1].title()

df = pd.read_csv(f"data/{champ}.txt")
dropOutliers(df)
params = returnParams(df)
updateParams(champ, params)
