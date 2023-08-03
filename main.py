# This is a sample Python script.
import json
from datetime import datetime
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# 导入urlopen函数
from urllib.request import urlopen, Request

import requests
# 导入BeautifulSoup
from bs4 import BeautifulSoup as bf, BeautifulSoup
from fake_useragent import UserAgent
import ssl

# 请求获取HTML
login_url = "https://knkmnd.zentaopm.com/user-login.html"
home_url = "https://knkmnd.zentaopm.com/bug-browse-4.html"
session_request=requests.session()
cookie = ''
headers1 = {
    "User-Agent":UserAgent().random,
    "cookie": cookie
}

wechat_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=146092d5-f6a0-4f8a-b5f5-7eb62e9a9368'

def init():
    headers = {
        "User-Agent": UserAgent().random,
    }
    result = session_request.post(
        login_url,
        data= {
            "account": "liujun",
            "password": "123456",
            "passwordStrength": 0,
            'referer': "/",
            'verifyRand': 1091524886,
            'keepLogin': 0,
        },
        headers=headers
    )
    headers1 = {
        "User-Agent": UserAgent().random,
        "cookie": result.cookies
    }
    mock_cookie = {
    "windowWidth" : '1282',
    "windowHeight" :"919",
    'zentaosid' : result.cookies['zentaosid'],
    "lang" : "zh-cn",
    "device" : "desktop",
    "theme" : 'default',
    "b-user-id" : 'b1a2d9c9-3aac-e2d1-17a5-1bab4a68b6f8',
    "feedbackView" : '0'
    }
    result1 = session_request.get(
        home_url,
        headers=headers,
        cookies=mock_cookie,
    )
    soup = BeautifulSoup(result1.text, 'html.parser')  # 这里一定要指定解析器，可以使用默认的 html，也可以使用 lxml。

    list = soup.select('tr')
    current_time = datetime.now()
    today_format = str(current_time.month).rjust(2,'0') + '-'+ str(current_time.day).rjust(2,'0')
    arr = []
    for tr in list:
        time = tr.select('td.c-openedDate')
        content = tr.select('td.c-title')
        assignTo = tr.select('td.c-assignedTo a span')
        if len(time) > 0 and len(content) > 0:
            record_time = time[0].get_text().split(' ')[0]
            if record_time == today_format:
                arr.append({
                    "title": content[0].get_text().split('\n')[0],
                    "assignTo": assignTo[0].get_text()
                })
    notice_wx(arr)


def notice_wx(arr):
    str1= "下面是今天的bug汇总：\n"
    send_weixin_text(str1)
    str2 = ''
    for index, value in enumerate(arr):
        str2 = str2 + str(index)+ '.' + "<font color=\"blue\">" + value['title'] + '(' + '<font color=\"green\">' + value['assignTo'] + '</font>' + ')'  +"</font>\n"
    send_weixin_markdown(str2)


def send_weixin_text(content):
    url = wechat_url # 这里就是群机器人的Webhook地址
    headers = {"Content-Type": "application/json"} # http数据头，类型为json
    data = {
        "msgtype": "text",
        "text": {
            "content": content, # 让群机器人发送的消息内容。
            "mentioned_list": ["@all"],
        }
    }
    r = requests.post(url, headers=headers, json=data) # 利用requests库发送post请求

def send_weixin_markdown(content):
    print('发消息')
    url = wechat_url # 这里就是群机器人的Webhook地址
    headers = {"Content-Type": "application/json"} # http数据头，类型为json
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": content, # 让群机器人发送的消息内容。
            "mentioned_list": ['郝韵臣',"@all"],
        }
    }
    r = requests.post(url, headers=headers, json=data) # 利用requests库发送post请求



if __name__ == '__main__':
   init()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
