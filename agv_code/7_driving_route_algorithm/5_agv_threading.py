import cv2
import numpy as np
from pymycobot.myagv import MyAgv
import threading
import time

agv = MyAgv("/dev/ttyAMA2", 115200)

# AGV를 제어하는데 사용될 변수
agv_lock = threading.Lock()
agv_stopped = False

def stop_agv():
    global agv_stopped
    agv_lock.acquire()
    agv_stopped = True
    agv.stop()
    agv_lock.release()

def process_frame(frame):
    global agv_stopped

    height, width, _ = frame.shape
    roi_height = int(height / 3)
    roi_top = height - roi_height
    roi = frame[roi_top:, :]

    cv2.line(roi, (width // 2, 0), (width // 2, roi_height), (0, 255, 0), 2)

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # 빨간색 범위 설정
    lower_red1 = np.array([0, 100, 100], dtype=np.uint8)
    upper_red1 = np.array([10, 255, 255], dtype=np.uint8)
    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    
    lower_red2 = np.array([160, 100, 100], dtype=np.uint8)
    upper_red2 = np.array([180, 255, 255], dtype=np.uint8)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # 빨간색을 합친 마스크
    red_combined_mask = red_mask1 | red_mask2
    
    # 노란색 범위 설정
    lower_yellow = np.array([20, 100, 100], dtype=np.uint8)
    upper_yellow = np.array([30, 255, 255], dtype=np.uint8)
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # 노란색을 합친 마스크
    yellow_combined_mask = yellow_mask
    
    # 빨간색 또는 노란색을 합친 영상
    result_image = cv2.bitwise_and(roi, roi, mask=red_combined_mask | yellow_combined_mask)

    gray = cv2.cvtColor(result_image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) >= 1:
        max_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(roi, [max_contour], -1, (0, 255, 0), 2)

        M = cv2.moments(max_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            
            center_line = width // 2
            if cx < center_line - 50 or cx > center_line + 50:
                stop_agv()
                return "STOP"

    return None

def camera_thread():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera error")
            break

        if not agv_stopped:
            result = process_frame(frame)
            if result and result == "STOP":
                print(result)

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# 10초 동안 AGV를 멈추는 스레드
def stop_agv_thread():
    global agv_stopped
    time.sleep(10)
    agv_lock.acquire()
    agv_stopped = False
    agv_lock.release()

# 메인 스레드에서 카메라 스레드와 AGV 정지 스레드를 시작
camera_thread = threading.Thread(target=camera_thread)
stop_agv_thread = threading.Thread(target=stop_agv_thread)

camera_thread.start()
stop_agv_thread.start()

camera_thread.join()
stop_agv_thread.join()