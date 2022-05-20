# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By

import smtplib
from email.mime.text import MIMEText
from email.header import Header

url1 = 'http://ehall.seu.edu.cn/gsapp/sys/wddbsqappseu/*default/index.do?t_s=1652969354823&amp_sec_version_=1&gid_=T1ljeGQwY3J6OEhKSWd3RWZHcjQ5b1JmQ3dvRVMxdHd5aTd3ak9BL1lrQUVJYm5MRGwwUTVJaTFwOHFhcmZ6T21KMVZQc2tzbldOY0ZFWVVzV2tmclE9PQ&EMAP_LANG=zh&THEME=indigo#/xsbdjcsq'
url = "http://ehall.seu.edu.cn/gsapp/sys/wddbsqappseu/modules/xsbdjcsq/lwssjgcx.do"

#设置服务器
mail_host="smtp.163.com"
mail_user="***@163.com"
# 163授权码
mail_pass="***"

def login(user, pw, browser):
    browser.get(url1)
    browser.implicitly_wait(10)

    # 填写用户名密码
    username = browser.find_element(By.ID, 'username')
    password = browser.find_element(By.ID, 'password')
    username.clear()
    password.clear()
    username.send_keys(user)
    password.send_keys(pw)

    # 点击登录
    login_button = browser.find_element(by=By.CLASS_NAME, value='auth_login_btn')
    login_button.submit()

def mail(msg):
    sender = '***@163.com'
    receivers = ['***@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = Header("XR", 'utf-8')
    message['To'] = Header("XR", 'utf-8')

    subject = '信息更改'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        # smtpObj = smtplib.SMTP()
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        # smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(repr(e))
        print("Error: 无法发送邮件")

if __name__ == "__main__":

    user = ''
    # 密码
    pw = ''

    option = webdriver.ChromeOptions()
    # 隐藏浏览器
    option.add_argument('headless')

    s = Service("chromedriver.exe")
    browser = webdriver.Chrome(service=s, options=option)
    print("------------------浏览器已启动----------------------")
    login(user, pw, browser)
    browser.implicitly_wait(10)
    time.sleep(1)

    browser.get(url)
    browser.implicitly_wait(10)
    content_str = browser.page_source
    l = content_str.split(',')
    hash_code = ''
    ZJID = []
    CJ = []
    SCHOOL = []
    for ele in l:
        if ele[0:5] == '"ZJID':
            print(ele[7:11])
            ZJID.append(ele[7:11])
        elif ele[0:4] == '"CJ"':
            print(ele[5:11])
            CJ.append(ele[5:11])
        elif ele[0:7] == '"SSDWMC':
            print(ele[10:-1] + ':')
            SCHOOL.append(ele[10:-1])
    browser.quit()

    for i in range(0, 2):
        hash_code += SCHOOL[i]
        hash_code += ':'
        hash_code += ZJID[i]
        hash_code += ','
        hash_code += CJ[i]
        hash_code += '\n'

    print(hash_code)

    # 如果信息改变，发送邮件通知用户
    f = open("msg.txt", 'r', encoding="utf-8")
    stri = str(f.read())
    # print(stri)
    # print('read over')
    if hash_code != stri:
        print("Content changed!")
        f.close()
        f = open("msg.txt", 'w+', encoding="utf-8")
        mail(hash_code)
        f.write(hash_code)

    f.close()
