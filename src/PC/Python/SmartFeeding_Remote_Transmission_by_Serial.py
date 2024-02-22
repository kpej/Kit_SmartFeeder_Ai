import tensorflow.keras
import numpy as np
import cv2
import time
import serial
import serial.tools.list_ports


# 웹캠 선언
camera = cv2.VideoCapture(1)    # 웹캠 첫번째(0)
camera.set(3, 640)               # 웹캠 비율 640 * 480
camera.set(4, 480)

model_path = r"keras_model.h5"  # 학습모델 경로
model = tensorflow.keras.models.load_model(model_path)      # 학습모델 로딩
class_names = open("labels.txt", "r", encoding="UTF-8").readlines()

pre_id = ''
cur_id = ''

def send_etboard(id):
    my_serial.write(str(id).encode())
    print(str(id))

def main():
    global pre_id, cur_id

    while(camera.isOpened()):
        _, image = camera.read()  

        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)       # 웹캠이미지를 224, 224로 사이즈 조정        
        image_normalized = (image.astype(np.float32) / 127.0) - 1         # 정규화        
        image_reshaped = image_normalized.reshape((1, 224, 224, 3))               #

        prediction = model.predict(image_reshaped)                                 # 추론/예측
        cur_id = np.argmax(prediction[0])                                          # 결과
        print(class_names[cur_id], np.max(prediction[0]) * 100, "%")

        if np.max(prediction[0]) > 0.8 and cur_id != pre_id:
            send_etboard(cur_id)
            pre_id = cur_id

        cv2.imshow('camera out', image)

        if cv2.waitKey(100) == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    # ETboard가 연결된 포트와 연결
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "USB-SERIAL CH340" in p.description:
            print(f"{p} 포트에 연결하였습니다.")
            my_serial = serial.Serial(p.device, baudrate=9600, timeout=1.0)
            time.sleep(2)
    main()
    my_serial.close()