# 여러개 이미지 주변에 padding을 넣고 300*300으로 변환, 새 폴더를 만들어 저장하기.
import cv2
import numpy as np
import os

image_file_list = ["hood_T", "long_T", "pola", "shirt", "short_T", "sleeveless", "vest"]
filepath = 'D:\\python_D\\fashion_project\\fashion_data\\data_test_0707\\'
save_filepath = 'D:\\python_D\\fashion_project\\fashion_data\\data_test_0819\\'


# 저장할 폴더 하나 생성
try:
    os.mkdir(save_filepath)
except:
    print(save_filepath + "이미 생성됨")
    
for img_list in range(0, len(image_file_list)) :
    img_name = image_file_list[img_list]         # hood_T
    print(img_name + " file 불러오는 중\n");
    file_list = os.listdir(filepath + img_name)  # D:\\python_D\\fashion_project\\fashion_data\\data_train_0817\\hood_T 내부의 폴더 리스트 가져옴

    # 0819폴더의 hood_T 폴더 생성
    try:
        os.mkdir(save_filepath + img_name)           # D:\\python_D\\fashion_project\\fashion_data\\data_train_0819\\hood_T 생성
    except:
        print(save_filepath+img_name+"이미 생성됨")
        
    for i in range(1, len(file_list)+1): # file_list 개수만큼 읽어옴.
        #filename = filepath + img + "\\" + img + "_" + str(i) + ".jpg"          # D:\\python_D\\fashion_project\\fashion_data\\data_train_0817\\hood_T\\hood_T_1.jpg
        filename = filepath + img_name + "\\" + img_name+"_"+str(i)+".jpg"
        print("원본파일 : " + filename)
        save_filename = save_filepath + img_name + "\\" + img_name + "_" + str(i) + ".jpg"
        print("저장될 파일 : " +save_filename)

        img = cv2.imread(filename)

        # 이미지의 x, y가 300이 넘을 경우 작게해주기
        percent = 1
        if(img.shape[1] > img.shape[0]) :       # 이미지의 가로가 세보다 크면 가로를 300으로 맞추고 세로를 비율에 맞춰서
            percent = 300/img.shape[1]
        else :
            percent = 300/img.shape[0]

        img = cv2.resize(img, dsize=(0, 0), fx=percent, fy=percent, interpolation=cv2.INTER_LINEAR)

        # 이미지 범위 지정
        y,x,h,w = (0,0,img.shape[0], img.shape[1])

        # 그림 주변에 검은색으로 칠하기
        w_x = (300-(w-x))/2  # w_x = (300 - 그림)을 뺀 나머지 영역 크기 [ 그림나머지/2 [그림] 그림나머지/2 ]
        h_y = (300-(h-y))/2

        if(w_x < 0):         # 크기가 -면 0으로 지정.
            w_x = 0
        elif(h_y < 0):
            h_y = 0

        M = np.float32([[1,0,w_x], [0,1,h_y]])  #(2*3 이차원 행렬)
        img_re = cv2.warpAffine(img, M, (300, 300))
        cv2.imshow("img_re", img_re)

        # 이미지 저장하기
        cv2.imwrite(save_filename, img_re)
        cv2.destroyAllWindows()

