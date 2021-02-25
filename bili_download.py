import json
import os
import sys
from time import sleep

import bili_login
import requests
cho = input("是否重新登录？（1.登录  2.使用历史记录）：")
if cho == "1":
    sessdata = bili_login.login()
    with open("./pswd.conf", "w") as f:
        f.write(sessdata)
else:
    with open("./pswd.conf", "r") as f:
        sessdata = f.read()
bvid = input("请输入视频bvid号：")
info_url = "http://api.bilibili.com/x/web-interface/view?bvid=" + bvid
info_res = requests.get(info_url)
info = json.loads(info_res.text)
cid = info["data"]["cid"]

cho = int(input("请选择视频格式（1.mp4(首选，音视频分离，需二次合成)  2.flv(音视频一体，但可能存在限速)）："))
if cho == 1:
    res_url = "http://api.bilibili.com/x/player/playurl?bvid=" + bvid + "&cid=" + str(cid) + "&fnval=16&fourk=1"
else:
    res_url = "http://api.bilibili.com/x/player/playurl?bvid=" + bvid + "&cid=" + str(cid) + "&fnval=0&fourk=1"
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68",
    "cookie": "SESSDATA="+sessdata
}
res = requests.get(url=res_url, headers=header)
cont_dict = json.loads(res.text)
if cho == 1:
    try:
        d_url_v = cont_dict["data"]["dash"]["video"][0]["baseUrl"].replace("\u0026", "&")
        d_url_a = cont_dict["data"]["dash"]["audio"][0]["baseUrl"].replace("\u0026", "&")
    except:
        print("状态异常，可能登录信息失效或ip被暂时封禁，请重新登录或者稍后再试！")
        sleep(3)
        sys.exit()
    os.system('wget "' + d_url_v + '" --referer "https://www.bilibili.com" -O "Download_video.mp4"')
    os.system('wget "' + d_url_a + '" --referer "https://www.bilibili.com" -O "Download_audio.aac"')
else:
    try:
        d_url = cont_dict["data"]["durl"][0]["url"]
    except:
        print("状态异常，可能登录信息失效或ip被暂时封禁，请重新登录或者稍后再试！")
        sleep(3)
        sys.exit()
    os.system('wget "' + d_url + '" --referer "https://www.bilibili.com" -O "Download_video.flv"')
print("下载成功！")