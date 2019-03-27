# fashion_crawling_2.py : 각 옷 200장 크롤링, 페이지 다운, 각 폴더 생성 자동화
# 옷 사진 셀레니움으로 크롤링(outer : 가디건, 자켓, 패딩, 롱패딩, 코트, 점퍼, 후드집업)
'''
* outer 분류
1. 가디건 : cardigan
2. 자켓 : jacket
3. 패딩 : padding
4. 롱패딩 : long_padding
5. 코트 : coat
6. 점퍼 : jumper
7. 후드집업 : hood_zipup
'''

import requests
import urllib.request
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

# 옷 종류
#clothing = ["가디건", "자켓", "패딩", "롱패딩", "코트", "점퍼", "후드집업"]
clothing = ["가디건"]
clothing_en = ["cardigan", "jacket", "padding", "long_padding", "coat", "jumper", "hood_zipup"]

# 변수 설정
download_count = 200                                                    # download_count = 다운받을 이미지 총 개수
python_path = "D:\\python_D\\"                                          # python 경로 표시
save_path = python_path + "\\fashion_data\\outer\\"                     # save 경로 표시 (D:\\python_D\\fashion_data\\outer\\)


# 옷 종류만큼 크롤링 시작(download_count만큼 크롤링하게 됨.)
for i in range(0, len(clothing)):   # 옷의 종류(7번 루프 돎.)
    try: # 중간에 오류나는 것 방지
        # 검색어
        search = clothing[i]                                            # 한국어로 검색(가디건, 자켓, ...)
        folder_name = clothing_en[i]                                    # savepath 밑에 만들 폴더 (cardigan)
        file_name = folder_name+"_"                                     # 이 파일 이름으로 저장될 것. (cardigan_)

        # url(내가 다운받을 곳의 크롬에서 주소)
        url = "https://www.google.com/search?biw=1388&bih=1053&tbm=isch&sa=1&ei=dZybXKfdLvSFr7wP1MKR-AU&q="+search+"&oq="+search+"&gs_l=img.3..35i39j0l9.141911.210484..210605...0.0..3.141.2339.10j12......1....1..gws-wiz-img.....0..0i30.HOlw9AU3P4c"

        driver = webdriver.Chrome(executable_path="D:\\python_D\\chromedriver.exe")
        driver.get(url)

        # pagedown 하기
        body = driver.find_element_by_tag_name("body")
        for num in range(0,100):                                        # 페이지 다운 100번 할 것. 100번 하면서 가장 밑으로 내려가고, 처음부터 받아올 수 있음.
            body.send_keys(Keys.PAGE_DOWN)
            if(num % 10 == 0):
                print("페이지다운")
            #time.sleep(1)
        time.sleep(2)

                
        # 이미지 저장위한 폴더 생성
        folder = ''
        try:
            folder = save_path + folder_name    # D:\python_D\fashion_data\outer\cardigan 이라는 폴더경로이름
            os.mkdir(folder)                                            # 각 품종에 대한 폴더 생성함.
            print(folder_name + " : 폴더 생성 성공 : ")
        except:
            print(folder+": 폴더 생성 실패 또는 이미 만들어짐.")

        count = -1                                                      # Google 로고와 아이콘(2장)을 버리기 위해 -1로 설정.
        img = driver.find_elements_by_tag_name("img")                   # img 태그를 찾고,

        for item in img:
            if(count < 0):
                count = count+1
                continue
            if(count > 0 and count < download_count):                   # D:\python_D\fashion_data\outer\cardigan\cardigan_1.jpg 로 저장될 것.
                full_name = save_path + folder_name + "\\" + file_name + str(count) + ".jpg"
                try:
                    urllib.request.urlretrieve(item.get_attribute('src'), full_name) # src를 받는다.
                    print(item.get_attribute('src')[:30] + " : ")
                except:
                    urllib.request.urlretrieve(item.get_attribute('data-src'), full_name)
                    print(item.get_attribute('data-src')[:30] + " : ")
                print("{0}. Saving : {1}".format(count,full_name))
            count = count+1

        driver.quit()
        print("Saved!")                                                 # 다 다운받으면 Saved! 출력됨.
    except :
        print(clothing[i]+"다 받음. %d 개"%count)
        driver.quit()
