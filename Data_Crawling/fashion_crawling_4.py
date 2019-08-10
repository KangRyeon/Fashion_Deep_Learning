# fashion_crawling_4.py : 각 옷 200장 크롤링, 페이지 다운, 각 폴더 생성 자동화
# 옷 사진 셀레니움으로 크롤링(outer : 가디건, 자켓, 패딩, 롱패딩, 코트, 점퍼, 후드집업)
# fashion_data, giodano 라는 폴더는 미리 생성해 두어야 함.
# 보이는 페이지에서 눌러 들어가 데이터를 얻을 경우
# shesmiss x list 에서 할때
import requests
import urllib.request
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

# 변수 설정
download_count = 2000                                                    # download_count = 다운받을 이미지 총 개수
python_path = "D:\\python_D\\"                                          # python 경로 표시
#save_path = python_path + "\\fashion_data\\outer\\"                     # save 경로 표시 (D:\\python_D\\fashion_data\\outer\\)
save_path = python_path + "fashion_project\\fashion_data\\giodano\\"

# 게시글 그림 눌렀을 때 들어갈 주소 모음
arr_href = []

# 옷 종류만큼 크롤링 시작(download_count만큼 크롤링하게 됨.)
for i in range(0, 1):   # 옷의 종류(7번 루프 돎.)
    try: # 중간에 오류나는 것 방지
        # url(내가 다운받을 곳의 크롬에서 주소)
        #url = "https://www.google.com/search?biw=1388&bih=1053&tbm=isch&sa=1&ei=dZybXKfdLvSFr7wP1MKR-AU&q="+search+"&oq="+search+"&gs_l=img.3..35i39j0l9.141911.210484..210605...0.0..3.141.2339.10j12......1....1..gws-wiz-img.....0..0i30.HOlw9AU3P4c"
        url = "http://www.idfmall.co.kr/shop/big_section.php?page=9&cno1=1084&cno2=1075&sort="
        folder_name = "shirt"
        file_name = folder_name+"_"                                     # 이 파일 이름으로 저장될 것. (cardigan_)
        driver = webdriver.Chrome(executable_path="D:\\python_D\\chromedriver.exe")
        driver.get(url)

        # 페이지 로딩까지 기다림
        time.sleep(2)
        
        # 이미지 저장위한 폴더 생성
        folder = ''
        try:
            folder = save_path + folder_name    # D:\python_D\fashion_data\outer\cardigan 이라는 폴더경로이름
            os.mkdir(folder)                                            # 각 품종에 대한 폴더 생성함.
            print(folder_name + " : 폴더 생성 성공 : ")
        except:
            print(folder+": 폴더 생성 실패 또는 이미 만들어짐.")
            

        # 이미지 그림 누를것들 주소 윗부분 가져옴
        try:
            post = driver.find_elements_by_xpath('//*[@class="prdimg"]')            # <div class="prdimg"> <a href="/암호화된 주소/"> 형식.
            print("클래스 검색성공", len(post))
        except:
            print("클래스 검색실패")

        # 이미지 그림 누를것들 주소 가져옴
        j = 0
        for u in post:          # 모든 prdimg 클래스를 가진 요소에서 a태그의 href부분 가져옴.
            href = u.find_element_by_css_selector('a').get_attribute('href')            # 클래스검색 -> 그밑의 태그검색
            #href = post[0].find_element_by_css_selector('a').get_attribute('href') 이것과 같음.
            
            print("주소받아옴[%d] : %s" %(j, href))
            arr_href.append(href) # 게시글 주소가 담길 리스트에 넣어줌.
            j = j + 1     # j = 담은 게시글 개수


        count = 1285                                                      # count = 이름_번호 에 들어갈 번호 count
        # 이미지 그림 눌러 들어가 이미지 다운
        for h in arr_href:
            url = h                        # 게시글 주소 담겨있음.
            driver.implicitly_wait(2)
            driver.get(url)

            img = driver.find_elements_by_tag_name("img")                   # img 태그를 찾고,
    #        img = driver.find_element_by_class_name('//*[@id="contents"]/div/div[2]/ul/li[1]/div/ul/li[1]/a/img')
                                                     #//*[@id="contents"]/div/div[2]/ul/li[1]/div/ul/li[1]/a/img
                                                     #//*[@id="contents"]/div/div[2]/ul/li[2]/div/ul/li[1]/a/img
            print("---------------이미지그림 눌림")
            for item in img:
                if("jpg" in item.get_attribute('src')):
                    if(count < 0):
                        count = count+1
                        continue
                    
                    if(count > 0 and count < download_count):                   # D:\python_D\fashion_data\outer\cardigan\cardigan_1.jpg 로 저장될 것.
                        full_name = save_path + folder_name + "\\" + file_name + str(count) + ".jpg"
                        print("full_name : " + full_name)
                        try:
                            urllib.request.urlretrieve(item.get_attribute('src'), full_name) # src를 받는다.
                            print(item.get_attribute('src')[:30] + " : ")
                        except:
                            urllib.request.urlretrieve(item.get_attribute('data-src'), full_name)
                            print(item.get_attribute('data-src')[:30] + " : ")
                        print("{0}. Saving : {1}".format(count,full_name))
                    count = count+1

            print("Saved!")                                                 # 다 다운받으면 Saved! 출력됨.
    except :
        print(folder_name+"다 받음. %d 개"%count)
        driver.quit()
