#!/usr/bin/python
#encoding: utf-8
import tinysegmenter
import operator
import requests
import json
import io

import argparse
import sys

parser = argparse.ArgumentParser(description='This script will parse .ass file to .json representation')
#parser.add_argument('')
#parser.add_argument('--name',dest='output_name',required=True)
parser.add_argument('-f',dest='filepath',required=True)
parser.add_argument('-v',dest='verbose',type=bool,default=False)


del sys.argv[0]

args_dict = vars(parser.parse_args(sys.argv))
filepath = args_dict['filepath']

#figure out what dir based on name and episode...eventually will be command line args
#show = 'hyouka'
#episode = '1'
#filename= './{0}_subs/{0}{1}.ass'.format(show,episode)

#open the file, then open the output
#inputfile = open(filename)
inputfile = open(filepath)
max_line = 0    
#outputfilename = './{0}_subs/{0}{1}_csv.txt'.format(show,episode)

#outputfile = open(outputfilename,'w')
outputfile = open('test.txt','w')

print 'successfully opened file'
#strip away the metadata from the subtitles
line_list = []
for line in inputfile:
    if line[0]=='D':
        
        timestamp_list = line.split(',,')

        just_diag = timestamp_list[len(timestamp_list)-1].strip()
        line_list.append(just_diag.decode('utf-8'))

        #line_list.append(just_diag)
        if len(just_diag)>max_line:
            max_line = len(just_diag)
        
print 'finished stripping metadata'
#open the segmenter
segmenter = tinysegmenter.TinySegmenter()

line_tokens_list = []

#for line of dialogue in subs
word_id = 0

for line in line_list:
    print line
    word_list = []
    #split it
    line_split = segmenter.tokenize(line)

    #for word in split line
    for word in line_split:
        if (word!= u' '):
            word_obj = {}
            word_obj['word'] = word
            word_obj['id'] = word_id

            word_list.append(word_obj)
            
            word_id += 1
    #print list(word_list)
    # 'hello'
    line_tokens_list.append(word_list)
    #print list(line_list    )
print 'finished looping'
#with io.open(outputfilename,'w',encoding='utf8') as outputfile:
outputfile.write(json.dumps(line_tokens_list,ensure_ascii=False).encode('utf8'))



        


