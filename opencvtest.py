import cv2
import numpy as np


while True:
    img = cv2.imread('image4.png')
    frame = img

    # Locate points of the documents
    # or object which you want to transform
    pts1 = np.float32([[388, 350], [110, 560],
                       [920, 400], [1075, 650]])

    pts2 = np.float32([[0, 0], [0, 800],
                       [800, 0], [800, 800]])

    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(frame, matrix, (800, 800))

    # Wrap the transformed image
    cv2.imshow('frame', frame)  # Initial Capture
    cv2.imshow('frame1', result)  # Transformed Capture

    if cv2.waitKey(24) == 27:
        break
cv2.destroyAllWindows()
