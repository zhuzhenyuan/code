# -*- coding: utf-8 -*-
import numpy as np
import cv2
import os



def detect(img, cascade):
    rects = []
    try:
        rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=3, minSize=(100, 100),
                                         flags=cv2.CASCADE_SCALE_IMAGE)

        if len(rects) == 0:
            return []
        rects[:,2:] += rects[:,:2]
        # rects = rects * np.array([0.9,0.9,1.02,1.02])
        # rects = rects * np.array([1,1,0.94,0.94])
        # rects = rects * np.array([1.08,1.08,0.94,0.94])
    except:
        pass
    return rects


def detect_eye(img, cascade):
    rects = []
    try:
        rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=3, minSize=(5, 5),
                                         flags=cv2.CASCADE_SCALE_IMAGE)

        if len(rects) == 0:
            return []
        rects[:,2:] += rects[:,:2]
    except:
        pass
    return rects


def get_face_160(frame):
    try:
        cascade_fn = "haarcascade_frontalface_alt.xml"
        nested_fn = "haarcascade_lefteye_2splits.xml"

        cascade = cv2.CascadeClassifier(cascade_fn)
        nested = cv2.CascadeClassifier(nested_fn)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        # x = cv2.Sobel(gray, cv2.CV_16S,1,0)
        # y = cv2.Sobel(gray, cv2.CV_16S,0,1)
        # absX = cv2.convertScaleAbs(x)  # 转回uint8
        # absY = cv2.convertScaleAbs(y)
        # gray = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)

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
                    # x1, y1, x2, y2 = rects[0]
                    # x1 = int(x1)
                    # x2 = int(x2)
                    # y1 = int(y1)
                    # y2 = int(y2)
                    # tmp_img = cv2.resize(roi, (320, 320))
                    # return tmp_img
                    return roi
    except:
        pass


def get_orb_value(img1, img2):
    surf = cv2.SURF(1000)
    kp1, des1 = surf.detectAndCompute(img1, None)
    kp2, des2 = surf.detectAndCompute(img2, None)
    try:
        if len(des1) and len(des2) and des1 is not None and des2 is not None:
            bf = cv2.BFMatcher(cv2.NORM_L2)
            matches = bf.knnMatch(des1, des2, k=2)
            pp = []
            for m, n in matches:
                # print str(m.distance) + "" + str(n.distance)
                # if m.distance < 0.95 * n.distance:
                #     pp.append(m.distance)
                pp.append(m.distance)
                # pp.append(m)
            # print "norm_value:  " + str()
            # pp.sort()
            # print pp
            return cv2.norm(np.array(pp), normType=cv2.NORM_L2)
    except:
        print "-1"
        os.remove("./tmp.jpg")


def filter_data(matches):
    try:
        # 筛选 当描述子之间的距离大于两倍的最小距离时,即认为匹配有误.但有时候最小距离会非常小,设置一个经验值30作为下限
        good_matches = []
        for i in matches:
            if float(i) <= max(2*float(matches[0]), 0.2):
                good_matches.append(i)
        return good_matches
    except:
        return []


# 计算一条记录的平均值
def analysis_3(value):
    try:
        if value:
            value = filter_data(value)
            # num_sum = 0
            # for num in value:
            #     if float(num) <= 0.2:
            #         num_sum += 1
            # return num_sum * 1.0 / len(value)
            num_sum = 0
            for num in value:
                num_sum += float(num)
            return num_sum * 1.0 / len(value)
        else:
            return -1.0
    except:
        pass


if __name__ == "__main__":
    try:
        count = 0
        cap = cv2.VideoCapture(0)
        img_path = "./tmp.jpg"
        while 1:
            # 得到每一帧图像
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)

            # 高斯模糊，消除噪声
            # frame1 = cv2.GaussianBlur(frame, (3, 3), 0)

            frame_160_gray = np.array([])
            frame_160_gray = get_face_160(frame)
            # print frame_160_gray
            if frame_160_gray is not None and len(frame_160_gray):
                if not os.path.exists(img_path):
                    cv2.imwrite(img_path, frame_160_gray)
                tmp_jpg = cv2.imread(img_path, 0)

                frame_160_gray = cv2.equalizeHist(frame_160_gray)
                tmp_jpg = cv2.equalizeHist(tmp_jpg)

                # orb
                pp = get_orb_value(frame_160_gray, tmp_jpg)
                print "norm_value:  " + str(pp)
                # value = analysis_3(pp)
                value = pp
                vvvv = 6
                if value <= vvvv:
                    result = "是, 判定为同一个人"
                    print result
                else:
                    result = "否,判定为不同的人"
                    cv2.imwrite(img_path, frame_160_gray)
                    print "@%s@已经替换图像**********************************************************************************************************" % str(value)
                print "value== %s \t 大于%s？< %s >" % (str(value),str(vvvv), result)

                count += 1
            # 显示每一帧图像
            cv2.imshow("capture", frame)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # 延时 30 ms，任意键退出
            # if(cv2.waitKey(30) >= 0):
            #     break

        cap.release()
        cv2.destroyAllWindows()

    except:
        pass
