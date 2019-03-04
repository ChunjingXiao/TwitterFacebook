# TwitterFacebook
Find users who have accounts on both Twitter and Facebook, and identify cross-posts. Here,if a user publishes a tweet in Twitter and a feed in Facebook that contain the same information, we consider them as a cross-post). Just follow the ordinal values of the file names. 
 


# 01IdentifySameUser
The codes in this folder aim to match the accounts on Twitter and Facebook. And UserNameSimilarFilter is the result with 12976 users.

## 1FindFacebookFromTwitter:
This code extracts Facebook accounts from Twitter profiles.
 > input : TwitterProfile
 >> UserID Name ScreenName Location Description Url Protected Follower Friend CreatedAt Favourite UtcOffset TimeZone Status Lang List statusCreated  statusAll 

 > outFile: findFacebookFromTwitter
 >> userID     #follower  facebookAccount       Url                       screenName



## 2FindTwitterFromFacebook
This code extracts Twitter accounts from Facebook profiles.

 > input: facebookProfile
 >> |::|json format file from Facebook APIs|;;|

 > output: findTwitterFromFacebook
 >> facebookID   #likes  twitterAccount   website1;website2


## 3BothTiwtterFacebook

 Match the Twitter account and Tacebook account of the same user. Here are the methods:
    (1) if the Facebook acount can be found from Twitter profiles, it is selected and its matchedType is findFacebookFromTwitter
    (2) if the Twitter acount can be found from Facebook profiles, it is selected and its matchedType is findTwitterFromFacebook
    (3) if the links in Twitter and Facebook profiles are the same, it is selected and its matchedType is LinkTwitterSameFacebookLink

 > inFile: findFacebookFromTwitter
 >> userID     #follower  facebookAccount       Url                       screenName

 > inFile2: findTwitterFromFacebook
 >> facebookID   #likes  twitterAccount   website1;website2

> output: findBothFacebookTwitter
>> twitterID   #followr FacebookID     #likes    matchedType



## 4BothFacebookTwitterAllUpdate

Update the twitterName, facebookName, #follower and #likes in findBothFacebookTwitterAll based on the twitter profiles and facebook profiles

> inFile: findBothFacebookTwitterAll
>> twitterID   #followr FacebookID     #likes    Url

> inFile2: TwitterProfileData
>> 'UserID','Name','ScreenName','Location','Description','Url','Protected','Follower','Friend','CreatedAt','Favourite','UtcOffset','TimeZone','Status','Lang','List'

>　inFile3: FacebookProfileData
>>　|::|json format file from Facebook APIs|;;|

>　outFiel: findBothFacebookTwitterAllUpdate
>> twitterID   #followr  FacebookID     #likes    howMatchUserID                   twitterName    TwitterUrl             facebookName      facebookUrl

## 5UserNameSimilarFilter
filter users whose similarity of names in Twitter and Facebook is more than 0.8

> inFile: BothFacebookTwitterAllUpdate
>> twitterID   #followr  FacebookID     #likes    howMatchUserID                   twitterName    TwitterUrl             facebookName      facebookUrl

> outFile: UserNameSimilarFilter
>> twitterID  #followr FacebookID	#likes	howMatchUserID	                twitterName	TwitterUrl	        facebookName	    facebookUrl

# 02IdentifyCossPost
The codes in this folder aim to identify cross-posts from Twitter and Facebook. And CossPostMergeFilter.rar is the result with 468,011 cross-posts.

## 1IdentifyCossPostUrl
 This is used to match whether tweets in Twitter and feeds in Facebook from the same user contain the same URLs.
 PS: this use the function: isSameUrl(url1,url2) in IdentifySameUrls.py



> input1: IdentifySameUser
>> twitterID #followr #twitterUrl #sameLongUrl FacebookID #likes #facebookUrl     howMatchUserID        twitterName       facebookName   timeZone 
>> 109118967	3904208	41	    5	113525172018777	2464791	12	FacebookFromTwitterProfiles	jaimecamil	jaimecamil      -14400
>> 62477022	244525	15	    7	192465074360	1724259	14	FacebookFromTwitterProfiles	andaadam	AndaAdamOfficial -18000

> input2: expandDnsTwitterData
>> shortURL                               longURL                                       status
>> http://bit.ly/1Ux1bFx	https://amp.twimg.com/v/77996099-1089-4371-944d-3e863875fd7b	200
>> http://www.warnerchannel.com	http://www.warnerchannel.com/co/	200

> input3: expandDnsFacebookData
>> shortURL                               longURL                                       status

> input4: FormatTwitterTweets
>>    userId       TweetID            #RT #favorite #comment    date         isRT isRep      expandURL    #mentions #hashtage   text
>> |::|14985126|::|714569507218456577|::|1|::|2|::|0|::|2016-03-28 21:47:01|::|0|::|0|::|http://bit.ly/1LammK9|::|0|::|0|::|What to https://t.co/WdNuNLJ0Mu|;;|
>> |::|14985126|::|714520937341784064|::|2|::|3|::|0|::|2016-03-28 18:34:01|::|0|::|0|::|http://bit.ly/1o0Yy0R|::|0|::|0|::|When it https://t.co/ad5Go6wy7q https://t.co/N06Lnne6yE|;;|

> input5: FormatFacebookFeeds
>> userId		feedID	#shares	#likes	#comments	created_time	    type	status_type	link	            name	description	message
>> |::|94319190752|::|10153640474135753|::|3|::|7|::|7|::|2016-04-14 02:00:00|::|link|::|shared_story|::|http://www.patheos.com|::|Sex and|::|For the|::|Even if|;;|
>> |::|94319190752|::|10153640287040753|::|0|::|5|::|1|::|2016-04-14 00:00:00|::|link|::|shared_story|::|http://www.patheos.com|::|Are Polytheists |::|Why is|::|Yvonne|;;|

> output: IdentifyCossPostUrl  # is used for Question2EffectIdeal, Question3PostAll, and experiments
>> twUserID	twTweetID	fbUserID	fbFeedID  urlOrderNum #twRT #twFavorite	#twComment #fbReshare #fbLikes #fbComment timeDifference  twitterName facebookName 
>> 19019298	7.14543E+17	37791069588	1.01541E+16	13	1	1	    0	        0	0	0	    -4	        IAmBiotech	IAmBiotech
>> 13877002	7.15385E+17	72139486384	1.01541E+16	1	2	4	    0	        1	7	2	    -583	clarionledger	clarionledger




## 2IdentifyCossPostText
Match cross-posts by text similarity

> input1: IdentifySameUser    # generated by TwitterFacebookData2017\01IdentifySameUser
>> twitterID #followr #twitterUrl #sameLongUrl FacebookID #likes #facebookUrl     howMatchUserID        twitterName       facebookName   timeZone 
>> 109118967	3904208	41	    5	113525172018777	2464791	12	FacebookFromTwitterProfiles	jaimecamil	jaimecamil      -14400
>> 62477022	244525	15	    7	192465074360	1724259	14	FacebookFromTwitterProfiles	andaadam	AndaAdamOfficial -18000

> input2: FormatTwitterTweets:
>>    userID       TweetID            #RT #favorite #comment    date         isRT isRep      expandURL    #mentions #hashtage   text
>> |::|14985126|::|714569507218456577|::|1|::|2|::|0|::|2016-03-28 21:47:01|::|0|::|0|::|http://bit.ly/1LammK9|::|0|::|0|::|What to https://t.co/WdNuNLJ0Mu|;;|

> input3: FormatFacebookFeeds
>> userID		feedID	#shares	#likes	#comments	created_time	    type	status_type	link	            name	description	message
>> |::|94319190752|::|10153640287040753|::|0|::|5|::|1|::|2016-04-14 00:00:00|::|link|::|shared_story|::|http://www.patheos.com|::|Are Polytheists |::|Why is|::|Yvonne|;;|

> output: IdentifyCossPostText  # is used for Question2EffectIdeal, Question3PostAll, and experiments     
>> twUserID	twTweetID	fbUserID	fbFeedID  urlOrderNum #twRT #twFavorite	#twComment #fbReshare #fbLikes #fbComment timeDifference  twitterName facebookName 
>> 19019298	7.14543E+17	37791069588	1.01541E+16	13	1	1	    0	        0	0	0	    -4	        IAmBiotech	IAmBiotech
>> 13877002	7.15385E+17	72139486384	1.01541E+16	1	2	4	    0	        1	7	2	    -583	clarionledger	clarionledger

> output: IdentifyCossPostTextRepeat # is used for Question1Overlap






## 3CossPostMerge

Merge  IdentifyCossPostText and IdentifyCossPostUrl into one file.

> input1: IdentifyCossPostText    
>> twUserID	twTweetID	fbUserID	fbFeedID  urlOrderNum #twRT #twFavorite	#twComment #fbReshare #fbLikes #fbComment timeDifference  twitterName facebookName 
>> 19019298	7.14543E+17	37791069588	1.01541E+16	13	1	1	    0	        0	0	0	    -4	        IAmBiotech	IAmBiotech
>> 13877002	7.15385E+17	72139486384	1.01541E+16	1	2	4	    0	        1	7	2	    -583	clarionledger	clarionledger

> input2: IdentifyCossPostUrl
>> twUserID	twTweetID	fbUserID	fbFeedID  urlOrderNum #twRT #twFavorite	#twComment #fbReshare #fbLikes #fbComment timeDifference  twitterName facebookName 
>> 19019298	7.14543E+17	37791069588	1.01541E+16	13	1	1	    0	        0	0	0	    -4	        IAmBiotech	IAmBiotech
>> 13877002	7.15385E+17	72139486384	1.01541E+16	1	2	4	    0	        1	7	2	    -583	clarionledger	clarionledger

> output: CossPostMerge      
>> twUserID	twTweetID	fbUserID	fbFeedID  urlOrderNum #twRT #twFavorite	#twComment #fbReshare #fbLikes #fbComment timeDifference  twitterName facebookName 
>> 19019298	7.14543E+17	37791069588	1.01541E+16	13	1	1	    0	        0	0	0	    -4	        IAmBiotech	IAmBiotech
>> 13877002	7.15385E+17	72139486384	1.01541E+16	1	2	4	    0	        1	7	2	    -583	clarionledger	clarionledger

