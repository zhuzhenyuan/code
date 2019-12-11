# -*- coding: utf-8 -*-
# @Time    : 2017/7/13 下午4:00
# @Author  : play4fun
# @File    : 37.2-对ORB描述符进行蛮力匹配.py
# @Software: PyCharm

"""
37.2-对ORB描述符进行蛮力匹配.py:
匹配器对象是什么
matches = bf.match(des1, des2) 返回值是一个 DMatch对象列表
DMatch 对 具有下列属性
• DMatch.distance - 描述符之间的距离。越小越好。
• DMatch.trainIdx - 目标图像中描述符的索引。
• DMatch.queryIdx - 查询图像中描述符的索引。
• DMatch.imgIdx - 目标图像的索引。
"""


import numpy as np
import cv2
import os


def filter_data(matches):
    try:
        # 筛选 当描述子之间的距离大于两倍的最小距离时,即认为匹配有误.但有时候最小距离会非常小,设置一个经验值30作为下限
        good_matches = []
        for i in matches:
            if int(i) <= max(2*int(matches[0]), 60):
                good_matches.append(i)
        return good_matches
    except:
        return []


def get_array(matches, num):
    # Sort them in the order of their distance.
    matches = sorted(matches, key=lambda x: x.distance)
    # 获取距离值
    test = []
    # for i in good_matches:
    for i in matches[:num]:
        test.append(i.distance)
    test = np.array(test)
    return test


# 计算一条记录的平均值
def analysis_3(value):

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


def get_hist_value(img1, img2):
    try:
    # img1 = cv2.imread(query_image, 0)  # queryImage
    # img2 = cv2.imread(train_image, 0)  # trainImage

    # Initiate ORB detector  获取值 orb 对象
    # orb = cv2.ORB_create()
    # find the keypoints and descriptors with ORB  计算特征
        hist1 = cv2.calcHist([img1],
                            [0],  # 使用的通道
                            None,  # 没有使用mask
                            [256],  # HistSize
                            [0.0, 255.0])  # 直方图柱的范围
        hist2 = cv2.calcHist([img2],
                            [0],  # 使用的通道
                            None,  # 没有使用mask
                            [256],  # HistSize
                            [0.0, 255.0])  # 直方图柱的范围
        a = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)

        return  a

        # create BFMatcher object  获取 BF 对象
        # bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        # Match descriptors.  进行匹配
        # matches = bf.match(des1, des2)
        # pp = []
        # for i in matches:
        #     pp.append(i.distance)
        # pp.sort()
        # print pp
        # return "匹配个数：" + str(len(matches))
        # return pp
    except:
        print "-1"
        return -1


def get_result(src_img_path, dst_path):
    count_is = 0
    count_no = 0

    dst_img_list = os.listdir(dst_path)

    img1 = cv2.imread(src_img_path, 0)
    img1 = cv2.equalizeHist(img1)

    for dst_img in dst_img_list:
        try:
            img2 = cv2.imread(dst_path+dst_img, 0)
            img2 = cv2.equalizeHist(img2)
            pp = get_hist_value(img1, img2)
            # value = analysis_3(pp)
            # print "a: " + str(pp)
            if pp < 0.8:
                result = "是, 判定为同一个人"
                count_is += 1
            else:
                result = "否,判定为不同的人"
                count_no += 1
            print "value== %s \t 小于0.5？< %s >" % ( str(pp), result)
        except:
            continue
    # print "is: %d   no: %d" % (count_is, count_no)
    return count_is, count_no


if __name__ == "__main__":
    count_is = 0
    count_no = 0

    # name_list = ["a", "b", "c", "d", "e", "f", "g"]
    # name_list = ["h", "i"]
    # name_list = ["i"]
    name_list = [x for x in xrange(1, 65)]
    # name_list = [33]
    for name in name_list:
        # query_image = "./test_data/%s.jpg" % name

        src_img_path = './test_data/src_app/%s/' % name
        dst_img_path = './test_data/dst_app/%s/' % name


        src_img_path_list = os.listdir(src_img_path)

        a, b = get_result(src_img_path+src_img_path_list[0], dst_img_path)
        count_is += a
        count_no += b

    print "result --> is: %d   no: %d" % (count_is, count_no)