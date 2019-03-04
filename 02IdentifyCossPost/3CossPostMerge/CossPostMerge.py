# -*- coding: utf-8 -*-

# input1: IdentifyCossPostText   
# twUserID	twTweetID	fbUserID	fbFeedID  urlOrderNum #twRT #twFavorite	#twComment #fbReshare #fbLikes #fbComment timeDifference  twitterName facebookName 
# 19019298	7.14543E+17	37791069588	1.01541E+16	13	1	1	    0	        0	0	0	    -4	        IAmBiotech	IAmBiotech
# 13877002	7.15385E+17	72139486384	1.01541E+16	1	2	4	    0	        1	7	2	    -583	clarionledger	clarionledger
#   0              1                2             3             4       5       6           7           8       9       10           11               12            13

# input2: IdentifyCossPostUrl
# twUserID	twTweetID	fbUserID	fbFeedID  urlOrderNum #twRT #twFavorite	#twComment #fbReshare #fbLikes #fbComment timeDifference  twitterName facebookName 
# 19019298	7.14543E+17	37791069588	1.01541E+16	13	1	1	    0	        0	0	0	    -4	        IAmBiotech	IAmBiotech
# 13877002	7.15385E+17	72139486384	1.01541E+16	1	2	4	    0	        1	7	2	    -583	clarionledger	clarionledger
#   0              1                2             3             4       5       6           7           8       9       10           11               12            13

# output: CossPostMerge      
# twUserID	twTweetID	fbUserID	fbFeedID  urlOrderNum #twRT #twFavorite	#twComment #fbReshare #fbLikes #fbComment timeDifference  twitterName facebookName 
# 19019298	7.14543E+17	37791069588	1.01541E+16	13	1	1	    0	        0	0	0	    -4	        IAmBiotech	IAmBiotech
# 13877002	7.15385E+17	72139486384	1.01541E+16	1	2	4	    0	        1	7	2	    -583	clarionledger	clarionledger
#   0              1                2             3             4       5       6           7           8       9       10           11               12            13

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
#from nltk.metrics import edit_distance
import numpy as np
from scipy.spatial import distance

def printTime(beginTime):
    endTime = datetime.datetime.now() #calculate time
    print ("------------consumed-----------time-----------begin-----------")
    print ("consumed time:" + str(endTime - beginTime) )
    print ("------------consumed-----------time-----------end-------------")



# input1: IdentifyCossPostText    
# twUserID	twTweetID	fbUserID	fbFeedID  urlOrderNum #twRT #twFavorite	#twComment #fbReshare #fbLikes #fbComment timeDifference  twitterName facebookName 
# 19019298	7.14543E+17	37791069588	1.01541E+16	13	1	1	    0	        0	0	0	    -4	        IAmBiotech	IAmBiotech
# 13877002	7.15385E+17	72139486384	1.01541E+16	1	2	4	    0	        1	7	2	    -583	clarionledger	clarionledger
#   0              1                2             3             4       5       6           7           8       9       10           11               12            13
def readCossPostText(inFile1, tweetFeedDictAll):
    fin = open(inFile1) 
    count =0
    selectCount = 0
    for current in fin:
        count += 1
        data = current.replace('\n','')
        curL = data.split('\t')
        tweetId = curL[1]
        feedId = curL[3]
        if(not tweetFeedDictAll.has_key(tweetId + "," + feedId)):
            tweetFeedDictAll[tweetId + "," + feedId] = current
def writeFile(outFile,tweetFeedDictAll):
    fout = open(outFile,'w')
    for(ids,content) in tweetFeedDictAll.items():
        fout.write(content)
        
def main(argv):
    inFile1 = argv[1]   # IdentifyCossPostText
    inFile2 = argv[2]   # IdentifyCossPostUrl
    outFile = argv[3]   # CossPostMerge
    beginTime = datetime.datetime.now() 
    
    tweetFeedDictAll = {}  # tweetFeedDict[tweetId + feedId] = current
    readCossPostText(inFile1, tweetFeedDictAll)
    readCossPostText(inFile2, tweetFeedDictAll)
    
    
    writeFile(outFile,tweetFeedDictAll)



    printTime(beginTime)
    print "\a"
    print 'finish' 

    
if __name__ == "__main__":
    #ִmain fuction
    main(sys.argv)
