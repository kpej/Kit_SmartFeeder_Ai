# *****************************************************************************************
# FileName     : SmartFeeding_Ai
# Description  : 스마트 팩토리 코딩 키트 (기본)
# Author       : 박은정
# CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
# Created Date : 2024.02.22
# Reference    :
# Modified     : 2024.02.23 : SCS : Only AI
# *****************************************************************************************

# import                         
import time
import sys
from machine import UART, Pin, PWM
from ETboard.lib.pin_define import *
from ETboard.lib.OLED_U8G2 import *
from common import *

# global variable
led_op = Pin(5)                           # 동작 LED 핀 지정
led_red = Pin(D2)                         # 빨강 LED 핀 지정
led_blue = Pin(D3)                        # 파랑 LED 핀 지정
led_green = Pin(D4)                       # 초록 LED 핀 지정
led_yellow = Pin(D5)                      # 노랑 LED 핀 지정

oled = oled_u8g2()                        # OLED

class_names = ['dog', 'chicken', 'giraffe', 'none']

uart = UART(1)                            # 시리얼 통신 포트 지정

# setup
def setup():
    led_op.init(Pin.OUT)                  # 동작 LED 출력모드 설정
    
                                          # 모터와 LED 겸용     
    led_red.init(Pin.OUT)                 # 빨강 LED 출력모드 설정
    led_blue.init(Pin.OUT)                # 파랑 LED 출력모드 설정
    led_green.init(Pin.OUT)               # 초록 LED 출력모드 설정
    led_yellow.init(Pin.OUT)              # 노랑 LED 출력모드 설정
    
    serial_init(uart)                     # USB 시리얼 통신 설정
    
    motor_off()                           # 모터 끄기


# main loop
def loop():   
    led_op.value(HIGH)    
    time.sleep(0.1)
    
    ai_process()
    
    led_op.value(LOW)
    time.sleep(0.1)

# ai_process
def ai_process():
    class_id = receive_msg(uart)          # PC에서 1초 동안 class_id 수신    
    id_line = "Class ID: " + str(class_id)
    name_line = "Name: %s" %(class_names[class_id])
    
    oled.clear()                          # OLED에 초기화하고 표시하기    
    oled.setLine(1, "* Ai Feeder *")    
    oled.setLine(3, id_line)
    oled.setLine(5, name_line)
    oled.display()

    if class_id == 0:                     # 강아지면
        food_supply()                     # 먹이 공급하기
    
    return
    
    
# 사료 공급
def food_supply():
    oled.setLine(7, "Motor On")
    oled.display()    
    motor_on()
    
    time.sleep(3)
    
    oled.setLine(7, "Motor Off")
    oled.display()
    motor_off()


# 모터 켜기
def motor_on():
    led_red.value(HIGH)           # DC 모터
    led_blue.value(HIGH)

    led_green.value(HIGH)         # 진동 모터
    led_yellow.value(HIGH)

# 모터 끄기
def motor_off():
    led_red.value(LOW)           # DC 모터
    led_blue.value(LOW)

    led_green.value(LOW)         # 진동 모터
    led_yellow.value(LOW)
    
    
# start point
if __name__ == "__main__" :
    setup()
    while True :
        loop()


# ==========================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
# ==========================================================================================
