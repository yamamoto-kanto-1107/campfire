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

    url = f'https://camp-fire.jp/projects/search?project_status=closed&page={company_start}'

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
    url_arr=[]

    page=1
    count = 0
    while page < 51:
        try:
            # 最新の `ol` 要素を取得
            container = driver.find_element(By.CLASS_NAME,'container')
            company_elements = container.find_element(By.TAG_NAME, 'ol')

            # `li` 要素を取得
            company_element_li = company_elements.find_elements(By.TAG_NAME, 'li')

            for i in range(len(company_element_li)):
                count +=1
                print(count)
                try:
                    # `card` 要素を取得しクリック
                    container = driver.find_element(By.CLASS_NAME,'container')
                    company_elements = container.find_element(By.TAG_NAME, 'ol')

                    # `li` 要素を取得
                    company_element_li = company_elements.find_elements(By.TAG_NAME, 'li')
                    company_element_btn = company_element_li[i].find_element(By.CLASS_NAME, 'card')
                    company_element_btn.click()

                    # 識別ボタンをクリック
                    try:
                        identify_btn = driver.find_element(By.ID,'gtm-sct-button')
                        identify_btn.click()
                    except:
                        driver.back()
                        continue

                    # 定義部分を取得
                    define =driver.find_element(By.CLASS_NAME,'definitions')
                    all = define.find_elements(By.CLASS_NAME, 'description')

                    if all[3].text ==  '無し' or all[3].text ==  '請求があり次第提供します。メッセージ機能にてご連絡ください。':
                        print('no phone')
                        close_btn = driver.find_element(By.CLASS_NAME,'close')
                        close_btn.click()
                        driver.back()
                        continue
                    else:
                        #電話番号の重複
                        if all[3].text in phone_arr:
                            print('double phone')
                            close_btn = driver.find_element(By.CLASS_NAME,'close')
                            close_btn.click()
                            driver.back()
                            continue
                        else:
                            phone_arr.append(all[3].text)

                    if all[0].text ==  '請求があり次第提供します。メッセージ機能にてご連絡ください。':
                        print('no company')
                        close_btn = driver.find_element(By.CLASS_NAME,'close')
                        close_btn.click()
                        driver.back()
                        continue
                    else:
                        print(all[0].text)
                        company_arr.append(all[0].text)

                    if all[2].text ==  '請求があり次第提供します。メッセージ機能にてご連絡ください。':
                        print('no address')
                        close_btn = driver.find_element(By.CLASS_NAME,'close')
                        close_btn.click()
                        driver.back()
                        continue
                    else:
                        address_arr.append(all[2].text)

                    if all[1].text ==  '請求があり次第提供します。メッセージ機能にてご連絡ください。':
                        print('no name')
                        close_btn = driver.find_element(By.CLASS_NAME,'close')
                        close_btn.click()
                        driver.back()
                        continue
                    else:
                        name_arr.append(all[1].text)

                    current_url = driver.current_url
                    url_arr.append(current_url)

                    driver.back()

                except Exception as e:
                    print(f"Error during interaction with item {e}")
                    driver.back()


        except Exception as e:
            print(f"Error retrieving DOM: {e}")

        try:
            if page == company_end and company_all != True:
                break

            print(page)
            page += 1
            next_project_btn = driver.find_element(By.CLASS_NAME,'next')
            next_project_btn.click()
        except:
            break

    print(f'name::{name_arr}')
    print(f'phone::{phone_arr}')
    print(f'address::{address_arr}')
    print(f'company::{company_arr}')

    insert_arr = zip(company_arr,name_arr,phone_arr,address_arr,url_arr)

    with open(f'{csv_pass}/output.csv','w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['会社名','代表者名','電話番号','住所','URL'])
        for row in insert_arr:
            writer.writerow(row)
