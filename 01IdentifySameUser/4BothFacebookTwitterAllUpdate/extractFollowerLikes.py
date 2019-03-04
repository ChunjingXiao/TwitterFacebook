# -*- coding: utf-8 -*-
# update the #follower and #likes in findBothFacebookTwitterAll from the twitter profiles and facebook profiles

# inFile: findBothFacebookTwitterAll
# twitterID   #followr FacebookID     #likes    Url                   
# 40053156	28	rwilderjr	0	www.facebook.com/rwilderjr
# 30693817	488	cookiemodel	0	facebook.com/cookiemodel

#inFile2: TwitterProfileData
# 'UserID','Name','ScreenName','Location','Description','Url','Protected','Follower','Friend','CreatedAt','Favourite','UtcOffset','TimeZone','Status','Lang','List'
#     userID         Name          screenName          Location      Description                    Url              Protected Follower Friend  
# |::|21579600|::|Sarah Fleenor|::|SarahFleenor|::|Indianapolis|::|25.Has.......IUPUI Alum.|::|http://t.co/F0RCZAemX4|::|False|::|353|::|382|::|
#       0             1               2                  3               4                           5                     6       7      8
#    CreatedAt       Favourite  UtcOffset         TimeZone              Status   Lang List   lastTweetTime           lastTweet
# 2009-02-22 17:18:31|::|1241|::|-14400|::|Eastern Time (US & Canada)|::|18689|::|en|::|8|::|2016-04-14 22:36:08|::|{'contributors': .... None}|;;|
#       9                 10       11               12                    13      14    15        16                    17

#inFile3: FacebookProfileData
#|::|json format file from Facebook APIs|;;|

#outFiel: findBothFacebookTwitterAllUpdate
# twitterID   #followr  FacebookID     #likes    howMatchUserID                   twitterName    TwitterUrl             facebookName      facebookUrl
# 126830575	443	127122857320666	998	FacebookFromTwitterProfiles	AGNewHaven	https://t.co/AOwdu58GIv	 agnewhaven	http://www.agnewhaven.com
# 70598975	1929	11553867053	5557	FacebookFromTwitterProfiles	LavishandLime	http://t.co/FnESasWZhK	lavishandlime	URL: http://www.lavishandlime.com Twitter: http://twitter.com/LavishandLime Pinterest: http://pinterest.com/lavishandlime Blog: http://lavishandlime.blogspot.ca/

import urllib2
import urllib
import re
import datetime
import time
import sys
import os
import traceback 
from urllib2 import HTTPError, Request, urlopen, URLError
import minjson

def readBothFile(inFile,outFile,twitterFollower,facebookLikes):
    # twitterFollower[user] = [userid, #followr, screenName, link]
    fout = open(outFile,"w")
    fin = open(inFile) # findBothFacebookTwitterAll
    for current in fin:
        current = current.replace('\n','')
        curL = current.split('\t')
        twitter = curL[0]
        follower = 0
        facebook = curL[2]
        likes = 0
        isTwitter = 0
        isFacebook = 0
        if (twitterFollower.has_key(twitter)):
            follower = twitterFollower[twitter][1]
            isTwitter = 1
        if (facebookLikes.has_key(facebook)):
            likes = facebookLikes[facebook][1]
            isFacebook = 1
        if (isTwitter == 1 and isFacebook ==1 ): # select users who have twitter profiles and facebook profiles
            #fout.write( twitterFollower[twitter][0] + '\t' + str(follower) + '\t' + facebookLikes[facebook][0] + '\t' + str(likes)  + '\t' + curL[4] + '\n')
            fout.write( twitterFollower[twitter][0] + '\t' + str(follower) + '\t' + facebookLikes[facebook][0] + '\t' + str(likes)  + '\t' + curL[4] )
            fout.write( '\t' + twitterFollower[twitter][2] + '\t' + twitterFollower[twitter][3] + '\t' + facebookLikes[facebook][2] +  '\t' + facebookLikes[facebook][3] +'\n')

def extractTwitterFollower(inFile2,twitterFollower):
    columnMark =  '|::|'
    rowMark = '|;;|\n'
    count = 0
    fin = open(inFile2) # TwitterProfileData
    for current in fin:
        if not (current[0:4] == columnMark and current[-5:] == rowMark): 
            continue 
        count += 1 # allCount
        if(count % 100000 == 0):
            print 'twitterFollower:' + str(count)
        data = current[4:-5]
        data = data.replace('\n','')
        curL = data.split(columnMark)
        userId = curL[0]
        screenName = curL[2]
        follower = curL[7]  
        link = curL[5]
        if (not twitterFollower.has_key(userId)):  # twitterFollower[user] = [userid, #followr, screenName, link]
            twitterFollower[userId] = [userId, follower, screenName,link]
        if (not twitterFollower.has_key(screenName)):
            twitterFollower[screenName] = [userId, follower, screenName,link]

def multipleFilesTwitter(inFile2,twitterFollower):
    fileCount = 0
    for root, dirs, files in os.walk(inFile2):
        for name in files:
            fileCount += 1
            print str(fileCount) + '::currentFile::' + name
            extractTwitterFollower(os.path.join(root, name),twitterFollower)
    print 'twitterFollower is done:' + str(len(twitterFollower))
def extractFacebookLikes(inFile3,facebookLikes):
    columnMark =  '|::|'
    rowMark = '|;;|\n'
    count = 0   
    fin = open(inFile3)
    for current in fin:
        if not (current[0:4] == columnMark and current[-5:] == rowMark): 
            continue
        count += 1 # allCount
        if(count % 1000 == 0):
            print 'facebookLikes:' + str(count)
        data2 = current[4:-5] 
        if(len(data2) <= 5): # if |::|400|;;|, continue
            continue
        data = data2.replace("\\/","/")
        data = data.replace("\\n"," ")
        dataJsonList = minjson.safeRead(data)
        for (oneUser,dataJson) in dataJsonList.items():
            userId = dataJson['id']
            if (dataJson.has_key('username')):
                userName = dataJson['username']
            else:
                userName = oneUser    
            if (dataJson.has_key('likes')):
                likes = dataJson['likes']
            else:
                likes = 0
            website =  '0'
            if (dataJson.has_key('website')):
                website = dataJson['website']
                #website = website.replace("\n",";")
                #website = website.replace("\t",";")
                #website = website.replace("  "," ")
                #website = website.replace("  "," ")
                #print 'before::' + website
                website = re.sub('\s+',';',website)
                website = website.replace("\\/","/")
                #website = website.replace("http://","")
                #print 'after::' + website
    
            if (not facebookLikes.has_key(userId)):
                facebookLikes[userId] = [userId, likes,userName,website]
            if (not facebookLikes.has_key(userName)):
                facebookLikes[userName] = [userId, likes,userName,website]

def multipleFilesFacebook(inFile3,facebookLikes):
    fileCount = 0
    for root, dirs, files in os.walk(inFile3):
        for name in files:
            fileCount += 1
            print str(fileCount) + '::currentFile::' + name
            extractFacebookLikes(os.path.join(root, name),facebookLikes)
    print 'facebookLikes is done:' + str(len(facebookLikes))
def main(argv):    
    inFile = argv[1]  # findBothFacebookTwitterAll
    inFile2 = argv[2]  # TwitterProfileData   
    inFile3 = argv[3]  # FacebookProfileData
    outFile = argv[4]  # findBothFacebookTwitterAllUpdate


    twitterFollower = {} # twitterFollower[user] = [userid, #followr, screenName, link]     
    multipleFilesTwitter(inFile2,twitterFollower)
    #extractFollower(inFile2,twitterFollower)
    
    facebookLikes = {} # facebookLikes[user] = [userid, #likes, name, link]
    multipleFilesFacebook(inFile3,facebookLikes)
    #extractLikes(inFile3,facebookLikes)
    
    readBothFile(inFile,outFile,twitterFollower,facebookLikes)


if __name__ == "__main__":
    #ִmain fuction
    main(sys.argv)

