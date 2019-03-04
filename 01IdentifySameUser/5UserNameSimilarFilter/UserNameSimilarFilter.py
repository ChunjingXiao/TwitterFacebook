# -*- coding: utf-8 -*-
# filter users whose similarity of names in Twitter and Facebook is below 0.8

# inFile: BothFacebookTwitterAllUpdate 
# twitterID   #followr  FacebookID     #likes    howMatchUserID                   twitterName    TwitterUrl             facebookName      facebookUrl
# 126830575	443	127122857320666	998	FacebookFromTwitterProfiles	AGNewHaven	https://t.co/AOwdu58GIv	 agnewhaven	http://www.agnewhaven.com
# 70598975	1929	11553867053	5557	FacebookFromTwitterProfiles	LavishandLime	http://t.co/FnESasWZhK	lavishandlime	URL: http://www.lavishandlime.com Twitter: http://twitter.com/LavishandLime Pinterest: http://pinterest.com/lavishandlime Blog: http://lavishandlime.blogspot.ca/
#    0          1           2           3        4                                  5                  6                       7                8

# UserNameSimilarFilter
# twitterID  #followr FacebookID	#likes	howMatchUserID	                twitterName	TwitterUrl	        facebookName	    facebookUrl
# 126830575	443	1.27123E+14	998	FacebookFromTwitterProfiles	AGNewHaven	https://t.co/AOwdu58GIv	 agnewhaven	http://www.agnewhaven.com
#    0          1           2           3        4                                  5                  6                       7                8


import urllib2
import urllib
import re
import datetime
import time
import sys
import os
import traceback 
from urllib2 import HTTPError, Request, urlopen, URLError


def readAllData(inFile,allDataList):
    fin = open(inFile) # findBothFacebookTwitterAll
    for current in fin:
        current = current.replace('\n','')
        allDataList.append(current)
    print 'readAllData is done'
def removeRepeatedTwitter(allDataList):
    #fin = open(inFile) # findBothFacebookTwitterAll
    twitterFollower = {} # twitterFollower[userId] = #follower
    removeList = []
    for current in allDataList:
        #current = current.replace('\n','')
        curL = current.split('\t')
        twitter = curL[0]
        follower = int(curL[1])
        facebook = curL[2]
        likes = int(curL[3])
        if (not twitterFollower.has_key(twitter)):
            twitterFollower[twitter] = [follower,likes,current]
        else:
            if( follower + likes > twitterFollower[twitter][0] + twitterFollower[twitter][1]):
                twitterFollower[twitter] = [follower,likes,current]
                removeList.append(twitterFollower[twitter][2])
                #allDataList.remove(twitterFollower[twitter][2])
                #print "allDataList.remove:" + str(twitterFollower[twitter][2])
            else:
                removeList.append(current)
                #allDataList.remove(current)
                #print "allDataList.remove:" + str(current)
    for one in removeList:
        allDataList.remove(one)
    print 'removeRepeatedTwitter is done'
def removeRepeatedFacebook(allDataList):
    #fin = open(inFile) # findBothFacebookTwitterAll
    facebookLikes = {} # facebookLikes[userId] = #Likes
    removeList = []
    for current in allDataList:
        #current = current.replace('\n','')
        curL = current.split('\t')
        twitter = curL[0]
        follower = int(curL[1])
        facebook = curL[2]
        likes = int(curL[3])
        if (not facebookLikes.has_key(facebook)):
            facebookLikes[facebook] = [follower,likes,current]
        else:
            if( follower + likes > facebookLikes[facebook][0] + facebookLikes[facebook][1]):
                facebookLikes[facebook] = [follower,likes,current]
                if facebookLikes[facebook][2] in allDataList:
                    removeList.append(facebookLikes[facebook][2])
                    #allDataList.remove(facebookLikes[facebook][2])
                    #print "allDataList.remove:" + str(facebookLikes[facebook][2])
            else:
                if current in allDataList:
                    removeList.append(current)
                    #allDataList.remove(current)
                    #print "allDataList.remove:" + str(current)
    for one in removeList:
        allDataList.remove(one)
    print 'removeRepeatedFacebook is done'
def outallDataList(outFile,allDataList):
    
    foutAll = open(outFile + 'All',"w")
    for current in allDataList:
        curL = current.split('\t')
        #---------------------name similarity filter------------------begin---------------------
        linkType = curL[4]
        twName = curL[5]
        fbName = curL[7]
        if(linkType == "LinkTwitterSameFacebookLink"):
            simValue = compareName(twName,fbName)
            if(simValue < 0.8): #----------threshold is 0.8----------------------------
                continue
        #---------------------name similarity filter------------------end----------------------- 
        
        foutAll.write(current + '\n')
            
    print 'outallDataList is done'
def compareName(twName,fbName):
    s1 = twName.lower()
    s2 = fbName.lower()
    #s1Set = set(s1.split(''))
    s1Set = set(s1)
    s2Set = set(s2)
    commonWords = s1Set & s2Set 
    unionWords = s1Set | s2Set
    if(len(unionWords) == 0):
        return 0
    else:
        return round(float(len(commonWords)) / len(unionWords),4) 
    
def main(argv):    
    inFile = argv[1]  # BothFacebookTwitterAllUpdate
    outFile = argv[2]  # UserNameSimilarFilter

    allDataList = []
    readAllData(inFile,allDataList)
    
    removeRepeatedTwitter(allDataList)
    
    removeRepeatedFacebook(allDataList)
    
    outallDataList(outFile,allDataList)

    
    #twName = "nigeriafilms"
    #fbName = "nigeriafilmscom"
    #print compareName(twName,fbName)    


if __name__ == "__main__":
    #ִmain fuction
    main(sys.argv)

