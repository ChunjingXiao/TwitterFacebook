# -*- coding: utf-8 -*-
# input : TwitterProfile
# UserID Name ScreenName Location Description Url Protected Follower Friend CreatedAt Favourite UtcOffset TimeZone Status Lang List statusCreated  statusAll 
#   0     1       2         3         4        5      6        7        8       9         10       11        12      13    14   15        16           17

# outFile: findFacebookFromTwitter
# userID     #follower  facebookAccount       Url                       screenName
# 104967519	252	0	        www.caorda.com	                caorda
# 30693817	488	cookiemodel	facebook.com/cookiemodel	cookiemodel

# facebookAccount: if the Facebook account is not found,  facebookAccount is 0

import urllib2
import urllib
import re
import datetime
import time
import sys
import os
import traceback 
from urllib2 import HTTPError, Request, urlopen, URLError

def findFacebook(current):
    # there is a bug for http://www.facebook.com/colleen.hardcastle
    # this code extract colleen which is wrong. And the right one should be colleen.hardcastle
    current = current.replace('#!','')
    #http://www.facebook.com/home.php#!/AdielxCohen
    current = current.replace('home.php','')
    reFacebook = re.compile('facebook.com/(.+?)\W',re.S)
    tempFacebook = reFacebook.findall(current)
    for i in range(0,len(tempFacebook)):
        tempFacebook[i] = tempFacebook[i].replace('/','')
    removeList = ['page','pages','profile']
    for rem in removeList:
        while rem in tempFacebook:
            tempFacebook.remove(rem)
    if(len(tempFacebook) == 0):
        tempFacebook = ['0']
    return tempFacebook[0]
def twitterProfile(fileName,fout,userList):
    # extract Facebook and Link from Twitter Profiles
    # output:
    # twitterUserID twitterScreenName facebookName link
    columnMark =  '|::|'
    rowMark = '|;;|\n'
    fin = open(fileName)
    # UserID Name ScreenName Location Description Url Protected Follower Friend CreatedAt Favourite UtcOffset TimeZone Status Lang List statusCreated  statusAll 
    #   0     1       2         3         4        5      6        7        8       9         10       11        12      13    14   15        16           17
    count = 0
    for current in fin:
        if not (current[0:4] == columnMark and current[-5:] == rowMark): 
            continue
        count += 1 
        if(count % 100000 == 0):
            print 'fileName:' + fileName + ';;  current Count:' + str(count)
        data = current[4:-5]
        data = data.replace('\n','')
        currentSplit = data.split(columnMark)
        if (not userList.has_key(currentSplit[0])):
            userList[currentSplit[0]] = 1
        else:
            #print currentSplit[0]
            continue   # if repeated, skip
        getFacebook = findFacebook(currentSplit[4])
        urlLink = currentSplit[5]
        urlLink = urlLink.replace("http://","")
        if (urlLink[len(urlLink)-1:len(urlLink)] == "/"):
            urlLink = urlLink[0:len(urlLink)-1]
        if( urlLink == 'None'):
            urlLink = '0'
        if (getFacebook == '0'):
            getFacebook = findFacebook(urlLink  + '|')
        fout.write(currentSplit[0] + '\t' + currentSplit[7] + '\t' + str(getFacebook) + '\t' + urlLink + '\t' + currentSplit[2] + '\n')
        
def multipleFiles(inFile, inFile2):
    fout = open(inFile2,"w")
    fileCount = 0
    userList = {} # userList[userID] = 1, this is used to remove repeated users
    for root, dirs, files in os.walk(inFile):
        for name in files:
            fileCount += 1
            print str(fileCount) + '::currentFile::' + name
            twitterProfile(os.path.join(root, name),fout,userList)    
def main(argv):    
    inFile = (argv[1])  # TwitterProfile
    inFile2= (argv[2])  # findFacebookFromTwitter
    

    multipleFiles(inFile, inFile2)
    #fout = open(inFile2,"w")
    #twitterProfile(inFile,fout)
        
    


if __name__ == "__main__":
    #ִmain fuction
    main(sys.argv)

