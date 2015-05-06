#!/usr/bin/python
from __future__ import print_function 

import MySQLdb
import numpy as np
from collections import defaultdict

from builtins import input

import battingorder

import csv

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="", # your password
                      db="retrosheet") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

def date_query(date, start=True):
    comp_op = "<="
    if start:
        comp_op = ">="
    if len(date) == 4:
        return "SUBSTR(events.game_id,4,4) "+comp_op + " '" + date + "'"
    elif len(date) == 8:
        return "SUBSTR(events.game_id,4,8) "+comp_op + " '" + date + "'"
    else:
        raise Exception("invalid date format!")
    

year = input("Enter what year you want data from\n")
team = input("Enter team id\n")


# Gets the relevant games
inner_query = "CREATE TEMPORARY TABLE IF NOT EXISTS table2 AS" + \
              "(SELECT e.BAT_ID, e.BATTEDBALL_cd, e.ab_fl, e.sf_fl, e.event_cd, e.game_id, e.BAT_DEST_ID, e.BAT_TEAM_ID " + \
              "FROM events e " + \
              "INNER JOIN game_types ON game_types.game_id = e.game_id "+ \
              "where game_types.game_type='R' AND " + \
              "e.game_id LIKE '___"+year+"%' );"

# Restricts to regular season games
print("creating table2 ... ", inner_query)
cur.execute(inner_query)

def get_roster():
    cur.execute("SELECT DISTINCT(BAT_ID) from table2;")
    roster = cur.fetchall()
    roster = np.asarray(roster)[:,0].tolist()
    return roster

"""
Creates a temporary table of all the relevant stats for later use
"""
def create_stats_table():
    query = "CREATE TEMPORARY TABLE IF NOT EXISTS stats_table AS" + \
            "(SELECT bat_id, event_cd, COUNT(*) from table2 " + \
            "WHERE event_cd IN (14,15,20,21,22,23) GROUP BY event_cd, bat_id);"
    print("creating stats table ...", query)
    cur.execute(query)

def get_all_stats():
    query = "SELECT bat_id, event_cd, COUNT(*) from table2 " + \
            "WHERE event_cd IN (14,15,20,21,22,23) GROUP BY event_cd, bat_id;"
    print("collecting all player stats ...", query)
    cur.execute(query)
    results = cur.fetchall()

    cur.execute("SELECT bat_id, count(*) from table2 WHERE AB_FL = 'T' GROUP BY bat_id;")
    ab = cur.fetchall()

    stats = {}

    for row in results:
        if not row[0] in stats:
            stats[row[0]] = defaultdict(int) # Returns 0 by default
        stats[row[0]][row[1]] = int(row[2])

    for row in ab:
        if not row[0] in stats:
            stats[row[0]] = defaultdict(int)
        stats[row[0]]['ab'] = int(row[1])

    return stats



def get_player_stats(player_id, stats_dict):
    results = stats_dict[player_id]    
    hr, tr, db, single = results[23], results[22], results[21], results[20]
    ab = results['ab']
    outs = ab - hr - tr - db - single
    stats = [hr, tr, db, single, results[14]+results[15], outs, player_id]
    return stats

"""
returns starting lineup and ending score for the given game
Also returns the number of innings played
Returns tuple of general game info, home_lineup, away_lineup
"""
def game_info(game_id):
    query = "SELECT home_team_id, away_team_id, away_score_ct, " + \
    "home_score_ct, INN_CT, "+\
        "HOME_LINEUP1_BAT_ID, HOME_LINEUP2_BAT_ID, HOME_LINEUP3_BAT_ID, HOME_LINEUP4_BAT_ID, HOME_LINEUP5_BAT_ID, HOME_LINEUP6_BAT_ID, HOME_LINEUP7_BAT_ID, HOME_LINEUP8_BAT_ID, HOME_LINEUP9_BAT_ID, " + \
        "AWAY_LINEUP1_BAT_ID, AWAY_LINEUP2_BAT_ID, AWAY_LINEUP3_BAT_ID, AWAY_LINEUP4_BAT_ID, AWAY_LINEUP5_BAT_ID, AWAY_LINEUP6_BAT_ID, AWAY_LINEUP7_BAT_ID, AWAY_LINEUP8_BAT_ID, AWAY_LINEUP9_BAT_ID " + \
        "FROM games " + \
        "WHERE game_id='"+game_id+"';"
    cur.execute(query)
    results = cur.fetchall()[0]

    away_score = results[2]
    home_score = results[3]

    info = dict(zip(np.array(cur.description)[:5,0].tolist(), results[:5]))
    home_lineup = results[5:5+9]
    away_lineup = results[5+9:5+18]

    return info, home_lineup, away_lineup


def get_all_games(year):
    query = "SELECT e.game_id FROM games e " + \
            "INNER JOIN game_types ON game_types.game_id = e.game_id "+ \
              "where game_types.game_type='R' AND year_id='"+year+ "';"
    cur.execute(query)
    results = cur.fetchall()
    return np.array(results)[:,0].tolist()


"""
Get prediction errors and save it to a csv file
"""
def get_prediction_errors(year):
    all_stats = get_all_stats()
    errors = [["home", "away", "home_score", "away_score", "pred_home_score", "pred_away_score"]]
    for game_id in get_all_games(year):
        info, home_lineup, away_lineup = game_info(game_id)
        if info['INN_CT'] != 9:
            continue #Throw out games that go to extra innings

        stats = []
        try:
            for pid in home_lineup:
                stats.append(get_player_stats(pid, all_stats))
        except KeyError:
            continue #Throw out lineups with unseen players
        pred_home_score = battingorder.get_run_expectancy(stats)

        stats = []
        try:
            for pid in away_lineup:
                stats.append(get_player_stats(pid, all_stats))
        except KeyError:
            continue
        pred_away_score = battingorder.get_run_expectancy(stats)

        home_score, away_score = info['home_score_ct'], info['away_score_ct']
        home_team, away_team = info['home_team_id'], info['away_team_id']

        data = [home_team, away_team, home_score, away_score, pred_home_score, pred_away_score]
        errors.append(data)

    with open("simulation_error"+year+".csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(errors)

    return

    #th

stats = [[38,5,33,113,98,383,'ChipperJones_LF'],
[34,2,25,96,56,468,'AndruwJones_CF'],
[36,2,28,94,94,313,'GarySheffield_RF'],
[25,1,34,80,35,398,'VinnyCastilla_3B'],
[4,0,19,66,24,235,'RafaelFurcal_SS'],
[9,2,10,43,28,139,'MarcusGiles_2B'],
[3,0,4,20,10,63,'JulioFranco_1B'],
[17,1,16,83,28,252,'JavyLopez_C'],
[0,0,3,33,13,293,'StartingPitchers_P']]
print("lineup: ", battingorder.get_run_expectancy(stats))

get_prediction_errors(year)
