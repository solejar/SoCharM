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
import preprocess_data as prep

client = MongoClient('mongodb://localhost:27017')

parser = argparse.ArgumentParser(description='This is the script which handles data collection for the app. Takes --game inputs')

parser.add_argument('--game',dest='game',default='league')
parser.add_argument('--save',dest='save',default=False)

args_dict = vars(parser.parse_args(sys.argv[1:]))
game = args_dict['game']
save = args_dict['save']

def collect_data(game):
    if(game=='league'):
        print 'game is League of Legends'
        db = client.league

        league_url = 'https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&champListData=all&tags=all&dataById=false'
        headers = {"X-Riot-Token": "RGAPI-fe756ea4-3914-44b1-a171-a0fd1851098f"}
        try:
            response = requests.get(league_url,headers=headers)
        except requests.ConnectionError:
            print 'uh oh something went wrong with the api'
        else:
            data = response.json()
            #print data
            champion_data = data['data']

            for champion, data in champion_data.iteritems():

                post_id = db.champion_data.insert_one(data).inserted_id
                if(post_id):
                    print 'Added champion {0}'.format(champion)

                flattened_champ = prep.flatten_data(game,data)

                post_id =db.champion_data_flattened.insert_one(flattened_champ).inserted_id
                if(post_id):
                    print 'successfully flattened champion {0}'.format(flattened_champ['name'])




    elif (game=='dota2'):
        db = client.dota2
        print 'game is DOTA'
    elif(game=='overwatch'):
        db = client.overwatch

        print 'game is overwatch'

        for heroID in range(1,25): #this is the amount of heros that api supports
            overwatch_url = 'https://overwatch-api.net/api/v1/hero/{0}'.format(heroID)
            try:
                response = requests.get(overwatch_url)
            except requests.ConnectionError:
                print 'uh oh something went wrong with request for hero: {0}'.format(heroID)
            else:
                data = response.json()

                flattened_hero= prep.flatten_data(game,data)
                if save:
                    post_id = db.hero_data.insert_one(data).inserted_id

                    if(post_id):
                        print 'added hero data'
                        #print 'Added hero {0}'.format(data['name'].decode('utf-8').encode('ascii','ignore'))

                    post_id = db.hero_data_flattened.insert_one(flattened_hero).inserted_id

                    if(post_id):
                        print flattened_hero.keys()
                        print "successfully flattened hero"
                        #print 'successfully flattened champion {0}'.format(flattened_hero['name'].decode('utf-8').encode('ascii','ignore'))







collect_data(game)
