#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the PyMVPA package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
from pymongo import MongoClient
import argparse
import sys

client = MongoClient('mongodb://localhost:27017')

parser = argparse.ArgumentParser(description='This is the script which handles data collection for the app. Takes --game inputs')

parser.add_argument('--game',dest='game',required=True)
parser.add_argument('--kernel',dest='kernel',default='all')

del sys.argv[0]

args_dict = vars(parser.parse_args(sys.argv))
game = args_dict['game']
kernel = args_dict['kernel']

print kernel

def load_characters(game):
  characters = []
  return characters
