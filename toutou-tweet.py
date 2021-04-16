# -*- coding:utf-8 -*-
import json, configparser
from requests_oauthlib import OAuth1Session
import random
from PIL import Image
import os
import datetime
import sys

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

# 3日間VRChatに入ってなかったら投稿しない
now = datetime.datetime.now()
someday_ago = now - datetime.timedelta(days=3)
someday_ago_str = someday_ago.strftime('%Y-%m-%d')
some_dirs = dates_list[0:3]
if dates_list[0] < someday_ago_str:
    sys.exit()

image_paths = []
selected_image_paths = []
for d in some_dirs:
    image_dir_path = path + '\\' + d 
    image_files = os.listdir(image_dir_path)
    for file_name in image_files:
        selected_image_paths.append(image_dir_path + '\\' + file_name)

selected_image_paths = random.sample(selected_image_paths,4)

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


