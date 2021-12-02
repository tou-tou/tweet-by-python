import os
import datetime
import sys
import pathlib
import shutil

path = "E:\\Pictures\\VRChat"
firstfiles = os.listdir(path)

def isMonth(dirname):
    """
    フォルダの名前が月で終わっている
    ex;2021-12
    """
    if dirname.count('-') == 1 :
        return True
    else:
        return False

def isNowMonth(dirname):
    """
    フォルダの名前が現在の月で終わっている
    ex;2021-12
    """
    today = datetime.date.today()
    if dirname == str(today.year) + '-' + str(today.day):
        return True
    else:
        False

# 月別フォルダを探す
dirs = [f for f in firstfiles if os.path.isdir(os.path.join(path, f)) and isMonth(f)]

# 月別フォルダの下に日付フォルダをつくる
for dirname in dirs:
    monthpath = path + '\\' + dirname
    files = os.listdir(monthpath)
    imagefiles = [f for f in files if os.path.isfile(os.path.join(path, f))]
    for imageFileName in imagefiles:
        currentFilePath = monthpath + '\\' + imageFileName

        fileinfo = pathlib.Path(currentFilePath)
        dt = datetime.datetime.fromtimestamp(fileinfo.stat().st_ctime)
        destDir = monthpath + '\\' + dt.strftime('%Y-%m-%d')
        destFilePath = destDir + '\\' + imageFileName
        #日付フォルダがなければ、写真が作成された日付でフォルダを作成
        if not os.path.isdir(destDir):
            os.mkdir(destDir)
        #移動先に同名ファイルがなければ移動
        if not os.path.isfile(destFilePath) :
            shutil.move(currentFilePath,destDir)

