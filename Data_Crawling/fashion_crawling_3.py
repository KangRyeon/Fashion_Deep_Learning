# fashion_crawling_3.py : 각 옷 200장 크롤링, 페이지 다운, 각 폴더 생성 자동화
# 옷 사진 셀레니움으로 크롤링(outer : 가디건, 자켓, 패딩, 롱패딩, 코트, 점퍼, 후드집업)
# fashion_data, giodano 라는 폴더는 미리 생성해 두어야 함.
# 보이는 페이지에서 데이터를 얻을 경우 (보이는 페이지에서 눌러 들어가 데이터를 얻을 경우는 fashion_crawling_4.py에)
# chrischristy 크롤링
import requests
import urllib.request
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

# 변수 설정
download_count = 200                                                    # download_count = 다운받을 이미지 총 개수
python_path = "D:\\python_D\\"                                          # python 경로 표시
#save_path = python_path + "fashion_project\\fashion_data\\outer\\"                     # save 경로 표시 (D:\\python_D\\fashion_project\\fashion_data\\outer\\)
save_path = python_path + "fashion_project\\fashion_data\\giodano\\"

# 옷 종류만큼 크롤링 시작(download_count만큼 크롤링하게 됨.)
for i in range(0, 1):
    try:
        # url(내가 다운받을 곳의 크롬에서 주소)
        url = "http://chrischristy.com/product/list.html?cate_no=64"
        folder_name = "vest"
        file_name = folder_name+"_"                                     # 이 파일 이름으로 저장될 것. (vest_)
        driver = webdriver.Chrome(executable_path="D:\\python_D\\chromedriver.exe")
        driver.get(url)

        # 페이지 로딩까지 기다림
        time.sleep(2)
        
        # 이미지 저장위한 폴더 생성
        folder = ''
        try:
            folder = save_path + folder_name    # D:\python_D\fashion_project\\fashion_data\\giodano\\ 이라는 폴더경로이름
            os.mkdir(folder)                                            # 각 품종에 대한 폴더 생성함.
            print(folder_name + " : 폴더 생성 성공 : ")
        except:
            print(folder+": 폴더 생성 실패 또는 이미 만들어짐.")
            

        
        count = 0                                                      # Google 로고와 아이콘(2장)을 버리기 위해 -1로 설정.
        img = driver.find_elements_by_tag_name("img")                   # img 태그를 찾고,
        
        print("이미지들 받음")
        for item in img:
            print("이미지들중에 하나")
            if("jpg" in item.get_attribute('src')):
                if(count < 0):
                    count = count+1
                    continue
                print("이미지들중에 둘, count = ", count, ", download_count = ", download_count)
                print("받아온 img 태그 : "+item.get_attribute('src')[:30] + " : ")
                if(count > 0 and count < download_count):                   # D:\python_D\fashion_data\outer\cardigan\cardigan_1.jpg 로 저장될 것.
                    print("이미지들중에 셋")
                    full_name = save_path + folder_name + "\\" + file_name + str(count) + ".jpg"
                    print("이미지들중에 넷")
                    print("full_name : " + full_name)
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
        print(folder_name+"다 받음. %d 개"%count)
        driver.quit()
