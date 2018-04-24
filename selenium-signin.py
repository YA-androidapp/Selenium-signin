#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################
#                            #
#    ログインテスト 自動化   #
#                            #
##############################

# ファイル名設定用
import datetime
import os

# Seleniumのドライバ
from selenium import webdriver
# # Seleniumで要素の読み込みを待機するためのパッケージ類
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 定数
TEXT_NOT_MATCH = 'アカウントまたはパスワードが正しくありません。パスワードを忘れた場合は、今すぐリセットしてください。' # 認証失敗時に表示されるメッセージ
URL = 'https://example.net/signin' # ログインページのURL

MESSAGE_MATCH = '認証に成功しました　　　: '
MESSAGE_NOT_MATCH = '　　　認証に失敗しました: '

WAITING_TIME = 10000

# HTMLの属性値等
CLASS_RESULT = 'ResultMessage'
CLASS_SUBMIT = 'SubmitButton'
NAME_USERID = 'UserName'
NAME_USERPW = 'Password'

# 試行対象のユーザ・パスワードをそれぞれ対応付けて設定
user_ids = ['admin1', 'admin2']
user_pws = ['password1', 'password2']


# スクショ保存時のファイル名を生成
def get_filepath():
    now = datetime.datetime.now()
    filename = 'screen_{0:%Y%m%d%H%M%S}.png'.format(now)
    filepath = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), filename)
    return filepath


# Seleniumを起動して認証を試行
def challenges():
    # Firefoxを指定して起動
    fox = webdriver.Firefox()
    fox.set_window_size(1280, 720)
    fox.get(URL)

    # Wait
    WebDriverWait(fox, WAITING_TIME).until(
        EC.presence_of_element_located((By.CLASS_NAME, CLASS_SUBMIT)))
    fox.save_screenshot(get_filepath())

    found = False
    for user_id, user_pw in zip(user_ids, user_pws):
        found = challenge(fox, user_id, user_pw)

    if(found):
        print(MESSAGE_MATCH, user_id, user_pw)
    else:
        print(MESSAGE_NOT_MATCH, user_id, user_pw)

    # 終了時の後片付け
    fox.close()
    fox.quit()


def submit(fox, name):
    fox.find_element_by_class_name(name).click()


def clearAndSendKeys(fox, name, text):
    fox.find_element_by_name(name).clear()
    fox.find_element_by_name(name).send_keys(text)


def challenge(fox, user_id, user_pw):
    clearAndSendKeys(fox, NAME_USERID, user_id)
    clearAndSendKeys(fox, NAME_USERPW, user_pw)
    submit(fox, CLASS_SUBMIT)

    WebDriverWait(fox, WAITING_TIME).until(
        EC.presence_of_element_located((By.CLASS_NAME, CLASS_SUBMIT)))
    fox.save_screenshot(get_filepath())

    print(fox.find_element_by_class_name(CLASS_RESULT).text)

    if(fox.find_element_by_class_name(CLASS_RESULT).text == TEXT_NOT_MATCH):
        return False
    else:
        return True


def main():
    challenges()


if __name__ == '__main__':
    main()

# Copyright (c) 2018 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.
