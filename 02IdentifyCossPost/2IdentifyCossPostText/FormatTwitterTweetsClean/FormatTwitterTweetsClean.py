# -*- coding: utf-8 -*-
#clean text for IdentifySameText.py, because this step is slow
# remove URL, non-English...... 

# input1: FormatTwitterTweets:
#    userID       TweetID            #RT #favorite #comment    date         isRT isRep      expandURL    #mentions #hashtage   text
#|::|14985126|::|714569507218456577|::|1|::|2|::|0|::|2016-03-28 21:47:01|::|0|::|0|::|http://bit.ly/1LammK9|::|0|::|0|::|Deal Alert: New York to Australia from $632 round-trip: https://t.co/erHKWcOZBQ https://t.co/Bwwmpnscr9|;;|
#    0                  1              2    3    4               5           6    7            8                9    10        11   

# outfile: FormatTwitterTweetsClean:
#    userID       TweetID            #RT #favorite #comment    date         isRT isRep      expandURL    #mentions #hashtage   text
#|::|14985126|::|714569507218456577|::|1|::|2|::|0|::|2016-03-28 21:47:01|::|0|::|0|::|http://bit.ly/1LammK9|::|0|::|0|::|deal alert new york to australia from 632 round-trip |;;|
#    0                  1              2    3    4               5           6    7            8                9    10        11   

import urllib2
import urllib
import cookielib
import re
import datetime
import time
import sys
import os
import traceback
import math


def printTime(beginTime):
    endTime = datetime.datetime.now() #calculate time
    print ("------------consumed-----------time-----------begin-----------")
    print ("consumed time:" + str(endTime - beginTime) )
    print ("------------consumed-----------time-----------end-------------")




def cleanContent(tweet):
    tweet = tweet + ' '
    #tweet = "The Coolest Photo Bag You've Ever Seen http://t.co/NImuwiCz #cartoon #cheese #photo @jumpfrompaper" 
        
    reUrl = re.compile(r'http://(.+?)[ ,!:;\s]')   #-----------------------remove Urls--------------------------------filter----------------- 
    newT = reUrl.sub(' ',tweet)
    
    reUrl2 = re.compile(r'https://(.+?)[ ,!:;\s]') #-----------------------remove Urls--------------------------------filter----------------- 
    newT = reUrl2.sub(' ',newT)
    
    reUrl3 = re.compile(r'www.(.+?)[ ,!:;\s]')     #-----------------------remove Urls--------------------------------filter----------------- 
    newT2 = reUrl3.sub(' ',newT)
    
    #reMention = re.compile(r'@(.+?)[^\w]')         #-----------------------remove Mention-----------------------------filter----------------- 
    #newT2 = reMention.sub(' ',newT)
    
    #reHashtag = re.compile(r'#(.+?)[^\w]')        #-----------------------remove Hashtag-----------------------------filter----------------- 
    #newT2 = reHashtag.sub(' ',newT2)    

    reNonUtf8 = re.compile(r'\\u(.+?)[ ,.!:;\s]')   #-----------------------remove \u2014------------------------------filter----------------- 
    newT2 = reNonUtf8.sub(' ',newT2)
    
    reNonABC123 = re.compile(r'(?![\'-])[^\w]')     #-----------------------remove punctuation except '- ----------------filter----------------- 
    newT2 = reNonABC123.sub(' ',newT2)    
    
    if(1):  # stopwords
        reSplit = re.compile('[\s]+')
        wordList = reSplit.split(newT2)        
        writeContent = ''
        lastOne = ''
        isWrite = 0
        for one in wordList:
            one2 = one.lower()
            one2 = one2.strip()
            
            if(one2.startswith('\'') or one2.endswith('\'')):   #-----------------------remove ' in start and end pos-----------------filter----------------- 
                one = one.replace('\'','')    
            if(one2.endswith('\'s')):   #-----------------------remove 's in  end pos-------------------------filter----------------- 
                one = one.replace('\'s','')        
            #if (one2.isdigit()):              #-----------------------remove 0123456789-----------------filter----------------- 
            #    continue
            #if(stopWords.has_key(one2)):   #-----------------------remove stopWords--------------------------------filter----------------- 
            #    continue
            #if(len(one2) <= 2):            #-----------------------remove length <= 2--------------------------------filter----------------- 
            #    continue
            '''
            try:
                aa = float(one)
                continue
            except:
                pass
            '''
            writeContent += one + ' '

    reBlanket = re.compile(r'[\s]+')
    writeContent = reBlanket.sub(' ',writeContent) #-----------------------remove space------------------------------filter----------------- 
    return writeContent.lower()
def readTweets(inFile1,outFile):
    fin = open(inFile1)
    fout = open(outFile,'w')
    
    columnMark =  '|::|'
    rowMark = '|;;|\n'  
    count =0
    for current in fin:
        count +=1
        if (count % 500000 ==0):
            print count        
        data = current[4:-5]
        curL = data.split(columnMark)
        userID = curL[0]
        message = cleanContent(curL[11])
        for ii in range(11):
            fout.write(columnMark + curL[ii] )
        fout.write(columnMark + message + rowMark )

        
    fin.close()
    print '----readTweets finished------count----' + str(count) + '----'

def main(argv):
    inFile1 = argv[1]   # FormatTwitterTweets
    outFile = argv[2]   # FormatTwitterTweetsClean

  
    reload(sys)
    sys.setdefaultencoding('utf-8')
    beginTime = datetime.datetime.now() 
    
    readTweets(inFile1,outFile)

    printTime(beginTime)
    print "\a"
    print 'finish' 

    
if __name__ == "__main__":
    #ִmain fuction
    main(sys.argv)
