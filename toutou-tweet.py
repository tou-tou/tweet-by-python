# -*- coding:utf-8 -*-
import json, configparser
from requests_oauthlib import OAuth1Session
import random
from PIL import Image
import os
import datetime
import sys
import glob
import re
import pathlib

# config.iniの読み込み
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

CK = config_ini.get('DEFAULT', 'CK')
CS = config_ini.get('DEFAULT', 'CS')
AT = config_ini.get('DEFAULT', 'AT')
AS = config_ini.get('DEFAULT', 'AS')
twitter = OAuth1Session(CK, CS, AT, AS)

url_media = "https://upload.twitter.com/1.1/media/upload.json?media_category=tweet_image"
url_text = "https://api.twitter.com/1.1/statuses/update.json"
path = "E:\\Pictures\\VRChat"

files = os.listdir(path)
dirs = [f for f in files if os.path.isdir(os.path.join(path, f))]
dates_list = sorted(dirs,reverse=True)

def isMonth(dirname):
    """
    フォルダの名前が月で終わっている
    ex;2021-12
    """
    if dirname.count('-') == 1 :
        return True
    else:
        return False
        
def isWeekEnd(now):
    day = now.strftime('%A')
    if day in ['Friday','Saturday','Sunday']:
        return True
    return False

def isRecentLogin(now,lastDate):
    someday_ago = now - datetime.timedelta(days=7)
    someday_ago_str = someday_ago.strftime('%Y-%m-%d')
    if lastDate <= someday_ago_str:
        return False
    return True

def getLatestGetPicDate():
    monthDirs = [f for f in files if os.path.isdir(os.path.join(path, f)) and isMonth(f)]
    months_list = sorted(monthDirs,reverse=True)
    recentImageFiles = glob.glob(path + '\\' + months_list[0] + '\\*\\' + '*.png')
    recentImageList = sorted(recentImageFiles,reverse=True)
    latestImagePath = recentImageList[0]
    fileinfo = pathlib.Path(latestImagePath)
    dt = datetime.datetime.fromtimestamp(fileinfo.stat().st_ctime)
    return dt.strftime('%Y-%m-%d')


PICCOUNT = 50
# 最近のPICCOUNT枚以下の写真を選ぶ
def getRecentPics():
    monthDirs = [f for f in files if os.path.isdir(os.path.join(path, f)) and isMonth(f)]
    months_list = sorted(monthDirs,reverse=True)
    recentImageFiles = glob.glob(path + '\\' + months_list[0] + '\\*\\' + '*.png') + glob.glob(path + '\\' + months_list[1] + '\\*\\' + '*.png')
    recentImageFiles = sorted(recentImageFiles,reverse=True)
    l = len(recentImageFiles)  if len(recentImageFiles) < PICCOUNT  else PICCOUNT
    return recentImageFiles[0:l]


# ランダムに4つ画像pathを選ぶ
selected_image_paths = random.sample(getRecentPics(),4)


# 7日間VRChatに入ってなかったら投稿しない、金土日以外は投稿しない
now = datetime.datetime.now()
if (not isRecentLogin(now , getLatestGetPicDate())) or (not isWeekEnd(now)):
    sys.exit()


# TWEETDAY日間分の写真から選ぶ
TWEETDAY = 2


media_ids = []
for i in range(4):
    with open(selected_image_paths[i],"rb") as image_file:
        image_data=image_file.read() 

    files = {"media" : image_data}
    req_media = twitter.post(url_media, files = files)
    media_id = json.loads(req_media.text)['media_id']
    media_ids.append(media_id)

message = '最近の！'
media_ids_string=','.join(map(str,media_ids))
params = {'status': message, "media_ids": media_ids_string}
req_media = twitter.post(url_text, params = params)


