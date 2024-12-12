from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

import time
import csv


def getDataToCampfire(mailaddress,password,csv_pass,company_count):
    url = 'https://camp-fire.jp/'
    wait_time = 5

    print(company_count)
    print(csv_pass)
    driver= webdriver.Chrome()
    driver.get(url)

    #ログインボタンのクリック
    login_btn = driver.find_element(By.ID, 'gtm-hnav-link-to-login')
    login_btn.click()

    #メールアドレスの挿入
    mail_input = driver.find_element(By.CLASS_NAME,'form-control')
    mail_input.send_keys(mailaddress)

    #次へボタンをクリック
    next_btn = driver.find_element(By.NAME,'commit')
    next_btn.click()

    #パスワードを入力
    pass_input = driver.find_element(By.ID,'user_password')
    pass_input.send_keys(password)

    #ログインボタンをクリック
    login_btn2 = driver.find_element(By.NAME,'commit')
    login_btn2.click()

    #プロジェクトを探す
    search_project_btn = driver.find_element(By.ID,'gtm-hnav-link-to-projects-pc')
    search_project_btn.click()


    #企業の名前を取得する
    company_names = []
    page = 1
    count = 0
    while True:
        company_elements = driver.find_element(By.TAG_NAME,'ol')
        company_element_li = company_elements.find_elements(By.TAG_NAME,'li')

        for li in company_element_li:
            company_element_text = li.find_elements(By.CLASS_NAME,'text')
            company_names.append(company_element_text[1].text)

            count +=1
            print(count)
            if count == company_count:
                print('call?')
                break

        if count == company_count:
            print('call?')
            break

        print(f'call{page}')
        try:
            page += 1
            next_project_btn = driver.find_element(By.CLASS_NAME,'next')
            next_project_btn.click()
        except:
            break

    print('call3')
    with open(f'{csv_pass}/output.csv','w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['会社名'])
        for company_name in company_names:
            writer.writerow([company_name])


    time.sleep(wait_time)
