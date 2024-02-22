# import
import time
import sys
from machine import UART, Pin, PWM
from ETboard.lib.pin_define import *
from ETboard.lib.OLED_U8G2 import *


# global variable
led_red = Pin(D2)                         # 빨강 LED 핀 지정
led_blue = Pin(D3)                        # 파랑 LED 핀 지정
led_green = Pin(D4)                       # 초록 LED 핀 지정
led_yellow = Pin(D5)                      # 노랑 LED 핀 지정

button_blue = Pin(D7)                     # 파랑 버튼 핀 지정
button_green = Pin(D8)                    # 초록 버튼 핀 지정

oled = oled_u8g2()

mode = 0                                  # 0: AI / 1: Timer
mode_str = 'AI'

supply_time = 10                          # 사료 공급 타이머 시간
now_time = 0                              # 현재 시간
pre_time = 0                              # 마지막 사료 공급 시간
last_supply_time = ''

count = 0                                 # 모이 공급 횟수

# 객체 확인을 위한 변수 선언
class_id = 3
class_names = ['dog', 'chicken', 'giraffe', 'none']

uart = UART(1)              # 시리얼 통신 포트 지정

# setup
def setup():
    led_red.init(Pin.OUT)                 # 빨강 LED 출력모드 설정
    led_blue.init(Pin.OUT)                # 파랑 LED 출력모드 설정
    led_green.init(Pin.OUT)               # 초록 LED 출력모드 설정
    led_yellow.init(Pin.OUT)              # 노랑 LED 출력모드 설정

    button_blue.init(Pin.IN)              # 파랑 버튼 입력모드 설정
    button_green.init(Pin.IN)             # 초록 버튼 입력모드 설정
    
    uart.init(baudrate=115200,            # 시리얼 통신 속도 지정
              timeout=1000,               # 최대 1초만 수신 대기
              tx=1, rx=3)                 # 이티보드 통신 핀 번호 지정


# main loop
def loop():
    global class_id, mode, mode_str, pre_time, now_time, count, last_supply_time

    receive()                            # PC에서 보낸 시리얼 통신을 읽어오는 함수 호출

    button_blue_status = button_blue.value()
    button_green_status = button_green.value()

    led_red.value(LOW)                    # DC 모터 중지
    led_blue.value(LOW)

    led_green.value(LOW)                  # 진동 모터 중지
    led_yellow.value(LOW)

    # 파랑 버튼이 눌리면 타이머 모드로 변경
    if button_blue_status == LOW:
        print("모드 변경: 타이머")
        mode = 1
        mode_str = "Timer"

        # 사료 공급 횟수가 0이라면 마지막 공급 시간을 현재 시간으로 초기화
        if count == 0:
            pre_time = int(round(time.time()))
    # 초록 버튼이 눌리면 AI 모드로 변경
    elif button_green_status == LOW:
        print("모드 변경: AI")
        mode = 0
        mode_str = "AI"

    # 모드가 AI 모드일 시
    if mode == 0:
        if class_id == 0:
            motor_work()
        print("모드: AI 모드")
        print("객체:", class_names[class_id])

    # 모드가 타이머 모드일 시
    if mode == True:
        # 현재 시간을 저장
        now_time = int(round(time.time()))
        # 타이머 종료 시
        if now_time - pre_time > supply_time:
            motor_work()
        print("모드: 타이머 모드")
        print("타이머:", now_time - pre_time, "초")

    print("횟수:", count)
    print("마지막 공급 시간:", last_supply_time)
    print("-----------------------------------");

    oled.clear()

    mode_line = "Mode: %s" %(mode_str)
    count_line = "Count: %d" %(count)
    object_line = "Object: %s" %(class_names[class_id])

    oled.setLine(1, "* Smart Feeder *")
    oled.setLine(2, mode_line)
    oled.setLine(3, count_line)
    oled.setLine(4, object_line)
    oled.display()

    time.sleep(0.07)


# 사료 공급
def supply():
    global pre_time, count, last_supply_time

    led_red.value(HIGH)           # DC 모터 작동
    led_blue.value(HIGH)

    led_green.value(HIGH)         # 진동 모터 작동
    led_yellow.value(HIGH)

    time.sleep(3)

    count += 1                                # 사료 공급 횟수 1 증가
    pre_time = int(round(time.time()))        # 사료 공급 시간 저장
    now = time.localtime()                    # 현재 시간 저장
    # 현재 시간과 분을 형식을 지정하여 저장
    last_supply_time = "{:02d}/{:02d}/{:02d} {:02d}:{:02d}".format(now[0], now[1], now[2], now[3], now[4])


# receive
def receive():
    global class_id

    msg = uart.readline()             # 메시지를 1줄씩 읽음
    if msg is None:                   # 어떤 메시지도 받지 못하면
        led_yellow.value(HIGH)        # 노랑 LED 깜밖임
        time.sleep(0.5)      
        led_yellow.value(LOW)      
        time.sleep(0.5)      
        return

    class_id = int(msg.rstrip())


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