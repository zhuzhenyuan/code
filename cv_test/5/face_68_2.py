import cv2
import dlib

cap=cv2.VideoCapture(0)

predictor_path = "shape_predictor_68_face_landmarks.dat"

predictor = dlib.shape_predictor(predictor_path)
detector = dlib.get_frontal_face_detector()

while True:
    _,frame=cap.read()
    frame = cv2.flip(frame, 1)
    # Ask the detector to find the bounding boxes of each face. The 1 in the
    # second argument indicates that we should upsample the image 1 time. This
    # will make everything bigger and allow us to detect more faces.
    dets = detector(frame, 1)
    for det in dets:
        # Get the landmarks/parts for the face in box d.
        shape = predictor(frame, det)
        for p in shape.parts():
            cv2.circle(frame, (p.x, p.y), 3, (0,0,0), -1)
    cv2.imshow('video',frame)
    if cv2.waitKey(1)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()