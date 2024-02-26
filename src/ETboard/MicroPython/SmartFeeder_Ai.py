# *****************************************************************************************
# FileName     : SmartFeeder_Ai.py
# Description  : 스마트 팩토리 코딩 키트(Ai)
# Author       : 박은정
# CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
# Created Date : 2024.02.22
# Reference    :
# Modified     : 2024.02.23 : SCS : Only AI
# Modified     : 2024.02.26 : PEJ : 코드 정리 및 주석 수정
# *****************************************************************************************


#==========================================================================================
# import
#==========================================================================================                     
import time                                           # 시간 관련 모듈
from machine import Pin, UART                         # 핀 및 시리얼 통신 관련 모듈
from ETboard.lib.pin_define import *                  # ETboard 핀 관련 모듈
from ETboard.lib.OLED_U8G2 import *                   # ETboard OLED 관련 모듈
from common import *                                  # ETboard 시리얼 통신 관련 모듈


#==========================================================================================
# global variable
#==========================================================================================
led_op = Pin(5)                                       # 동작 LED 핀 지정
led_red = Pin(D2)                                     # 빨강 LED 핀 지정
led_blue = Pin(D3)                                    # 파랑 LED 핀 지정
led_green = Pin(D4)                                   # 초록 LED 핀 지정
led_yellow = Pin(D5)                                  # 노랑 LED 핀 지정

oled = oled_u8g2()                                    # oled 선언

uart = UART(1)                                        # 시리얼 통신 포트 지정

class_names = ['dog', 'chicken', 'giraffe', 'none']   # 개체 리스트 저장

count = 0                                             # 사료 공급 횟수 저장 변수


#==========================================================================================
# setup
#==========================================================================================
def setup():
    led_op.init(Pin.OUT)                              # 동작 LED 출력모드 설정

    # 모터 동작과 LED 겸용     
    led_red.init(Pin.OUT)                             # 빨강 LED 출력모드 설정
    led_blue.init(Pin.OUT)                            # 파랑 LED 출력모드 설정
    led_green.init(Pin.OUT)                           # 초록 LED 출력모드 설정
    led_yellow.init(Pin.OUT)                          # 노랑 LED 출력모드 설정

    serial_init(uart)                                 # USB 시리얼 통신 설정

    motor_off()                                       # 모터 중지


#==========================================================================================
# main loop
#==========================================================================================
def loop():
    led_op.value(HIGH)                                # 정상 동작 확인을 위해 led_op를 켬
    time.sleep(0.1)                                   # 0.1초 대기

    ai_process()                                      # ai_process 함수 호출

    led_op.value(LOW)                                 # 정상 동작 확인을 위해 led_op를 끔
    time.sleep(0.1)                                   # 0.1초 대기


#==========================================================================================
# ai_process                                          # 수신 데이터가 강아지면 사료 공급
#==========================================================================================
def ai_process():
    # 전역 변수 호출
    global count

    class_id = receive_msg(uart)                      # PC에서 1초 동안 class_id 수신    
    id_line = "Class ID: " + str(class_id)            # Class ID 정보 문자열 생성
    name_line = "Name: %s" %(class_names[class_id])   # 개체 정보 문자열 생성
    count_line = "Count: %d" %(count)                 # count 값 표시 문자열 생성

    oled.clear()                                      # OLED에 초기화하고 표시하기    
    oled.setLine(1, "* Ai Feeder *")                  # OLED 첫 번째 줄: 시스템 이름
    oled.setLine(2, id_line)                          # OLED 두 번째 줄: class id
    oled.setLine(3, name_line)                        # OLED 세 번째 줄: 개체 이름
    oled.setLine(4, count_line)                       # OLED 네 번째 줄: count 값
    oled.display()                                    # OLED 출력

    if class_id == 0:                                 # 수신받은 개체가 강아지면
        food_supply()                                 # food_supply 함수 호출
        count += 1                                    # count 1 증가


#==========================================================================================
# food_supply                                         # OLED 표시 및 모터 제어
#==========================================================================================
def food_supply():
    oled.setLine(5, "Motor On")                       # OLED 다섯 번째 줄: Motor on
    oled.display()                                    # OLED 출력
    motor_on()                                        # motor_on 함수 호출

    time.sleep(3)                                     # 3초간 대기

    oled.setLine(5, "Motor Off")                      # OLED 다섯 번째 줄: Motor Off
    oled.display()                                    # OLED 출력
    motor_off()                                       # motor_off 함수 호출


#==========================================================================================
# motor_on                                            # DC 모터, 진동 모터 켜기
#==========================================================================================
def motor_on():                   
    led_red.value(HIGH)                               # DC 모터 켜기
    led_blue.value(HIGH)

    led_green.value(HIGH)                             # 진동 모터 켜기
    led_yellow.value(HIGH)


#==========================================================================================
# motor_off                                           # DC 모터, 진동 모터 끄기
#==========================================================================================
def motor_off():
    led_red.value(LOW)                                # DC 모터 끄기
    led_blue.value(LOW)

    led_green.value(LOW)                              # 진동 모터 끄기
    led_yellow.value(LOW)


#==========================================================================================
# start point
#==========================================================================================
if __name__ == "__main__" :
    setup()
    while True :
        loop()


# ==========================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
# ==========================================================================================