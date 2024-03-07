import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

import re
import pandas as pd
import datetime
import os

def crawling_naver(url):
    
    options = Options()
    options.add_argument("--headless")  # 헤드리스 모드 활성화
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--window-size=1920x1080')

    #user-agent 추가
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    options.add_argument("user-agent="+user_agent)

    now = datetime.datetime.now()    
    formatted_now = now.strftime("%Y-%m-%d %H:%M")

    URL = url
    browser = webdriver.Chrome(options=options)
    browser.get(URL)
    time.sleep(1)
    browser.maximize_window()
    time.sleep(1)


    # 방콕 고르기

    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[4]/div/div/div[2]/div[1]/button[2]'))).click()
    time.sleep(0.5)
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[10]/div[2]/section/section/button[3]'))).click()
    time.sleep(0.5)
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[10]/div[2]/section/section/div/button[1]'))).click()
    time.sleep(0.5)
    
    # 날짜 고르기
    # 가는 날 버튼 -> 캘린더 열기
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[4]/div/div/div[2]/div[2]/button[1]'))).click()
    time.sleep(3)
    
    # 가는 날 선택
    # browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[10]/div[2]/div[1]/div[2]/div/div[2]/table/tbody/tr[4]/td[6]/button').click()
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[10]/div[2]/div[1]/div[2]/div/div[2]/table/tbody/tr[4]/td[6]/button'))).click()
    time.sleep(3)
    
    # 오는 날 선택
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[10]/div[2]/div[1]/div[2]/div/div[2]/table/tbody/tr[4]/td[7]/button'))).click()                         
    time.sleep(3)
    
    # 직항 선택
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[4]/div/div/div[2]/div[3]/button[2]'))).click()
    time.sleep(0.5)

    # 편도 선택
    WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[4]/div/div/div[1]/button[2]'))).click()
    time.sleep(0.5)
    
    # 항공권 검색
    WebDriverWait(browser, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[4]/div/div/div[2]/button'))).click()
    time.sleep(7)
    
    # 카드 혜택 제외하기
    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[7]/div/div[1]/div/div[2]/button'))).click()
    time.sleep(0.5)
    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[7]/div/div[1]/div/div[2]/div/button[2]/span'))).click()

    while True:
        # 현재 스크롤 위치
        current_scroll_position = browser.execute_script("return window.scrollY;")
        
        # 스크롤을 화면의 맨 아래로 이동
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # 잠시 대기 (동적으로 콘텐츠가 로딩되는 시간을 고려)
        time.sleep(3)
        
        # 새로운 스크롤 위치
        new_scroll_position = browser.execute_script("return window.scrollY;")
        
        # 새로운 스크롤 위치와 이전 스크롤 위치가 같다면 끝까지 스크롤 완료
        if new_scroll_position == current_scroll_position:
            break

            
    # 긁어 오기

    airline = [] # 항공사 이름
    take_off = [] # 이륙 시간
    landing = [] # 착륙 시간
    take_off_airport = [] # 출발 공항
    landing_airport = [] # 도착 공항
    non_stop_transit = [] # 직항 or 경유
    ftime = [] # 항공시간
    one_way_round = [] # 편도 or 왕복
    ticket_price = [] # 티켓 가격

    html=browser.page_source
    soup=BeautifulSoup(html,'html.parser')


    # 항공사 이름
    air_names=soup.select('b.airline_name__Tm2wJ')
    # 이륙 시간, 착륙 시간
    flights_check=soup.select('b.route_time__-2Z1T')
    # 출발 공항, 도착 공항
    flights_place=soup.select('i.route_code__3WUFO')
    # 직항, 걸리는 시간
    flights_times = soup.select('i.route_info__1RhUH')
    # 편도, 가격
    money = soup.select('b.item_usual__dZqAN')

    for i in range(len(air_names)):
        airline.append(air_names[i].get_text())
        time.sleep(0.3)

    for i in range(len(flights_check)):
        if i % 2 == 0:
            take_off.append(flights_check[i].get_text())
        else : 
            landing.append(flights_check[i].get_text())    
        time.sleep(0.3)

    for i in range(len(flights_place)):
        if i % 2 == 0:
            take_off_airport.append(flights_place[i].get_text())
        else : 
            landing_airport.append(flights_place[i].get_text())
        time.sleep(0.3)

    for i in range(len(flights_times)):
        way_n_time = re.split(', ', flights_times[i].get_text())
        non_stop_transit.append(way_n_time[0])
        ftime.append(way_n_time[1])
        time.sleep(0.3)

    for i in range(len(money)):
        money_info = re.split(' ', money[i].get_text())
        one_way_round.append(money_info[0])
        ticket_price.append(money_info[1][:-1])
        time.sleep(0.3)


    data = { "항공사" : airline,
            "이륙 시간" : take_off,
            "출발 공항" : take_off_airport,
            "착륙 시간" : landing,
            "도착 공항" : landing_airport,
            "직항, 경유" : non_stop_transit,
            "항공 시간" : ftime,
            "편도, 왕복" : one_way_round,
            "티켓 가격" : ticket_price,
            "크롤링 시작" : formatted_now
            }

    time.sleep(1)

    browser.close()

    return data


def main():

    url = "https://flight.naver.com"

    df = pd.DataFrame(crawling_naver(url))

    if not os.path.exists("/app/data"):
        df.to_csv("/app/data/naver_bangkok_26.csv", index=False, mode = "w", encoding="utf-8")    
    else :
        df.to_csv("/app/data/naver_bangkok_26.csv", index=False, mode = "a", encoding="utf-8", header=False)

if __name__ == "__main__":
    main()