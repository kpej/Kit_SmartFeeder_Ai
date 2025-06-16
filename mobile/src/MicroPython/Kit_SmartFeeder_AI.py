# ******************************************************************************************
# FileName     : Kit_SmartFeeder_AI.py
# Description  : 이티보드 스마트 급식기 코딩 키트(AI)
# Author       : 박은정
# Created Date : 2025.06.10 : PEJ 
# Reference    :
# ******************************************************************************************


#========================================================================================
# import
#========================================================================================
import time                                              # 시간 관련 모듈
import sys                                               # 시스템 관련 라이브러리
from machine import Pin                                  # 핀 관련 모듈
from ETboard.lib.pin_define import *                     # ETboard 핀 관련 모듈
from ETboard.lib.OLED_U8G2 import *                      # ETboard OLED 관련 모듈
from ETboard.lib.servo import Servo                      # ETboard Servo Motor 관련 모듈
from BluetoothSerial import BluetoothSerial              # 블루투스 통신 관련 라이브러리


#===========================================================================================
# global variable
#===========================================================================================
led_red = Pin(D2)                                        # 빨강 LED 핀 지정
led_blue = Pin(D3)                                       # 파랑 LED 핀 지정

button_blue = Pin(D7)                                    # 파랑 버튼 핀 지정

oled = oled_u8g2()                                       # oled 선언

servo = Servo(Pin(D6))                                   # 서보모터 핀 지정

SerialBT = BluetoothSerial()                             # 블루투스 통신 설정

count = 0                                                # 사료 공급 횟수 저장 변수
motor_state = "Off"                                      # 모터 상태를 "Off"로 초기화

ai_result = "background"                                 # AI 결과 값
prev_result = "background"                               # 이전 AI 결과 값

ai_label = {                                             # AI 라벨(ID, 동물)
    0: "background",                                     # AI 결과 값 0: 배경
    1: "dog",                                            # AI 결과 값 1: 개
    2: "giraffe",                                        # AI 결과 값 2: 기린
    3: "chicken",                                        # AI 결과 값 3: 닭
}


#===========================================================================================
def handle_data(msg):                                    # 수신 데이터 처리 함수
#===========================================================================================
    global ai_result

    byte_data = msg                                      # 바이트 문자열
    number = int(byte_data.decode('utf-8'))

    ai_result = ai_label[number]                         # 디코딩 후 정수로 변환


#===========================================================================================
def setup():                                             # 설정 함수
#===========================================================================================
    led_red.init(Pin.OUT)                                # 빨강 LED 출력 모드 설정
    led_blue.init(Pin.OUT)                               # 파랑 LED 출력 모드 설정

    button_blue.init(Pin.IN)                             # 파랑 버튼 입력 모드 설정

    motor_off()                                          # 모터 중지

    print('블루투스 이름 : ' + SerialBT._ble_name)       # 블루투스 이름 출력

    SerialBT.on_received(handle_data)         # 수신받은 데이터를 처리하기 위한 함수 연결


#===========================================================================================
def loop():                                              # 반복 함수
#===========================================================================================

    global count, prev_result                            # 전역 변수 호출

    if not SerialBT.is_connected():                      # 블루투스가 연결되지 않았다면
        print('연결되지 않았습니다.')                    # 쉘에 "연결되지 않았습니다." 출력
        time.sleep(1)
        return

    # 이전 AI 결과 값과 현재 AI 결과 값이 다르면서 결과 값이 개일 경우
    if prev_result != ai_result and ai_result == ai_label[1]:
        food_supply()                                    # 사료 공급 함수 호출
        count += 1                                       # count 1 증가

    prev_result = ai_result                              # 이전 AI 결과 값 갱신

    print("먹이 공급 횟수: ", count)                     # 쉘에 먹이 공급 횟수 출력
    print("AI 결과: ", ai_result)                        # 쉘에 AI 결과 값 출력
    print("-----------------------")

    oled_print()                                         # OLED 출력 함수 호출

    time.sleep(0.1)


#===========================================================================================
def food_supply():                                       # 먹이 공급 함수
#===========================================================================================
    global motor_state                                   # 전역 변수 호출

    motor_state = "On"                                   # 모터 상태 변경
    oled_print()                                         # OLED 출력
    motor_on()                                           # motor_on 함수 호출

    motor_state = "OFF"                                  # 모터 상태 변경
    oled_print()                                         # OLED 출력
    motor_off()                                          # motor_off 함수 호출


#===========================================================================================
def motor_on():                                          # 모터 작동 함수
#===========================================================================================
    servo.write_angle(50)                                # 차단봉 열기

    led_red.value(HIGH)                                  # DC 모터 켜기
    led_blue.value(HIGH)

    time.sleep(1)                                        # 1초간 대기


#===========================================================================================
def motor_off():                                         # 모터 정지 함수
#===========================================================================================

    led_red.value(LOW)                                   # DC 모터 끄기
    led_blue.value(LOW)

    time.sleep(0.6)                                      #  0.6초간 대기

    servo.write_angle(180)                               # 차단봉 닫기


#===========================================================================================
def oled_print():                                        # OLED 출력 함수
#===========================================================================================
    global count, motor_state, ai_result                 # 전역 변수 호출

    count_line = "Count: %d" %(count)                    # count 값 표시 문자열 저장
    motor_line = "Motor: " + motor_state                 # 모터 상태 표시 문자열 저장
    ai_result_line = "AI: " + ai_result                  # 모터 상태 표시 문자열 저장

    oled.clear()                                         # OLED 초기화

    oled.setLine(1, "* Smart Feeder *")                  # OLED 첫 번째 줄 : 시스템 이름
    oled.setLine(2, count_line)                          # OLED 두 번째 줄: 사료 공급 횟수
    oled.setLine(3, motor_line)                          # OLED 세 번째 줄: 모터 상태
    oled.setLine(4, ai_result_line)                      # OLED 세 번째 줄: 모터 상태

    oled.display()                                       # OLED 출력


#===========================================================================================
# start point
#===========================================================================================
if __name__ == "__main__" :
    setup()
    while True :
        loop()


#===========================================================================================
#                                                    
# (주)한국공학기술연구원 http://et.ketri.re.kr       
#
#===========================================================================================
