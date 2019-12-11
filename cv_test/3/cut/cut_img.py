#!/usr/bin/env python

'''
face detection using haar cascades

USAGE:
    facedetect.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>]
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2

# local modules
# from common import clock, draw_str


def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=3, minSize=(100, 100),
                                     flags=cv2.CASCADE_SCALE_IMAGE)

    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    rects = rects * np.array([1,0.8,1,1.05])
    return rects


def detect_eye(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=3, minSize=(100, 100),
                                     flags=cv2.CASCADE_SCALE_IMAGE)

    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects


def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)


if __name__ == '__main__':
    # print(__doc__)

    cascade_fn = "haarcascade_frontalface_alt.xml"
    nested_fn = "haarcascade_eye.xml"

    cascade = cv2.CascadeClassifier(cascade_fn)
    nested = cv2.CascadeClassifier(nested_fn)

    # while True:
    # img = cv2.imread('../i.jpg')
    img = cv2.imread('q.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # t = clock()
    rects = detect(gray, cascade)

    x1,y1,x2,y2 = rects[0]
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    cv2.imwrite('t_t.jpg', img[y1:y2, x1:x2])

    vis = img.copy()
    draw_rects(vis, rects, (0, 255, 0))
    if not nested.empty():
        for x1, y1, x2, y2 in rects:
            x1 = int(x1)
            x2 = int(x2)
            y1 = int(y1)
            y2 = int(y2)
            roi = gray[y1:y2, x1:x2]
            vis_roi = vis[y1:y2, x1:x2]
            subrects = detect_eye(roi.copy(), nested)
            draw_rects(vis_roi, subrects, (255, 0, 0))
    # dt = clock() - t

    # draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
    cv2.imwrite('t.jpg', vis)
        # cv2.imshow('facedetect', vis)

        # if cv2.waitKey(5) == 27:
        #     break
    # cv2.destroyAllWindows()
