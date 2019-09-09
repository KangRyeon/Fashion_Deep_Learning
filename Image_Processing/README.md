이미지 전처리를 위한 파이썬 파일 모음

* rename_file.py
    - 상위폴더를 지정하면 하위폴더 이름을 받아 하위폴더이름_1.jpg 등 숫자가 뒤에 붙은 형태로 변경함.
    - animals/cat/2348efs12.jpg : 원래 랜덤의 이름을 가진 파일명을
      animals/cat/cat_1.jpg     : 하위폴더명_1.jpg 로 변경함.

* image_padding_one.py
    - 한개의 이미지 크기를 줄이고, 300 x 300으로 패딩을 입혀 저장
    - filename에 지정한 파일을 save_filename에 지정한 파일 이름으로

* image_padding.py
    - 여러개 이미지 크기를 줄이고, 300 x 300으로 패딩을 입혀 저장
