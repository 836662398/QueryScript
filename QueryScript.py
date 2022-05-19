from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import time

from selenium.webdriver.common.by import By

url1 = 'http://ehall.seu.edu.cn/gsapp/sys/wddbsqappseu/*default/index.do?t_s=1652969354823&amp_sec_version_=1&gid_=T1ljeGQwY3J6OEhKSWd3RWZHcjQ5b1JmQ3dvRVMxdHd5aTd3ak9BL1lrQUVJYm5MRGwwUTVJaTFwOHFhcmZ6T21KMVZQc2tzbldOY0ZFWVVzV2tmclE9PQ&EMAP_LANG=zh&THEME=indigo#/xsbdjcsq'
url = "http://ehall.seu.edu.cn/gsapp/sys/wddbsqappseu/modules/xsbdjcsq/lwssjgcx.do"


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

if __name__ == "__main__":

    user = '220191671'
    # 密码
    pw = ''
    s = Service("chromedriver.exe")
    browser = webdriver.Chrome(service=s)
    print("------------------浏览器已启动----------------------")
    login(user, pw, browser)
    browser.implicitly_wait(10)
    time.sleep(1)

    browser.get(url)
    browser.implicitly_wait(10)
    content_str = browser.page_source
    l = content_str.split(',')
    for ele in l:
        if ele[0:5] == '"ZJID':
            print(ele[7:11])
        elif ele[0:4] == '"CJ"':
            print(ele[5:11])
        elif ele[0:7] == '"SSDWMC':
            print(ele[10:-1] + ':')
    browser.quit()