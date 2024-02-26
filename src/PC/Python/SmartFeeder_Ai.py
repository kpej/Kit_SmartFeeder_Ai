# *****************************************************************************************
# FileName     : SmartFeeder_Ai
# Description  : 스마트 팩토리 코딩 키트 - PC
# Author       : 박은정 & 손철수
# CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
# Created Date : 2024.02.22
# Reference    :
# Modified     : 2024.02.23 : SCS : Only AI
# Modified     : 2024.02.26 : SCS : Clean Code
# *****************************************************************************************

#==========================================================================================
# import
#==========================================================================================
import tensorflow.keras
import numpy as np
import cv2
import time
import serial
import serial.tools.list_ports


#==========================================================================================
# global variable
#==========================================================================================
# 웹캠 선언
camera = cv2.VideoCapture(0)                          # 웹캠 첫번째(0)
camera.set(3, 640)                                    # 웹캠 비율 640 * 480
camera.set(4, 480)

# 인공지능 학습 모델 및 레이블 파일
model_path = r"keras_model.h5"  # 학습모델 경로
model = tensorflow.keras.models.load_model(model_path)      # 학습모델 로딩
class_names = open("labels.txt", "r", encoding="UTF-8").readlines()

# 최근 추론한  클래스 ID
pre_id = ''

my_serial = serial.Serial()                           # 시리얼 포트

#==========================================================================================
# setup
#==========================================================================================
def setup():
    global my_serial
    
    # CI & BI 표    
    print('======================')
    print(' 한국공학기술연구원... ')
    print(' ETboard Ai v0.91     ')
    print('======================')    
    
    # 장치관리자에서 USB 포트 검색하기 
    ports = list(serial.tools.list_ports.comports())
    
    # USB 포트에서 ETboard 찾기
    for p in ports:
        if "USB-SERIAL CH340" in p.description:            
            try:
                my_serial = serial.Serial(p.device, baudrate=115200, timeout=1.0)
                print(f"{p} 포트에 연결하였습니다.")
                time.sleep(2)
            except Exception as e:
                print("\n", e)
                print(f"{p} 포트에 연결할 수 없습니다.")
                print("다른 프로그램에서 사용하고 있으면 연결을 끊으세요")
                print("그래도 안되면 PC를 재부팅하세요\n")
                exit(1)
            return
        
    # ETboard 찾기 실패    
    print("\n오류!!!\nETboard가 연결되어 있지 않습니다.\nETboard를 연결을 확인하십시오\n")
    exit(1)

#==========================================================================================
# send_etboard    
#==========================================================================================    
def send_etboard(id):
    my_serial.write(str(id).encode())    

#==========================================================================================
# main                                       
#==========================================================================================
def main():
    global pre_id
    
    _, image = camera.read()
    cv2.imshow('camera out', image)

    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)       # 웹캠이미지를 224, 224로 사이즈 조정        
    image_normalized = (image.astype(np.float32) / 127.0) - 1                 # 정규화        
    image_reshaped = image_normalized.reshape((1, 224, 224, 3))               #

    prediction = model.predict(image_reshaped)                                # 추론/예측
    cur_id = np.argmax(prediction[0])                                         # 결과
    print(class_names[cur_id], np.max(prediction[0]) * 100, "%")

    if np.max(prediction[0]) > 0.9 and cur_id != pre_id:
        print("검출...이티보드로 메시지 전송")
        send_etboard(cur_id)
        pre_id = cur_id
        time.sleep(3.0)


#==========================================================================================
# start point
#==========================================================================================
if __name__ == '__main__':
    setup()
    while(camera.isOpened()):
        main()        
        if cv2.waitKey(100) == ord('q'):
            break
        
    cv2.destroyAllWindows()    
    my_serial.close()
    
# ==========================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
# ==========================================================================================
