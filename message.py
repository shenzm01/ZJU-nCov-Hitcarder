import requests
import json
import os
import time
import smtplib
from email.mime.text import MIMEText
import datetime


def dingtalk(msg, dingtalk_token, tries=5):
    dingtalk_url = 'https://oapi.dingtalk.com/robot/send?access_token='+dingtalk_token
    now = datetime.datetime.now()
    msg = str(now.year) + "." + str(now.month) + "." + str(now.day) + ": " + msg
    data = {
        "msgtype": "text",
        "text": {
            "content": msg
        },
        "at": {
            "isAtAll": False
        }
    }
    header = {'Content-Type': 'application/json'}

    for _ in range(tries):
        try:
            r = requests.post(dingtalk_url,
                              data=json.dumps(data), headers=header).json()
            print(r)
            if r["errcode"] == 0:
                return True
        except:
            pass
        print('Retrying...')
        time.sleep(5)
    return False


def serverchan(text, desp, serverchan_key, tries=5):
    text, desp = text[:100], desp[:100]
    text = 'Server酱服务即将下线，请切换到其他通知通道（建议使用钉钉）\n' + text
    for _ in range(tries):
        try:
            r = requests.get("https://sc.ftqq.com/" + serverchan_key
                             + ".send?text=" + text + "&desp=" + desp).json()
            print(r)
            if r["errno"] == 0:
                return True
        except:
            pass
        print('Retrying...')
        time.sleep(5)
    return False

def sendmail(title, content, mail_host, mail_user, mail_pass, sender, receivers):
    #邮件内容设置
    message = MIMEText(content ,'plain','utf-8')
    #邮件主题       
    message['Subject'] = title 
    #发送方信息
    message['From'] = sender 
    #接受方信息     
    message['To'] = receivers[0]  
    #登录并发送邮件
    try:
        smtpObj = smtplib.SMTP() 
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_user, mail_pass) 
        #发送
        smtpObj.sendmail(sender, receivers, message.as_string()) 
        #退出
        smtpObj.quit() 
    except smtplib.SMTPException as e:
        print('error',e) #打印错误

if __name__ == "__main__":
    msg = "打卡"*1000
    dingtalk_token = os.environ.get('DINGTALK_TOKEN')
    if dingtalk_token:
        ret = dingtalk(msg, dingtalk_token)
        print('send_dingtalk_message', ret)

    serverchan_key = os.environ.get('SERVERCHAN_KEY')
    if serverchan_key:
        ret = serverchan(msg, '', serverchan_key)
        print('send_serverChan_message', ret)
