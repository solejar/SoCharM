#!/usr/bin/python
#encoding: utf-8
import tinysegmenter
import operator
import requests
#import json

show = 'bakemonogatari'
episode = '1'
filename= './{0}_subs/{0}{1}.ass'.format(show,episode)

inputfile = open(filename)
max_line = 0    
outputfilename = './{0}_subs/{0}{1}_stripped.txt'.format(show,episode)
outputfilenameFreq = './{0}_subs/{0}{1}_wordfreq.txt'.format(show,episode)
outputfile = open(outputfilename,'w')
outputfilenameSpaced = './{0}_subs/{0}{1}_spaced.txt'.format(show,episode)
outputfilespaced = open(outputfilenameSpaced,'w')

line_list = []
for line in inputfile:
    if line[0]=='D':
    	just_diag_line = line.split(',,')
	split_length = len(just_diag_line)
	just_diag = just_diag_line[split_length-1].strip()
        line_list.append(just_diag.decode('utf-8'))
        if len(just_diag)>max_line:
            max_line = len(just_diag)
        outputfile.write(just_diag + '\n')
    
print "done stripping the file of metadata!"

segmenter = tinysegmenter.TinySegmenter()
freq_dict = {}

particles = {u" ","が","を","です","ね","よ","に","も","と","か","だ",
"の","は","で","から",'この','いる','さん','さ','だよ','？','だろ','これ',
'こと','そう','し','それ','なん','その','ある','私','どう','でも','して','はい'}
partutf = {"x"}
for word in particles:
    partutf.add(word.decode('utf-8'))
for line in line_list:
    #print(line)
    line_split = segmenter.tokenize(line)
    for word in line_split:
        #if (word!= u' '):
        #if (word not in partutf):
            if (freq_dict.has_key(word)==1):
                freq_dict[word] = freq_dict[word] + 1
            else:
                freq_dict[word] = 1
            outputfilespaced.write(word.encode('utf-8') + ' ')
    outputfilespaced.write('\n')    
sorted_dict = sorted(freq_dict.items(),key =operator.itemgetter(1), reverse = True)
outputfile_sorted = open(outputfilenameFreq,'w')
for pair in sorted_dict:
    if (pair[1] > 1):
        word = pair[0].encode('utf-8')
        try: 
            response =  requests.get('http://beta.jisho.org/api/v1/search/words?keyword={0}'.format(word))
            #response = requests.get('http://dev.virtualearth.net/REST/v1/Traffic/Incidents/37,-105,45,-94?key=AtfNAQ2-7DO88zFVrB7xChxDexS3OHilo5phzX00d7qohRMS9WcERj2gv6zLr67s')

        except requests.ConnectionError:
            outputfile_sorted.write(word + ': ' + str(pair[1])+ ' no reading \n')    
        else:
            data = response.json()
            try:
                kana = data['data'][0]['japanese'][0]['reading']

                outputfile_sorted.write(word + ': ' + str(pair[1])+ ' ' + kana.encode('utf-8')+'\n')
            except IndexError:
                outputfile_sorted.write(word + ': ' + str(pair[1])+ ' no reading \n')
            except KeyError:
                outputfile_sorted.write(word + ': ' + str(pair[1])+ ' no reading \n')
        


