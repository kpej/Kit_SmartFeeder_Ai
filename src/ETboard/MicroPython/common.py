# *****************************************************************************************
# FileName     : common
# Description  : 공통모듈
# Author       : 손철
# CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
# Created Date : 2024.02.22
# Reference    :
# Modified     : 
# *****************************************************************************************

# serial_init    
def serial_init(uart):    
    uart.init(baudrate=115200,            # 시리얼 통신 속도 지정
              timeout=1000,               # 최대 1초만 수신 대기
              tx=1, rx=3)                 # 이티보드 통신 핀 번호 지정
    
    
# serial_init    
def receive_msg(uart):    
    msg = uart.readline()                 # 메시지를 1줄씩 읽음
    if msg is None:                       # 어떤 메시지도 받지 못하면
        #led_yellow.value(HIGH)            # 노랑 LED 깜밖임
        #time.sleep(0.5)      
        #led_yellow.value(LOW)      
        #time.sleep(0.5)      
        return

    class_id = int(msg.rstrip())
    #return class_id
