# -*- coding: utf-8 -*-
# find the account of twitter and account of facebook of the same user, below is the method
# (1) if facebook acount can be found from twitter profiles:  findFacebookFromTwitter
# (2) if twitter acount can be found from facebook profiles:  findTwitterFromFacebook
# (1) if links in twitter profiles and facebook profiles are the same: LinkTwitterSameFacebookLink

# inFile: findFacebookFromTwitter
# userID     #follower  facebookAccount       Url                       screenName
# 104967519	252	0	        www.caorda.com	                caorda
# 30693817	488	cookiemodel	facebook.com/cookiemodel	cookiemodel
#    0           1        2                   3                           4
# inFile2: findTwitterFromFacebook
# facebookID   #likes  twitterAccount   website1;website2
# 133130832352	3062	4am_rock	www.twitter.com/4am_rock;www.myspace.com/04am;itunes.apple.com/us/album/light-from-light/id362464568;www.youtube.com/4am100
#    0           1        2               3

# output: findBothFacebookTwitter 
# twitterID   #followr FacebookID     #likes    Url                         
# 40053156	28	rwilderjr	0	www.facebook.com/rwilderjr
# 30693817	488	cookiemodel	0	facebook.com/cookiemodel
import urllib2
import urllib
import re
import datetime
import time
import sys
import os
import traceback 
from urllib2 import HTTPError, Request, urlopen, URLError

def extractBothUsers(inFile, inFile2,outFile):
    fout = open(outFile,"w")
    fin = open(inFile) # findFacebookFromTwitter
    twitterLinkDict = {} # twitterLinkDict[url] = [userID, #follower]
    count = 0
    for current in fin:
        count += 1
        if(count % 1000000 == 0):
            print count        
        curL = current.split('\t')
        twitterLink = curL[3]
        if(curL[2] != '0'):   # facebookAccount != '0' 
            #fout.write(curL[0] + '\t' + curL[1] + '\t' + curL[2] + '\t' + twitterLink + '\t' + curL[4] + '\n')
            #         TwitterID   #follower        #facebookID          #likes          Url
            #fout.write(curL[0] + '\t' + curL[1] + '\t' + curL[2] + '\t' + '0'  + '\t' + twitterLink+ '\n')
            fout.write(curL[0] + '\t' + curL[1] + '\t' + curL[2] + '\t' + '0'  + '\t' + 'FacebookFromTwitterProfiles' + '\n')
            continue
        elif (twitterLink != '0'):   # Url != '0'
            if (not twitterLinkDict.has_key(twitterLink)):
                twitterLinkDict[twitterLink] = [curL[0], curL[1]] # [userID, #follower]
            else:
                #print twitterLink]
                if(len(curL[1]) > len(twitterLinkDict[twitterLink][1])):       # if current users has bigger followers, then use this one.
                    twitterLinkDict[twitterLink] = [curL[0], curL[1]]
    fin2 = open(inFile2) # findTwitterFromFacebook
    count = 0
    for current in fin2:
        # there exist repeated matches, I don't deal with this problems, I will remove this kind user by comparing their published URLs
        # in findFacebookFromTwitter
        # 15104164	6247	0	benzimmer.com	bgzimmer
        # 75269226	6898	0	topics.nytimes.com/topics/features/magazine/columns/on_language/index.html	OnLanguage
        # in findBothFacebookTwitter
        # 15104164	6247	123505557709785	498	benzimmer.com;topics.nytimes.com/topics/features/magazine/columns/on_language/index.html
        # 75269226	6898	123505557709785	498	benzimmer.com;topics.nytimes.com/topics/features/magazine/columns/on_language/index.html
        
        count += 1
        if(count % 1000000 == 0):
            print count           
        current2 = current.replace('\n','')
        curL = current2.split('\t')
        if(curL[2] != '0'): 
            #         TwitterID   #follower       #facebookID         #likes              Url
            #fout.write(curL[2] + '\t' + '0' + '\t' + curL[0] + '\t' + curL[1]  + '\t' +  curL[3] + '\n')
            fout.write(curL[2] + '\t' + '0' + '\t' + curL[0] + '\t' + curL[1]  + '\t' +  'TwitterFromFacebookProfiles' + '\n')
        elif (curL[3] != '0'):   # Url != '0'
            fbLinkList = curL[3].split(';')
            for oneUrl in fbLinkList:
                if (twitterLinkDict.has_key(oneUrl)):  # if links in twitter profiles and facebook profiles are the same                     
                    #fout.write(twitterLinkDict[oneUrl][0] + '\t' + twitterLinkDict[oneUrl][1] + '\t' + curL[0] + '\t' + curL[1]  + '\t' + curL[3] + '\n')
                    fout.write(twitterLinkDict[oneUrl][0] + '\t' + twitterLinkDict[oneUrl][1] + '\t' + curL[0] + '\t' + curL[1]  + '\t' + 'LinkTwitterSameFacebookLink' + '\n')
def main(argv):    
    inFile = argv[1]  # findFacebookFromTwitter
    inFile2= argv[2]  # findTwitterFromFacebook
    outFile = argv[3] # getTiwtterFacebook
    

    extractBothUsers(inFile, inFile2,outFile)
    #fout = open(inFile2,"w")
    #twitterProfile(inFile,fout)
        
    


if __name__ == "__main__":
    #ִmain fuction
    main(sys.argv)

