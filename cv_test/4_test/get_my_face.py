# -*- coding: utf-8 -*-


'''
自己切出脸，160*160
'''

# Python 2/3 compatibility
# from __future__ import print_function

import numpy as np
import cv2
import os

# local modules
# from common import clock, draw_str


def detect(img, cascade):
    rects = []
    try:
        rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=3, minSize=(50, 50),
                                         flags=cv2.CASCADE_SCALE_IMAGE)

        if len(rects) == 0:
            return []
        rects[:,2:] += rects[:,:2]
        rects = rects * np.array([1,0.8,1,1.05])
    except:
        pass
    return rects


def detect_eye(img, cascade):
    rects = []
    try:
        rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=3, minSize=(50, 50),
                                         flags=cv2.CASCADE_SCALE_IMAGE)

        if len(rects) == 0:
            return []
        rects[:,2:] += rects[:,:2]
    except:
        pass
    return rects


def get_face_160(src_dir, dst_dir, img_list):
    try:
        # print(__doc__)

        cascade_fn = "haarcascade_frontalface_alt.xml"
        nested_fn = "haarcascade_lefteye_2splits.xml"

        cascade = cv2.CascadeClassifier(cascade_fn)
        nested = cv2.CascadeClassifier(nested_fn)

        count = 0
        for img_dir in img_list:
            img = cv2.imread(src_dir + img_dir)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)

            rects = detect(gray, cascade)

            if not nested.empty():
                for x1, y1, x2, y2 in rects:
                    x1 = int(x1)
                    x2 = int(x2)
                    y1 = int(y1)
                    y2 = int(y2)
                    roi = gray[y1:y2, x1:x2]
                    subrects = detect_eye(roi.copy(), nested)
                    if len(rects) and len(subrects) and rects is not None and subrects is not None:
                        x1, y1, x2, y2 = rects[0]
                        x1 = int(x1)
                        x2 = int(x2)
                        y1 = int(y1)
                        y2 = int(y2)
                        tmp_img = cv2.resize(img[y1:y2, x1:x2], (160, 160))
                        cv2.imwrite(dst_dir + img_dir, tmp_img)
                        print "%s:%s" % (src_dir, str(count))
                        count += 1
                        break

        print "**************"
        print "all is: " + str(count)
        print "**************"

    except:
        pass


def get_data(src_path, dst_path):
    try:
        dir_list = os.listdir(src_path)
        get_face_160(src_path, dst_path, dir_list)
    except:
        pass


if __name__ == "__main__":
    try:

        get_data("./test_data/src/zff_src/", "./test_data/dst/zff/")
        # get_data("./test_data/src/xxp_src/", "./test_data/dst/xxp/")
        # get_data("./test_data/src/zzy_src/", "./test_data/dst/zzy/")
        # get_data("./test_data/src/yh_src/", "./test_data/dst/yh/")
        # get_data("./test_data/src/ym_src/", "./test_data/dst/ym/")
        # get_data("./test_data/src/zch_src/", "./test_data/dst/zch/")
        # get_data("./test_data/src/nnh_src/", "./test_data/dst/nnh/")
    except:
        pass