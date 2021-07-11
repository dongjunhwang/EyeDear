"""
This Python Program Set Up Your Pupil direction Threshold.
Pupil Threshold save in text file.
"""

import cv2
from gaze_tracking import GazeTracking
from imutils import face_utils

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
setCount = 0

direction = ["Open", "Close"]
direction_key = ["V", "B"]
direction_index = 0

IMG_SIZE = (34,26)

while webcam.isOpened():
    _, frame = webcam.read()
    gaze.refresh(frame)
    

    text = "Please "+ direction[direction_index] + " your eyes" 
    text_push = "Push Button " + direction_key[direction_index] + " To Save photo!!"

    cv2.putText(frame, text, (20, 60), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)
    cv2.putText(frame, text_push, (20, 130), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
    cv2.imshow("SetUp", frame)
    
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #faces = gaze._face_detector(gray)
    #for face in faces:
    #    shapes = gaze._predictor(gray, face)
    #    shapes = face_utils.shape_to_np(shapes)
    #    eye_img_l, eye_rect_l = gaze.eye_left.crop_eye(gray, eye_points=shapes[36:42])
    #cv2.rectangle(frame, pt1=tuple(eye_rect_l[0:2]), pt2=tuple(eye_rect_l[2:4]), color=(255,255,255), thickness=2)
    faces = gaze._face_detector(frame)
    #save open img
    if cv2.waitKey(1) == ord('v') and direction_index == 0: 
        if setCount > 10:
            direction_index += 1
            setCount = 0
        if gaze.pupils_located:
            landmarks = gaze._predictor(frame, faces[0])
            landmarks = face_utils.shape_to_np(landmarks)
            eye_img_l, eye_rect_l = gaze.eye_left.crop_eye(frame, eye_points=landmarks[36:42])
            eye_img_r, eye_rect_r = gaze.eye_left.crop_eye(frame, eye_points=landmarks[42:48])
            eye_img_l = cv2.resize(eye_img_l, dsize=IMG_SIZE)
            eye_img_r = cv2.resize(eye_img_r, dsize=IMG_SIZE)
            cv2.imwrite('./img/open Left %d .jpg' %setCount ,eye_img_l, params=[cv2.IMWRITE_JPEG_QUALITY,100])
            cv2.imwrite('./img/open Right %d .jpg' %setCount ,eye_img_r, params=[cv2.IMWRITE_JPEG_QUALITY,100])
            print(setCount, direction[direction_index], ' save img')
            setCount += 1
    #save close img
    elif cv2.waitKey(1) == ord('b') and direction_index == 1:
        
        if setCount > 10:
            direction_index += 1
            setCount = 0
            
        if not gaze.pupils_located:
            landmarks = gaze._predictor(frame, faces[0])
            landmarks = face_utils.shape_to_np(landmarks)
            eye_img_l, eye_rect_l = gaze.eye_left.crop_eye(frame, eye_points=landmarks[36:42])
            eye_img_r, eye_rect_r = gaze.eye_left.crop_eye(frame, eye_points=landmarks[42:48])
            eye_img_l = cv2.resize(eye_img_l, dsize=IMG_SIZE)
            eye_img_r = cv2.resize(eye_img_r, dsize=IMG_SIZE)
            cv2.imwrite('./img/close Left %d .jpg' %setCount ,eye_img_l, params=[cv2.IMWRITE_JPEG_QUALITY,100])
            cv2.imwrite('./img/close Right %d .jpg' %setCount ,eye_img_r, params=[cv2.IMWRITE_JPEG_QUALITY,100])
            print(setCount, direction[direction_index], ' save img')
            setCount += 1
    
    if direction_index == 2 :
        if cv2.waitKey(1) == ord('q'):
            break

webcam.release()
cv2.destroyAllWindows()