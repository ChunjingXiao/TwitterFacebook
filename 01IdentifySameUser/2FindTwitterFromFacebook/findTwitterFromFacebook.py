# -*- coding: utf-8 -*-
# input: facebookProfile
# |::|json format file from Facebook APIs|;;|

# output: findTwitterFromFacebook
# facebookID   #likes  twitterAccount   website1;website2
# 133130832352	3062	4am_rock	www.twitter.com/4am_rock;www.myspace.com/04am;itunes.apple.com/us/album/light-from-light/id362464568;www.youtube.com/4am100

# twitterAccount: if the Twotter account is not found,  twitterAccount is 0 

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


def findTwitter(current):
    #reSplit = re.compile(r'\s*[,]*\s*')
    #newTagList = reSplit.split(newTagEn)
    #Description = Description.decode('unicode_escape','ignore')
        
    #http://www.facebook.com/profile.php?id=1825156357
          
    #http://twitter.com/#!/dinolikescrayon
    #current = current.replace('#!/','')
    current = current.replace('#!','')
    current = current.replace("\\/","/")
    # \W : [^a-zA-Z0-9_]
    reTwitter = re.compile('twitter.com/(.+?)\W',re.S)
    tempTwitter = reTwitter.findall(current)
    for i in range(0,len(tempTwitter)):
        tempTwitter[i] = tempTwitter[i].replace('/','')
        
    if(len(tempTwitter) == 0):
        tempTwitter = ['0'] 
    if (tempTwitter[0] == ' '):
        tempTwitter = ['0']    
    return tempTwitter[0]

def facebookProfile(fileName,fout,userList):
    # extract Twitter and Link from Facebook Profiles
    # output: 
    # facebookUserID likes TwitterName link
    fin = open(fileName)
    columnMark =  '|::|'
    rowMark = '|;;|\n'
    count = 0   
    for current in fin:
        if not (current[0:4] == columnMark and current[-5:] == rowMark): 
            continue
        count += 1 # allCount
        if(count % 100000 == 0):
            print count
        data2 = current[4:-5]  
        data = data2.replace("\\/","/")
        data = data.replace("\\n"," ")
        dataJson = minjson.safeRead(data)
        userID = dataJson['id']
        
        #if(userID == '108756882487616'):
        #    print data
        
        if (dataJson.has_key('likes')):
            likes = dataJson['likes']
        else:
            continue
            #print current
            #likes = '0'
        if (dataJson.has_key('website')):
            website = dataJson['website']
            website = website.replace("\n"," ")
            website = website.replace(";"," ")
            website = website.replace("\t"," ")
            website = website.replace("  "," ")
            website = website.replace("\\/","/")
            website = website.replace("http:\\","")
            websiteList  = website.split(' ')
            website = ''
            for urlLink in websiteList:
                if (len(urlLink) <=1 ):
                    continue
                urlLink = urlLink.replace("http://","")
                if (urlLink[len(urlLink)-1:len(urlLink)] == "/"):
                    urlLink = urlLink[0:len(urlLink)-1]                
                website += urlLink + ';'
            if (website[len(website)-1:len(website)] == ";"):
                website = website[0:len(website)-1]
        else:
            website = '0'
        if (dataJson.has_key('description')):
            description = dataJson['description']
            #description = description.decode('unicode_escape','ignore')
        else:
            description = '0'
        if (dataJson.has_key('general_info')):
            general_info = dataJson['general_info']
        else:
            general_info = '0'
        if (dataJson.has_key('about')):
            about = dataJson['about']
        else:
            about = '0'
        if (not userList.has_key(userID)):
            userList[userID] = 1
        else:
            #print userID
            continue   # if repeated, skip
        twitterAccount = findTwitter(website  + '|')
        if (twitterAccount == '0'):
            twitterAccount = findTwitter(description  + '|')
        if (twitterAccount == '0'):
            twitterAccount = findTwitter(general_info  + '|')
        if (twitterAccount == '0'):
            twitterAccount = findTwitter(about  + '|')
        
        fout.write(userID + '\t' + str(likes) + '\t' + twitterAccount + '\t' + website + '\n')
        
def multipleFiles(inFile, inFile2):
    fout = open(inFile2,"w")
    fileCount = 0
    userList = {} # userList[userID] = 1, this is used to remove repeated users
    for root, dirs, files in os.walk(inFile):
        for name in files:
            fileCount += 1
            print str(fileCount) + '::currentFile::' + name
            facebookProfile(os.path.join(root, name),fout,userList)    
def main(argv):    
    inFile = (argv[1])  # facebookProfile 
    inFile2= (argv[2])  # findTwitterFromFacebook
    

    multipleFiles(inFile, inFile2)
    #fout = open(inFile2,"w")
    #facebookProfile(inFile,fout)
        
    


if __name__ == "__main__":
    #ִmain fuction
    main(sys.argv)

