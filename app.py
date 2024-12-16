from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

import time
import csv


def getDataToCampfire(csv_pass,company_start = None,company_end=None,company_all = None):
    if company_start == None:
        company_start= 1

    url = f'https://camp-fire.jp/projects/search?page={company_start}'
    # url = f'https://camp-fire.jp/projects/search?page=1'

    driver= webdriver.Chrome()
    driver.get(url)
    driver.set_page_load_timeout(240)
    driver.set_script_timeout(120)
    driver.implicitly_wait(30)

    #データを取得する
    company_arr=[]
    address_arr=[]
    phone_arr=[]
    name_arr=[]

    # company_elements = driver.find_element(By.TAG_NAME,'ol')
    # company_element_li = company_elements.find_elements(By.TAG_NAME,'li')

    # company_element_btn =company_element_li[0].find_elements(By.CLASS_NAME,'card')
    # company_element_btn[0].click()
    # identify_btn = driver.find_element(By.CLASS_NAME,'sct-button')
    # identify_btn.click()
    # define = driver.find_element(By.CLASS_NAME,'definitions')
    # company = define.find_elements(By.CLASS_NAME,'description')
    # company_arr.append(company[0].text)
    # print(company_arr)
    # page = company_start
    company_end = 1
    page=1
    while True:
        try:
            # 最新の `ol` 要素を取得
            company_elements = driver.find_element(By.TAG_NAME, 'ol')

            # `li` 要素を取得
            company_element_li = company_elements.find_elements(By.TAG_NAME, 'li')
            total_items = len(company_element_li)

            for i in range(total_items):
                print(f'{i}個目')
                try:
                    # 最新の `li` 要素を再取得
                    company_elements = driver.find_element(By.TAG_NAME, 'ol')
                    company_element_li = company_elements.find_elements(By.TAG_NAME, 'li')

                    # `i` 番目の `li` 要素を取得
                    li = company_element_li[i]

                    # `card` 要素を取得しクリック
                    company_element_btn = li.find_element(By.CLASS_NAME, 'card')
                    company_element_btn.click()

                    # 識別ボタンをクリック
                    identify_btn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.ID, 'gtm-sct-button'))
                    )
                    identify_btn.click()

                    # 定義部分を取得
                    define = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'definitions'))
                    )
                    all = define.find_elements(By.CLASS_NAME, 'description')
                    if all[0].text ==  '請求があり次第提供します。メッセージ機能にてご連絡ください。':
                        continue
                    else:
                        company_arr.append(all[0].text)

                    if all[2].text ==  '請求があり次第提供します。メッセージ機能にてご連絡ください。':
                        continue
                    else:
                        address_arr.append(all[2].text)

                    if all[3].text ==  '無し':
                        continue
                    else:
                        phone_arr.append(all[3].text)

                    if all[1].text ==  '請求があり次第提供します。メッセージ機能にてご連絡ください。':
                        continue
                    else:
                        name_arr.append(all[1].text)

                    close_btn = driver.find_element(By.CLASS_NAME,'close')
                    close_btn.click()
                    driver.back()

                except Exception as e:
                    print(f"Error during interaction with item {i}: {e}")
        except Exception as e:
            print(f"Error retrieving DOM: {e}")



        print(f'name::{name_arr}')
        print(f'phone::{phone_arr}')
        print(f'address::{address_arr}')
        print(f'company::{company_arr}')

        try:
            if page == company_end and company_all != True:
                break

            page += 1
            next_project_btn = driver.find_element(By.CLASS_NAME,'next')
            next_project_btn.click()
        except:
            break

    insert_arr = zip(company_arr,name_arr,phone_arr,address_arr)

    with open(f'{csv_pass}/output.csv','w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['会社名','代表者名','電話番号','住所'])
        for row in insert_arr:
            writer.writerow(row)

