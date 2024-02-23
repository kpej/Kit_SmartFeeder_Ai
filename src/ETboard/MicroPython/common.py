# *****************************************************************************************
# FileName     : common
# Description  : 공통모듈
# Author       : 손철수
# CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
# Created Date : 2024.02.22
# Reference    :
# Modified     : 2024.02.23 : SCS : Check class_id
# *****************************************************************************************

# serial_init    
def serial_init(uart):    
    uart.init(baudrate=115200,            # 시리얼 통신 속도 지정
              timeout=1000,               # 최대 1초만 수신 대기
              tx=1, rx=3)                 # 이티보드 통신 핀 번호 지정
    
    
# serial_init    
def receive_msg(uart):    
    msg = uart.readline()                 # 메시지를 1줄씩 읽음
    if msg is None:             
        return 3

    class_id = int(msg.rstrip())
    if (class_id > 3 or class_id < 0):
        class_id = 3
        
    return class_id


# ==========================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
# ==========================================================================================

