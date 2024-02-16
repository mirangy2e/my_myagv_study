import cv2
import numpy as np

def find_contours_in_white(image):
    # black hsv range
    lower_black = np.array([86, 0, 0])
    upper_black = np.array([179, 255, 255])


    # 지정한 흰색 영역만 추출
    white_mask = cv2.inRange(image, lower_black, upper_black)
    white_area = cv2.bitwise_and(image, image, mask=white_mask)

    gray_image = cv2.cvtColor(white_area, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

    return image

# cap = cv2.VideoCapture('testVideo.mp4')
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 하단의 1/5 부분 추출
    height, width, _ = frame.shape
    roi_height = int(height / 5)
    roi = frame[4 * roi_height:height, :]

    # 흰색 영역의 윤곽선을 찾아 이미지에 표시
    result_frame = find_contours_in_white(roi)

    # 전체 이미지에 결과 적용
    frame[4 * roi_height:height, :] = result_frame[:, :]

    cv2.imshow('Contours in White', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()