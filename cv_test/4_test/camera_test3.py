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
        rects = rects * np.array([0.9,0.9,1.02,1.02])
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

    # Initiate ORB detector  获取值 orb 对象
    orb = cv2.ORB_create()
    # find the keypoints and descriptors with ORB  计算特征
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    try:
        if len(des1) and len(des2) and des1 is not None and des2 is not None:
            # print "des1*********" + str(len(des1))
            # print "des2*********" + str(len(des2))
            # create BFMatcher object  获取 BF 对象
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            # Match descriptors.  进行匹配
            matches = bf.match(des1, des2)
            # print "matches*********" + str(len(matches))
            pp = []
            for i in matches:
                pp.append(i.distance)
            pp.sort()
            return pp
            # print pp
            # return "匹配个数：" + str(len(matches))
            # return str(pp)

            # value = calc_fangcha(test)
            # value = cv2.norm(test, normType=cv2.NORM_L2)
            # print value
            # return value
    except:
        print("-1")
        os.remove("./tmp.jpg")
        # return -1


def filter_data(matches):
    try:
        # 筛选 当描述子之间的距离大于两倍的最小距离时,即认为匹配有误.但有时候最小距离会非常小,设置一个经验值30作为下限
        good_matches = []
        for i in matches:
            if float(i) <= max(2*float(matches[0]), 40):
                good_matches.append(i)
        return good_matches
    except:
        return []


# 计算一条记录的平均值
def analysis_3(value):
    try:
        if value:
            value = filter_data(value)
            num_sum = 0

            for num in value:
                num_sum += int(num)
            return num_sum * 1.0 / len(value)
        else:
            return -1.0
            # try:
            #     if num_sum * 1.0 / len(value) <= 52.245:
            #         pass
            # except:
            #     pass
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

                value = analysis_3(pp)
                vvvv = 42
                # if value < 52.245:
                # if value < 53.795:
                if value <= vvvv:
                    result = "是, 判定为同一个人"
                    print(result)
                else:
                    result = "否,判定为不同的人"
                    cv2.imwrite(img_path, frame_160_gray)
                    print("@%s@已经替换图像**********************************************************************************************************" % str(value))
                    # print "@%s@" % str(value)
                # print "value== %s \t 小于52.245？< %s >" % (str(value), result)
                # print "value== %s \t 小于54.201？< %s >" % (str(value), result)
                print("value== %s \t 小于%s？< %s >" % (str(value),str(vvvv), result))

                # if value <= 36:
                #     print value
                #     print "同一个人" + str(count)
                # else:
                #     print value
                #     print "不同的人" + str(count)


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
