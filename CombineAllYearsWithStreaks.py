from pandas import ExcelWriter
from openpyxl import load_workbook
import pandas as pd
import numpy as np
import pickle

fullTeamList = ['Calgary Flames', 'Phoenix Coyotes', 'Edmonton Oilers', 'Arizona Coyotes', 'Colorado Avalanche',
                'Vegas Golden Knights', 'Anaheim Ducks', 'Vancouver Canucks', 'San Jose Sharks', 'Los Angeles Kings',
                'Carolina Hurricanes', 'Pittsburgh Penguins', 'Tampa Bay Lightning', 'Detroit Red Wings', 'Columbus Blue Jackets',
                'Washington Capitals', 'Buffalo Sabres', 'Florida Panthers', 'Toronto Maple Leafs', 'Montréal Canadiens',
                'New Jersey Devils', 'Boston Bruins', 'Philadelphia Flyers', 'New York Rangers', 'New York Islanders',
                'Ottawa Senators', 'Atlanta Thrashers', 'St. Louis Blues', 'Chicago Blackhawks', 'Minnesota Wild',
                'Winnipeg Jets', 'Nashville Predators', 'Dallas Stars']


def openfile(filename):
    infile = open(filename, 'rb')
    df1 = pickle.load(infile)
    infile.close()
    return df1


df1 = openfile('2007-20dataset')
print(df1[0][0])
for year in range(len(df1)):
    teamStreak = {}
    n = 0
    for team in fullTeamList:
        teamStreak[team] = 0
    for date in range(len(df1[year])):
        homeTeamStreak = []
        awayTeamStreak = []
        # print(date)
        # print(year)
        for index, row in df1[year][date].iterrows():
            n = n + 1
            print(n)
            # Assign pre-game win/lose streaks for each game
            homeTeamStreak.append(teamStreak[row['hometeam']])
            awayTeamStreak.append(teamStreak[row['awayteam']])
            # Home team win condition
            if (row['homegoals'] > row['awaygoals']):
                # checks current streak for home team
                if (teamStreak[row['hometeam']] >= 0):
                    teamStreak[row['hometeam']] += 1
                else:
                    teamStreak[row['hometeam']] = 1
                # checks current streak for away team
                if (teamStreak[row['awayteam']] <= 0):
                    teamStreak[row['awayteam']] -= 1
                else:
                    teamStreak[row['awayteam']] = -1

            # Home team lose condition
            if (row['homegoals'] < row['awaygoals']):
                # checks current streak for home team
                if (teamStreak[row['hometeam']] <= 0):
                    teamStreak[row['hometeam']] -= 1
                else:
                    teamStreak[row['hometeam']] = -1

                # checks current streak for away team
                if (teamStreak[row['awayteam']] >= 0):
                    teamStreak[row['awayteam']] += 1
                else:
                    teamStreak[row['awayteam']] = 1
        df1[year][date]['homeTeamStreak'] = homeTeamStreak
        df1[year][date]['awayTeamStreak'] = awayTeamStreak

outfile = open("2007-20datasetV2", 'wb')
pickle.dump(df1, outfile)
outfile.close()
