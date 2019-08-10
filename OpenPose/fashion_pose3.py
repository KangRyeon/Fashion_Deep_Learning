# fashion_pose3.py : 여러 개 파일에 대해 상의, 하의, 전체에 대해 자동으로 저장할 수 있음. 해당하는 곳에 imwrite 해야 함.
# fashion_pose2.py 변형
# original이라는 폴더 내부의 hood_T라는 폴더 내부 이미지 개수 받아와 그만큼 돌아가며, original 폴더 밑에 hood_T_cut_final 이라는 폴더를 생성해 저장함.

import cv2
from PIL import Image
from numpy import array
import os

# 이미지를 넘겨주면 이미지 가로(image.shape[1]), 세로(shape[0])중 큰것을 300으로 맞추는 비율 찾아 사이즈 줄이고, 그 이미지 반환
def image_resize(img):
    percent = 1
    if(img.shape[1] > img.shape[0]) :       # 이미지의 가로가 세보다 크면 가로를 300으로 맞추고 세로를 비율에 맞춰서
        percent = 300/img.shape[1]
    else :
        percent = 300/img.shape[0]

    img = cv2.resize(img, dsize=(0, 0), fx=percent, fy=percent, interpolation=cv2.INTER_LINEAR)
    return img


# 검출한 키포인트 리스트 받아 x중에 max, min y중에 max, min 찾아 4개 값 반환, padding 정해주기, mode = 0(전신), 1(상반신), 2(하반신)
def image_cut_point(point_list, img_width, img_height, mode):
    upper_padding = 5
    under_padding = 30
    left_padding = 30
    right_padding = 30
    
    x_max = 0
    x_min = 9999
    y_max = 0
    y_min = 9999

    isNone = False
    
    mode_print = ["전신", "상반신", "하반신"]
    point_range = [list(range(len(point_list)))                     # point_range = [[전신], [상반신], [하반신]]
                    , [1, 2, 3, 4, 5, 6, 7, 8, 11]
                    , [8, 9, 10, 11, 12, 13]] 
    print("mode = " + str(mode) + ", " + mode_print[mode])      
    for i in point_range[mode]:
        if(point_list[i] != None) :
            print("i는 " , i , " (", point_list[i][0], ", ", point_list[i][1], ") : (", x_max, ", ", x_min, ", ", y_max, ", ", y_min, ")")
            if(point_list[i][0] > x_max):
                x_max = point_list[i][0]
            if(point_list[i][0] < x_min):
                x_min = point_list[i][0]
            if(point_list[i][1] > y_max):
                y_max = point_list[i][1]
            if(point_list[i][1] < y_min):
                y_min = point_list[i][1]
        else :
            print("i는 " , i , " (None) : (", x_max, ", ", x_min, ", ", y_max, ", ", y_min, ")")
            isNone = True       # point에 None(찾을수 없는 점) 이 있으면 
        

    x_max = x_max+right_padding
    x_min = x_min-left_padding
    y_max = y_max+left_padding
    y_min = y_min-upper_padding
    if(x_max > img_width):       # +20한 것이 사진보다 커지면 사진의 max 사이즈로
        x_max = img_width
    if(x_min < 0):               # -20한 것이 사진보다 작아지면 사진의 min 사이즈인 0으로
        x_min = 0
    if(y_max > img_height):
        y_max = img_height
    if(y_min < 0):
        y_min = 0

    # 검출되지 않은 점이 있으면
    if(isNone):
        if(mode == 0):              # 전신일때 0(머리)이 없으면 y_min = 0으로, 10,13(발목)이 없으면  y_max = 0으로
            if(point_list[0] == None):
                y_min = 0
            if((point_list[10] == None) or (point_list[13] == None)):
                y_max = img_height
            if(point_list[6] == None):  # 왼쪽 팔꿈치 없으면 x_max=0~x_min 거리만큼 오른쪽끝~x_min 거리만큼
                x_max = img_width - x_min
                
        elif(mode == 1):         # 상반신일때 0(머리)이 없으면 y_min = 0으로, 8, 11(힙)이 없으면 y_max = img_height로
            if(point_list[0] == None):
                y_min = 0
            if((point_list[8] == None) or (point_list[11] == None)):
                y_max = img_height
            if(point_list[6] == None):  # 왼쪽 팔꿈치 없으면 x_max=0~x_min 거리만큼 오른쪽끝~x_min 거리만큼
                x_max = img_width - x_min
                
        elif(mode == 1):         # 하반신일때 8, 11(힙)이 없으면 y_min = 0으로, 10, 13(발목)이 없으면 y_max = img_height로
            if((point_list[8] == None) or (point_list[11])):
                y_min = 0
            if((point_list[10] == None) or (point_list[13] == None)):
                y_max = img_height

        
    return x_max, x_min, y_max, y_min
            

    
    
BODY_PARTS_ARRAY = ["Head", "Neck", "RShoulder", "RElbow", "RWrist",                                                # MPII에서 각 파트 번호, 선으로 연결될 POSE_PAIRS
                "LShoulder", "LElbow", "LWrist", "RHip", "RKnee",
                "RAnkle", "LHip", "LKnee", "LAnkle", "Chest",
                "Background" ]

BODY_PARTS = { "Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
                "Background": 15 }

POSE_PAIRS = [ ["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
                ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
                ["LElbow", "LWrist"], ["Neck", "Chest"], ["Chest", "RHip"], ["RHip", "RKnee"],
                ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"] ]


# 각 파일 path
protoFile = "D:\\python_D\\fashion_project\\fashion_data\\pose_deploy_linevec_faster_4_stages.prototxt"
weightsFile = "D:\\python_D\\fashion_project\\fashion_data\\pose_iter_160000.caffemodel"

# 위의 path에 있는 network 불러오기
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

# 이미지별로 처리해서 저장
image_file_list = ["hood_T", "long_T", "pola", "shirt", "short_T", "sleeveless", "vest"]
#image_file_list = ["pola"]
for i in range(0, len(image_file_list)) :
    img = image_file_list[i]

    # 각 폴더(hood_T) 내의 이미지가 몇개인지 받아옴(original\\hood_T)
    file_list_num = len(os.listdir("D:\\python_D\\fashion_data\\original\\" + img))


    # 이미지 저장위한 폴더 생성
    cut_folder = ''
    try:
        folder = "D:\\python_D\\fashion_project\\fashion_data\\original\\" + img + "_cut_final"    # D:\\python_D\\fashion_project\fashion_data\original\\hood_T_cut_final 이라는 폴더경로이름
        os.mkdir(folder)                                            # 각 품종에 대한 폴더 생성함.
        print(img + "_cut" + " : 폴더 생성 성공")
    except:
        print(folder+": 폴더 생성 실패 또는 이미 만들어짐.")
            
    print(img+" file 불러오는 중\n");
    for j in range(1, file_list_num):
        #image_name = "D:\\python_D\\fashion_project\\fashion_data\\data_train10\\"+img+"\\"+img + "_" + str(j) + ".jpg"
        image_name = "D:\\python_D\\fashion_project\\fashion_data\\original\\"+img+"\\"+img + "_" + str(j) + ".jpg"
        original_image = cv2.imread(image_name)
        image = cv2.imread(image_name)
        cv2.imshow("original", original_image)

        cut_filename = img+"_"+str(j)+".jpg"   # hood_T_1.jpg


        # image_resize( ) : 이미지 resize하기 위에서 만든 함수
        image = image_resize(image)
        resize_image = image_resize(original_image)
        cv2.imshow("resize", image)

        imageHeight, imageWidth, _ = image.shape                                                                            # frame.shape = 불러온 이미지에서 height, width, color 받아옴

        inpBlob = cv2.dnn.blobFromImage(image, 1.0 / 255, (imageWidth, imageHeight), (0, 0, 0), swapRB=False, crop=False)   # network에 넣기위해 전처리
        net.setInput(inpBlob)                                                                                               # network에 넣어주기
        output = net.forward()                                                                                              # 결과 받아오기

        H = output.shape[2]                                                                                                 # output.shape[0] = 이미지 ID, [1] = 출력 맵의 높이, [2] = 너비
        W = output.shape[3]
        print("이미지 ID : ", len(output[0]), ", H : ", output.shape[2], ", W : ",output.shape[3])                          # 이미지 ID

        # 키포인트 검출시 이미지에 그려줌
        points = []
        for i in range(0,15):
            probMap = output[0, i, :, :]                                                                                    # 해당 신체부위 신뢰도 얻음.
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)                                                            # global 최대값 찾기

            x = (imageWidth * point[0]) / W                                                                                 # 원래 이미지에 맞게 점 위치 변경
            y = (imageHeight * point[1]) / H

            # 키포인트 검출한 결과가 0.1보다 크면(검출한곳이 위 BODY_PARTS랑 맞는 부위면) points에 추가, 검출했는데 부위가 없으면 None으로
            if prob > 0.1 :
                cv2.circle(image, (int(x), int(y)), 3, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)                    # circle(그릴곳, 원의 중심, 반지름, 색)
                print(str(i), "검출된", BODY_PARTS_ARRAY[i], " 점 : ",str(x), str(y), "\n")

                cv2.putText(image, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, lineType=cv2.LINE_AA)
                points.append((int(x), int(y)))
            else :
                points.append(None)

        print(points)

        # 전체
        # image_cut_point( ) : 이미지 어느 점 기준으로 자를 것인지 받아오기 위에서 만든 함수
        try:
            x_max, x_min, y_max, y_min = image_cut_point(points, image.shape[1], image.shape[0], 0)
            print("(x_max, x_min, y_max, y_min) = (", x_max, ", ", x_min, ", ", y_max, ", ", y_min, ")")
            cut = resize_image[y_min:y_max, x_min:x_max]
            cut2 = image[y_min:y_max, x_min:x_max]
            #cv2.imwrite('D:\\python_D\\fashion_project\\fashion_data\\original\\'+ img + "_cut_final\\" + cut_filename,cut2)    # filenmae 위에서 설정
            cv2.imshow("cut_image1",cut2)
        except:
            print("전체가 존재하지 않음.")

        # 상의
        try:
            x_max, x_min, y_max, y_min = image_cut_point(points, image.shape[1], image.shape[0], 1)
            print("(x_max, x_min, y_max, y_min) = (", x_max, ", ", x_min, ", ", y_max, ", ", y_min, ")")
            cut3 = resize_image[y_min:y_max, x_min:x_max]
            cv2.imwrite('D:\\python_D\\fashion_project\\fashion_data\\original\\'+ img + "_cut_final\\" + cut_filename,cut3)
            cv2.imshow("cut_image2",cut3)
        except:
            print("상의부분이 존재하지 않음.")

        # 하의
        try:
            x_max, x_min, y_max, y_min = image_cut_point(points, image.shape[1], image.shape[0], 2)
            print("(x_max, x_min, y_max, y_min) = (", x_max, ", ", x_min, ", ", y_max, ", ", y_min, ")")
            cut4 = resize_image[y_min:y_max, x_min:x_max]
            #cv2.imwrite(''D:\\python_D\\fashion_project\\fashion_data\\original\\'+ img + "_cut_final\\" + cut_filename,cut4)
            cv2.imshow("cut_image3",cut4)
        except:
            print("하의부분이 존재하지 않음.")
            
        # 점찍힌 이미지 복사
        imageCopy = image

        # 각 POSE_PAIRS별로 선 그어줌 (머리 - 목, 목 - 왼쪽어깨, ...)
        for pair in POSE_PAIRS:
            partA = pair[0]             # Head
            partA = BODY_PARTS[partA]   # 0
            partB = pair[1]             # Neck
            partB = BODY_PARTS[partB]   # 1

            #print(partA," 와 ", partB, " 연결\n")
            if points[partA] and points[partB]:
                cv2.line(imageCopy, points[partA], points[partB], (0, 255, 0), 2)


        cv2.imshow("final_image",imageCopy)
#        cv2.waitKey(0)
        cv2.destroyAllWindows()



        print(img + "_" + str(j) + ".jpg 불러옴")
    print(img + "file 다 불러옴\n");
