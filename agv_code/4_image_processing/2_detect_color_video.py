import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 흰색 영역 검출
    lower_white = np.array([30, 40, 200], dtype=np.uint8)
    upper_white = np.array([255, 255, 255], dtype=np.uint8)
    white_mask = cv2.inRange(frame, lower_white, upper_white)

    # 흰색 영역 이외는 검은색으로 출력 
    white_result = cv2.bitwise_and(frame, frame, mask=white_mask)
    
    # 결과 이미지 표시
    cv2.imshow("Original", frame)
    cv2.imshow("White", white_result)

    # 'q' 키 누르면 종료 
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
