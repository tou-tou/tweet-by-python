# -*- coding:utf-8 -*-
import json, config
from requests_oauthlib import OAuth1Session
import random

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

url = "https://api.twitter.com/1.1/statuses/update.json"


f = open("com_structure.txt",encoding = "utf-8")
tweetlist = f.readlines()
i = random.randint(0,len(tweetlist)-1)
f.close()

tweet=tweetlist[i] #投稿するツイート
params = {"status" : tweet}

req = twitter.post(url, params = params) #投稿

#if req.status_code == 200:
#   print("Succeed!")
#else:
#   print("ERROR : %d"% req.status_code)

