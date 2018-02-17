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

def collect_data(game):
    if(game=='League of Legends'):
        league_url = 'https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&champListData=all&tags=all&dataById=false'
        headers = {"X-Riot-Token": "RGAPI-290454e6-05e1-4d05-a5b5-99e5b02dbc29"}
        try:
            response = requests.get(league_url,headers=headers)
        except requests.ConnectionError:
            print 'uh oh something went wrong with the api'
        else:
            data = response.json()
            champion_data = data['data']
            outputfile_name = 'single_example.json'
            outputfile = open(outputfile_name,'w')

            outputfile.write(json.dumps(champion_data['MonkeyKing'],indent=4))

    elif (game=='DOTA2'):
        print 'game is DOTA'
    elif(game=='Overwatch'):
        print 'game is Overwatch'

game = 'League of Legends'

collect_data(game)
