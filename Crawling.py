import os
from os import path

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import urllib.request

# 검색어 리스트 정의
searchKeys = [
    "이 부분에 검색할 사진 입력",
    "여러 개 가능"
]

for searchKey in searchKeys:
    driver = webdriver.Chrome()
    driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
    elem = driver.find_element("name", "q")

    elem.send_keys(Keys.CONTROL + "a")
    elem.send_keys(Keys.DELETE)
    elem.send_keys(searchKey)
    elem.send_keys(Keys.RETURN)

    SCROLL_PAUSE_TIME = 1
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()
            except:
                break
        last_height = new_height

    images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
    count = 1

    for image in images:
        try:
            image.click()
            time.sleep(0.5)
            imgUrl = driver.find_element(
                By.XPATH,
                '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]'
            ).get_attribute("src")
            opener = urllib.request.build_opener()
            opener.addheaders = [
                ('User-Agent',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')
            ]
            urllib.request.install_opener(opener)

            folder_path = f'./Images/{searchKey.replace(" ", "_")}'
            os.makedirs(folder_path, exist_ok=True)
            urllib.request.urlretrieve(imgUrl, f'{folder_path}/{str(count)}.jpg')
            count = count + 1
        except Exception as e:
            # print('e : ', str(e))
            pass

    print(f'총 {count} 장의 이미지가 다운로드 되었습니다.')

driver.close()
