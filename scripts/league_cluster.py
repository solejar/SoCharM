#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the PyMVPA package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""
Self-organizing Maps
====================
.. index:: mapper, self-organizing map, SOM, SimpleSOMMapper
This is a demonstration of how a self-organizing map (SOM), also known
as a Kohonen network, can be used to map high-dimensional data into a
two-dimensional representation. For the sake of an easy visualization
'high-dimensional' in this case is 3D.
In general, SOMs might be useful for visualizing high-dimensional data
in terms of its similarity structure. Especially large SOMs (i.e. with
large number of Kohonen units) are known to perform mappings that
preserve the topology of the original data, i.e. neighboring data
points in input space will also be represented in adjacent locations
on the SOM.
The following code shows the 'classic' color mapping example, i.e. the
SOM will map a number of colors into a rectangular area.
"""
#PYTHONPATH=$PYTHONPATH:C/Users/Sean/proj/python/SoCharM
from mvpa2.suite import *
import argparse
import sys

#from operator import itemgetter, attrgetter, methodcaller

import matplotlib.pyplot as plt

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')

import projector

parser = argparse.ArgumentParser(description='This is the script which handles data collection for the app. Takes --game inputs')

parser.add_argument('--game',dest='game',default='league')
parser.add_argument('--kernel',dest='kernel',default='all')
parser.add_argument('--save',dest='save',default=False,type=bool)

#del sys.argv[0]

args_dict = vars(parser.parse_args(sys.argv[1:]))
game = args_dict['game']
kernel = args_dict['kernel']
save = args_dict['save']

kernel_map = {
    'league': {
        'all': [
            'features.attack',
            'features.difficulty',
            'features.armorperlevel',
            'features.armor',
            'features.hpregenperlevel',
            'features.hpregen',
            'features.attackspeedperlevel',
            'features.attackdamageperlevel',
            'features.attackdamage',
            'features.mpregenperlevel',
            'features.mpregen',
            'features.critperlevel',
            #'crit'
            'features.mrperlevel',
            'features.mr',
            'features.hpperlevel',
            'features.hp',
            'features.attackspeedoffset',
            'features.attackrange'
            'features.movespeed'
        ]
    },
    'overwatch': {

    },
    'dota2': {

    }

}

"""
First, we define some colors as RGB values from the interval (0,1),
i.e. with white being (1, 1, 1) and black being (0, 0, 0). Please
note, that a substantial proportion of the defined colors represent
variations of 'blue', which are supposed to be represented in more
detail in the SOM.
"""

db = client[game]

#fill characters
feature_list = kernel_map[game][kernel]
feature_list.append('name')
characters = projector.extract_features(game,feature_list)

#print characters[0]['features'].values()

character_list = [character['features'].values() for character in characters]

character_count = len(character_list)
character_names = [character['name'] for character in characters]
#print np.array_str(character_set[2],precision=4)

feature_count = len(character_list[0])
adjusted_feature_list = []
for i in range(0,feature_count):
    feature_vals = [character[i] for character in character_list]

    mean = np.mean(feature_vals)
    adjusted_feature_vals = feature_vals-mean

    std = np.std(adjusted_feature_vals)
    if(std):
        adjusted_feature_vals = adjusted_feature_vals/std

    else:
        adjusted_feature_vals = adjusted_feature_vals/sys.float_info.epsilon

    adjusted_feature_list.append(adjusted_feature_vals)

print 'finished scaling the features'

character_list = []
for i in range(0,character_count):
    character = []
    for feature in adjusted_feature_list:
        character.append(feature[i])
    character_list.append(character)

character_set = np.array(character_list)
#print character_set

"""
Now we can instantiate the mapper. It will internally use a so-called
Kohonen layer to map the data onto. We tell the mapper to use a
rectangular layer with 20 x 30 units. This will be the output space of
the mapper. Additionally, we tell it to train the network using 400
iterations and to use custom learning rate.
"""

#figure out what parameters need to be tweaked
som = SimpleSOMMapper((10, 20), 400, learning_rate=0.05)

"""
Finally, we train the mapper with the previously defined 'color' dataset.
"""
som.train(character_set)
#som.train(colors)

"""
Each unit in the Kohonen layer can be treated as a pointer into the
high-dimensional input space, that can be queried to inspect which
input subspaces the SOM maps onto certain sections of its 2D output
space.  The color-mapping generated by this example's SOM can be shown
with a single matplotlib call:
"""
#print som.K
#pl.imshow(som.K, origin='lower')
#plt.plot([1,2,3,4])
"""
And now, let's take a look onto which coordinates the initial training
prototypes were mapped to. The get those coordinates we can simply feed
the training data to the mapper and plot the output.
"""

mapped = som(character_set)

# SOM's kshape is (rows x columns), while matplotlib wants (X x Y)

xs = np.array([])
ys = np.array([])

named_results = []
for i, m in enumerate(mapped):
    result = {}
    #print i
    #print 'x,y: ({0},{1}), champion: {2}'.format(m[1],m[0],character_names[i])
    result['location'] = m.tolist()
    result['name'] = character_names[i]
    named_results.append(result)
    rand_xpos = m[1]+0.25*(np.random.rand()-0.5)
    rand_ypos = m[0]+0.25*(np.random.rand()-0.5)
    pl.text(rand_xpos, rand_ypos, character_names[i], ha='center', va='center',
           bbox=dict(facecolor='white', alpha=0.5, lw=0))
    xs = np.append(xs, rand_xpos)
    ys = np.append(ys,rand_ypos)#added with jiggle

sorted_map = sorted(named_results, key=lambda x: (x['location'][0],x['location'][1]))
#print sorted_map

db = client.league

old_cluster_key = sorted_map[0]['location']
curr_cluster_vals = []
if save:
    for result in sorted_map:

        curr_cluster_key = result['location']
        if(old_cluster_key!=curr_cluster_key):
            cluster = {
                'name' : '',
                'champions': curr_cluster_vals
            }

            post_id = db.results.insert_one(cluster).inserted_id
            if(not post_id):
                'something went wrong with result posting'
            curr_cluster_vals = []
        old_cluster_key = curr_cluster_key
        curr_cluster_vals.append(result)
        print result
    cluster = {
        'name': '',
        'champions': curr_cluster_vals
    }

    post_id=db.results.insert_one(cluster).inserted_id
    if(not post_id):
        'something went wrong with the insertion of a result'

pl.scatter(xs,ys)

pl.title('League SOM')

"""

The text labels of the original training colors will appear at the 'mapped'
locations in the SOM -- and should match with the underlying color.
"""

# show the figure
if cfg.getboolean('examples', 'interactive', True):
    pl.show()

"""
The following figure shows an exemplary solution of the SOM mapping of the
3D color-space onto the 2D SOM node layer:
.. image:: ../pics/ex_som.*
   :align: center
   :alt: Color-space mapping by a self-organizing map.
"""
