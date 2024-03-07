from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import pandas as pd 
from tqdm.notebook import tqdm
from urllib.request import urlopen, Request
from user_agent import generate_user_agent
import re
from bs4 import BeautifulSoup
import os
import datetime

class sleeping_timer:
    def __init__(self,time_set):
        self.time_set = 1
    
    def timer_sleep_by(self):
        time.sleep(self.time_set)


def get_osaka_data():

    timer_sleep = sleeping_timer(0.1)
    
    options = Options()
    options.add_argument("--headless")  # 헤드리스 모드 활성화
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--window-size=1920x1080')

    #user-agent 추가
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    options.add_argument("user-agent="+user_agent)
    
    url = "https://www.google.com/travel/flights?hl=ko&gl=kr&authuser"

    driver = webdriver.Chrome(options=options)
    
    driver.get(url)
    driver.implicitly_wait(5)
    time.sleep(2)
    driver.maximize_window()
    driver.implicitly_wait(5)
    time.sleep(2)

    #도착지 칸 클릭
    arrival_text = driver.find_elements(By.CLASS_NAME, "II2One.j0Ppje.zmMKJ.LbIaRd")
    arrival_text[2].click()
    driver.implicitly_wait(5)
    time.sleep(3)

    #도착지 칸에서 오사카 KIX 입력 
    arrival_text_input = driver.find_elements(By.XPATH, """//*[@id="i21"]/div[6]/div[2]/div[2]/div[1]/div/input""")
    arrival_text_input[0].send_keys("KIX")
    driver.implicitly_wait(5)
    arrival_text_input[0].send_keys(Keys.ENTER)
    time.sleep(3)

    #편도 리스트 다운 선택하기 
    one_way = driver.find_elements(By.CLASS_NAME, "VfPpkd-TkwUic")
    driver.implicitly_wait(5)
    one_way[0].click()
    timer_sleep.timer_sleep_by()

    #편도 클릭
    one_way_click = driver.find_elements(By.CLASS_NAME, "MCs1Pd.UbEQCe.VfPpkd-OkbHre.VfPpkd-OkbHre-SfQLQb-M1Soyc-bN97Pc.VfPpkd-aJasdd-RWgCYc-wQNmvb.ib1Udf.VfPpkd-rymPhb-ibnC6b.VfPpkd-rymPhb-ibnC6b-OWXEXe-SfQLQb-M1Soyc-Bz112c.VfPpkd-rymPhb-ibnC6b-OWXEXe-SfQLQb-Woal0c-RWgCYc")
    driver.implicitly_wait(5)
    one_way_click[1].click()
    timer_sleep.timer_sleep_by()
    
    #날짜 선택 ui 클릭
    date_ui = driver.find_elements(By.CLASS_NAME, "TP4Lpb.eoY5cb.j0Ppje")
    driver.implicitly_wait(5)
    date_ui[0].click()
    time.sleep(4)

    #날짜 선택 ui 다시클릭(포커스 다시 주기)
    date_ui_inside = driver.find_elements(By.CLASS_NAME, "NA5Egc.ESCxub.cd29Sd.wg2eAc")
    date_ui_inside[1].click()
    timer_sleep.timer_sleep_by()


    #날짜 선택 입력 클릭
    date_ui_inside = date_ui_inside[1].find_element(By.TAG_NAME, "input")
    date_ui_inside.send_keys("20240126")
    driver.implicitly_wait(5)
    date_ui_inside.send_keys(Keys.ENTER)
    time.sleep(3)

    #확인 버튼 클릭하기
    confirm_button = driver.find_elements(By.CLASS_NAME, "WXaAwc")
    driver.implicitly_wait(5)
    confirm_button = confirm_button[0].find_element(By.CLASS_NAME, "VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.z18xM.rtW97.Q74FEc.dAwNDc")
    driver.implicitly_wait(5)
    confirm_button.click()
    time.sleep(3)
    
    #검색 버튼 클릭하기 
    search_button = driver.find_elements(By.CLASS_NAME, "xFFcie")
    driver.implicitly_wait(5)
    search_button = search_button[0].find_element(By.CLASS_NAME, "VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc.nCP5yc.AjY5Oe.LQeN7.TUT4y.zlyfOd")
    search_button.click()
    time.sleep(5)
    
    #직항 선택 다운 리스트 선택하기
    driver.implicitly_wait(5)
    direct_flight = driver.find_elements(By.XPATH, """//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[4]/div/div/div[2]/div[1]/div/div[1]/span/button[1]""")
    direct_flight[0].click()
    timer_sleep.timer_sleep_by()

    #직항 라디오 버튼 선택하기 
    driver.implicitly_wait(5)
    direct_flight_chose = driver.find_elements(By.CLASS_NAME, "VfPpkd-GCYh9b.VfPpkd-GCYh9b-OWXEXe-dgl2Hf.kDzhGf.ZCYEwf.wHsUjf")
    driver.implicitly_wait(5)
    direct_flight_chose[1].click()
    time.sleep(5)

    #직항 선택창 닫기 
    direct_list_down_close = driver.find_elements(By.CLASS_NAME, "VfPpkd-Bz112c-LgbsSe.yHy1rc.eT1oJ.mN1ivc.evEd9e.HJuSVb")
    driver.implicitly_wait(5)
    direct_list_down_close[0].click()
    timer_sleep.timer_sleep_by()

    #팝업창 종료  
    pop_up_info = driver.find_elements(By.CLASS_NAME, "oNbB0")
    driver.implicitly_wait(5)
    timer_sleep.timer_sleep_by()

    if len(pop_up_info) != 0:
        pop_up_info = pop_up_info[0].find_elements(By.TAG_NAME, "div")
        driver.implicitly_wait(5)
        click_pop_up_close = pop_up_info[4]
        # pop_up_info.click()
        click_pop_up_close.click()
    
    timer_sleep.timer_sleep_by()


    #정렬 기준 선택하기 
    sorting_standard = driver.find_element(By.CLASS_NAME, "VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-Bz112c-UbuQg.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.ksBjEc.lKxP2d.LQeN7.zZJEBe")
    driver.implicitly_wait(5)
    sorting_standard.click()
    timer_sleep.timer_sleep_by()

    #정렬 기준으로 요금 선택하기 
    sorting_by_price = driver.find_elements(By.CLASS_NAME, "VfPpkd-StrnGf-rymPhb-ibnC6b")
    driver.implicitly_wait(5)
    sorting_by_price[1].click()
    time.sleep(5)

    #항공편 정보 가져오기 - Beatiful soup
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    take_off_list=[]
    time_data_list =[]
    landing_list =[]
    airline_list =[]
    airport_take_off_list = []
    ftime_list = []
    airport_landing_list = []
    non_stop_transit_list =[]
    one_way_round_list =[]
    flight_number_list = []
    ticket_price_list =[]


    #항공 출발 시간 가져오기 
    tmp_take_off_list = soup.find_all(class_= "wtdjmc YMlIz ogfYpf tPgKwe")

    #출발 시간 parsing
    for value in tmp_take_off_list:

        tmp_value = value.get_text()

        #오전,오후 찾기
        str_mon_night = re.search("[가-힣]+", tmp_value).group()

        #시간 찾기
        take_off_airport_hour = re.search("\d+(\d+)?:", tmp_value).group()
        #분 찾기
        take_off_airport_minute = re.search(":\d+\d+", tmp_value).group()
        #시간 데이터 비교 위해 수정 
        take_off_airport_hour = take_off_airport_hour.replace(":","")

        check_over_oneday = tmp_value.find("+1")
        #운항중 하루가 지났을 경우 예외처리 
        if check_over_oneday != -1:
            take_off_airport_hour = str(int(take_off_airport_hour)+12)

        #오후 일 경우 12시간 더해주기 
        if str_mon_night == "오후":
            if take_off_airport_hour != "12":
                take_off_airport_hour = str(int(take_off_airport_hour)+12)

        take_off = take_off_airport_hour +take_off_airport_minute
        take_off_list.append(take_off)

    #크롤링 시간 데이터
    for data in take_off_list:
        tmp_time = datetime.datetime.now() 
        formatted_now = tmp_time.strftime("%Y-%m-%d %H:%M")
        time_data_list.append(formatted_now)

    #항공 도착 시간 가져오기 
    tmp_landing = soup.find_all(class_ = "XWcVob YMlIz ogfYpf tPgKwe")


    #도착 시간 parsing
    for value in tmp_landing:

        tmp_value = value.get_text()

        str_mon_night = re.search("[가-힣]+", tmp_value).group()
        landing_airport_hour = re.search("\d+(\d+)?:", tmp_value).group()
        landing_airport_minute = re.search(":\d+\d+", tmp_value).group()

        landing_airport_hour = landing_airport_hour.replace(":","")

        check_over_oneday = tmp_value.find("+1")
        #운항중 하루가 지났을 경우 예외처리 
        if check_over_oneday != -1:
            if str_mon_night == "오전" and landing_airport_hour == "12":
                landing_airport_hour = str(int(landing_airport_hour)+12)
            elif str_mon_night == "오전": 
                landing_airport_hour = str(int(landing_airport_hour)+24)

        if str_mon_night == "오후":
            if landing_airport_hour != "12":
                landing_airport_hour = str(int(landing_airport_hour)+12)

        landing = landing_airport_hour +landing_airport_minute
        landing_list.append(landing)

    #항공사 이름 가져오기 
    tmp_airline = soup.find_all(class_ = "Ir0Voe")
    tmp_airline_inside = tmp_airline[0].find_all(class_="sSHqwe tPgKwe ogfYpf")


    for value in tmp_airline:
        str_tmp = (value.find_all(class_="sSHqwe tPgKwe ogfYpf"))[0].get_text()
        airline_list.append(str_tmp)

    #출발 공항
    tmp_airport_take_off = soup.find_all(class_="G2WY5c sSHqwe ogfYpf tPgKwe")
    tmp_airport_take_off[0].string


    for value in tmp_airport_take_off:
        airport_take_off_list.append(value.string)

    #도착 공항
    tmp_airport_landing = soup.find_all(class_="c8rWCd sSHqwe ogfYpf tPgKwe")
    tmp_airport_landing[0].string


    for value in tmp_airport_landing:
        airport_landing_list.append(value.string)

    # 운항 시간
    tmp_ftime = soup.find_all(class_="gvkrdb AdWm1c tPgKwe ogfYpf")


    for value in tmp_ftime:

        str_tmp = str(value.string)

        tmp_ftime_hour = re.search("\d+(\d+)?시간",str_tmp).group()
        check_tmp_ftime_minute = re.search("\d+\d+분",str_tmp)

        if check_tmp_ftime_minute:
            tmp_ftime_minute = check_tmp_ftime_minute.group()
        else:
            tmp_ftime_minute = "00분"

        tmp_ftime_hour = tmp_ftime_hour.replace("시간", "")

        if len(tmp_ftime_hour)<=1:
            tmp_ftime_hour = "0" + str(tmp_ftime_hour)

        ftime = tmp_ftime_hour + "시간 " + tmp_ftime_minute
        
        ftime_list.append(ftime)

    #직항 데이터 찾기 
    tmp_non_stop_transit = soup.find_all(class_="EfT7Ae AdWm1c tPgKwe")
    tmp_non_stop_transit[0].string


    for value in tmp_non_stop_transit:
        non_stop_transit_list.append(value.string)

    #편도, 왕복 데이터 

    for i in range(len(tmp_non_stop_transit)):
        one_way_round_list.append('편도')


    #편명 가져오기 
    tmp_flight_number = soup.find_all(class_= "y0NSEe axwZ3c y52p7d ogfYpf")

    for value in tmp_flight_number:
        tmp_result = value.find("div", {"data-travelimpactmodelwebsiteurl":True})["data-travelimpactmodelwebsiteurl"]
        timer_sleep.timer_sleep_by()
        index = tmp_result.find("itinerary")
        tmp_reg = re.search("\w+\w+-\d+(\d+\d+\d+)?", tmp_result[index+18:]).group()
        tmp_replace = tmp_reg.replace("-", " ")
        flight_number_list.append(tmp_replace)


    # 티켓 가격 
    tmp_ticket_price = soup.select(".BVAVmf.I11szd.POX3ye span")


    for value in tmp_ticket_price:

        tmp_ticket_price = value.get_text()

        tmp_ticket_price = tmp_ticket_price.replace("₩", "")

        ticket_price = tmp_ticket_price + "원"

        ticket_price_list.append(ticket_price)

    #데이터 합치기와 데이터 프레임 만들기 
    data = {"항공사" : airline_list,
        "이륙 시간" : take_off_list,
        "출발 공항" : airport_take_off_list,
        "착륙 시간" : landing_list,
        "도착 공항" : airport_landing_list, 
        "직항, 경유" : non_stop_transit_list,
        "항공 시간" : ftime_list,
        "크롤링 시작" : time_data_list, 
        "편도, 왕복" : one_way_round_list, 
        "티켓 가격" : ticket_price_list,
        "편명" : flight_number_list}
    
    df = pd.DataFrame(data)
    # df = df[df['티켓 가격'] != '가격을 확인할 수 없습니다.원']
    df['티켓 가격'] = df['티켓 가격'].apply(lambda x: None if x == '가격을 확인할 수 없습니다.원' else x)

     #드라이버 종료 
    driver.close()

    return df


def main():
    df = get_osaka_data()

    if not os.path.exists("/app/data"):
        df.to_csv("/app/data/google_osaka_26.csv", index=False, mode = "w", encoding="utf-8")
    else :
        df.to_csv("/app/data/google_osaka_26.csv", index=False, mode = "a", encoding="utf-8", header=False)

if __name__ == "__main__":
    main()

