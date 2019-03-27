# fashion_crawling_1.py : test를 위한 코드(가디건 5장만 크롤링해보기)
# 옷 사진 셀레니움으로 크롤링(outer : )
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

# 검색어
search = '가디건'                               # cardigan
folder_name = "cardigan"                        # 이 폴더 안에
file_name = "cardigan_"                         # 이 파일 이름으로 저장될 것.

# url(내가 다운받을 곳의 크롬에서 주소)
url = "https://www.google.com/search?biw=1388&bih=1053&tbm=isch&sa=1&ei=dZybXKfdLvSFr7wP1MKR-AU&q="+search+"&oq="+search+"&gs_l=img.3..35i39j0l9.141911.210484..210605...0.0..3.141.2339.10j12......1....1..gws-wiz-img.....0..0i30.HOlw9AU3P4c"

driver = webdriver.Chrome(executable_path="D:\\python_D\\chromedriver.exe")
driver.get(url)

# Google 로고와 아이콘(2장)을 버리기 위해 -1로 설정.
count = -1

img = driver.find_elements_by_tag_name("img")   # img 태그를 찾고,
for item in img:
    if(count < 0):
        count = count+1
        continue
    if(count > 0 and count <= 5):               # D:\python_D\fashion_data\outer\cardigan\cardigan_1.jpg 로 저장될 것.
        full_name = "D:\\python_D\\fashion_data\\outer\\"+ folder_name + "\\" + file_name + str(count) + ".jpg"
        try:
            urllib.request.urlretrieve(item.get_attribute('src'), full_name) # src를 받는다.
            print(item.get_attribute('src')[:30] + " : ")
        except:
            urllib.request.urlretrieve(item.get_attribute('data-src'), full_name)
            print(item.get_attribute('data-src')[:30] + " : ")
        print("{0}. Saving : {1}".format(count,full_name))
    count = count+1
    
driver.quit()
print("Saved!")                                  # 다 다운받으면 Saved! 출력됨.
