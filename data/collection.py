#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the PyMVPA package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
import requests
import json
from pymongo import MongoClient
import argparse
import sys

client = MongoClient('mongodb://localhost:27017')

parser = argparse.ArgumentParser(description='This is the script which handles data collection for the app. Takes --game inputs')

parser.add_argument('--game',dest='game',required=True)

del sys.argv[0]

args_dict = vars(parser.parse_args(sys.argv))
game = args_dict['game']

def collect_data(game):
    if(game=='league'):
        print 'game is League of Legends'
        db = client.league_of_legends

        league_url = 'https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&champListData=all&tags=all&dataById=false'
        headers = {"X-Riot-Token": "RGAPI-290454e6-05e1-4d05-a5b5-99e5b02dbc29"}
        try:
            response = requests.get(league_url,headers=headers)
        except requests.ConnectionError:
            print 'uh oh something went wrong with the api'
        else:
            data = response.json()
            champion_data = data['data']

            for champion, data in champion_data.iteritems():

                post_id = db.champion_data.insert_one(data).inserted_id
                if(post_id):
                    print 'Added champion {0}'.format(champion)


    elif (game=='DOTA2'):
        db = client.dota2
        print 'game is DOTA'
    elif(game=='Overwatch'):
        db = client.overwatch

        print 'game is Overwatch'

        for heroID in range(1,25): #this is the amount of heros that api supports
            overwatch_url = 'https://overwatch-api.net/api/v1/hero/{0}'.format(heroID)
            try:
                response = requests.get(overwatch_url)
            except requests.ConnectionError:
                print 'uh oh something went wrong with request for hero: {0}'.format(heroID)
            else:
                data = response.json()
                post_id = db.hero_data.insert_one(data).inserted_id

                if(post_id):
                    print 'Added hero {0}'.format(data.name)





collect_data(game)
