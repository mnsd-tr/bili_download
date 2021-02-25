import json
import os
import sys
import webbrowser
from time import sleep

import requests


def login():
    req_url = "http://passport.bilibili.com/qrcode/getLoginUrl"
    res = requests.get(req_url)
    cont = json.loads(res.text)

    reg_url = cont["data"]["url"]
    oauthKey = cont["data"]["oauthKey"]

    html_cont = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script type='text/javascript' src='http://cdn.staticfile.org/jquery/2.1.1/jquery.min.js'></script>
<script type="text/javascript" src="http://cdn.staticfile.org/jquery.qrcode/1.0/jquery.qrcode.min.js"></script>
<title>Bilibili_login</title>
</head>
<body>
<div id="qrcode"></div>
</body>
<script>
jQuery('#qrcode').qrcode({width: 150,height: 150,text: "''' + reg_url + '''"});
</script>
</html>
    '''

    with open("./scan.html", "w", encoding="utf-8") as f:
        f.write(html_cont)
    webbrowser.open('file://' + os.path.realpath("./scan.html"))
    input("请打开bilibili客户端扫码登录，登录信息一周内有效，信息保存至本地，无安全问题，请放心扫码确认后按回车键继续：")
    post_url = "http://passport.bilibili.com/qrcode/getLoginInfo"
    post_data = {"oauthKey": oauthKey}
    res = requests.post(post_url, post_data)
    res = json.loads(res.text)
    try:
        sessdata = res["data"]["url"].split("&")[-3].split("=")[1]
    except:
        print("登录异常，请重新操作！")
        sleep(3)
        sys.exit()
    os.remove("./scan.html")
    return sessdata

