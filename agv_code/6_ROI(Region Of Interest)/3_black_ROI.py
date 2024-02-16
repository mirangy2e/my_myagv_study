import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # 이미지를 hsv로 변환 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # black hsv range
    lower_black = np.array([86, 0, 0])
    upper_black = np.array([179, 255, 255])

    # HSV 
    black_mask = cv2.inRange(hsv, lower_black, upper_black)

    # 검은색으로 출력 
    black_result = cv2.bitwise_and(frame, frame, mask=black_mask)
    
    ############### ROI ######################
    height, width = frame.shape[:2]
    roi_top = height * 2 // 3 # 상단 경계 
    roi_bottom = height # 하단 경계 
    roi_left = 0 # 왼쪽 경계 
    roi_right = width # 오른쪽 경계 
    roi = black_result[roi_top:roi_bottom, roi_left:roi_right]
    
    # 결과 이미지 표시
    cv2.imshow("Original", frame)
    cv2.imshow("White", black_result)
    cv2.imshow("ROI", roi)

    # 'q' 키 누르면 종료 
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cv2.release()
cv2.destroyAllWindows()
