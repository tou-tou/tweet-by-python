# -*- coding:utf-8 -*-
import json, configparser
from requests_oauthlib import OAuth1Session
import random
from PIL import Image
import os
import datetime

# --------------------------------------------------
# configparserの宣言とiniファイルの読み込み
# --------------------------------------------------
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

CK = config_ini.get('DEFAULT', 'CK')
CS = config_ini.get('DEFAULT', 'CS')
AT = config_ini.get('DEFAULT', 'AT')
AS = config_ini.get('DEFAULT', 'AS')
twitter = OAuth1Session(CK, CS, AT, AS)


url_media = "https://upload.twitter.com/1.1/media/upload.json?media_category=tweet_image"
url_text = "https://api.twitter.com/1.1/statuses/update.json"


# select image paths
# 最新の日付フォルダ3日分からランダムに4つのパスを選択
# vrchat配下のフォルダ名を降順で並べて、3日以内のフォルダ内の画像からランダムで4つ選ぶ、なければスキップ
path = "Pictures/VRChat"
files = os.listdir(path)
dirs = [f for f in files if os.path.isdir(os.path.join(path, f))]
dates_list = sorted(dirs,reverse=True)

# now = datetime.datetime.now()
# three_ago = now - datetime.timedelta(days=3)
# three_ago_str = three_ago.strftime('%Y-%m-%d')

three_dirs = dates_list[0:3]
selected_image_paths = []

for d in three_dirs:
    image_path = path + '/' + d 
    image_file = os.listdir(image_path)


media_ids = []
# dataに画像
for i in range(4):
    # 画像データの読み込み
    with open(selected_image_paths[i],"rb") as image_file:
        image_data=image_file.read() 

    files = {"media" : image_data}
    req_media = twitter.post(url_media, files = files)

    # レスポンス
    if req_media.status_code != 200:
        print ("画像アップロード失敗: %s", req_media.text)
        exit()

    # media_id を取得
    media_id = json.loads(req_media.text)['media_id']
    media_ids.append(media_id)

# 投稿した画像をツイートに添付したい場合は取得したmedia_idを"media_ids"で指定してツイートを投稿
message = '最近の！ (bot テスト)'
media_ids_string=','.join(map(str,media_ids))
params = {'status': message, "media_ids": media_ids_string}
req_media = twitter.post(url_text, params = params)


# if req.status_code == 200:
#   print("Succeed!")
# else:
#   print("ERROR : %d"% req.status_code)

