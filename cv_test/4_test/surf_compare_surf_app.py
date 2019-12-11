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
            if float(i) <= max(2*float(matches[0]), 0.2):
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
        # num_sum = 0
        # for num in value:
        #     if float(num) <= 0.3:
        #         num_sum += 1
        # return num_sum * 1.0 / len(value)
        num_sum = 0
        for num in value:
            num_sum += float(num)
        return num_sum * 1.0 / len(value)
    else:
        return -1.0
        # try:
        #     if num_sum * 1.0 / len(value) <= 52.245:
        #         pass
        # except:
        #     pass


def get_orb_value(img1, img2):
    surf = cv2.SURF(1000)
    # surf = cv2.xfeatures2d.SURF_create()
    kp1, des1 = surf.detectAndCompute(img1, None)
    kp2, des2 = surf.detectAndCompute(img2, None)
    try:
        bf = cv2.BFMatcher(cv2.NORM_L2)
        # 11111111111111111
        # matches = bf.knnMatch(des1, des2, k=1)
        # pp = []
        # for i in matches:
        #     for a in i:
        #         pp.append(a.distance)
        # pp.sort()
        # 222222222222222222
        matches = bf.knnMatch(des1, des2, k=2)
        pp = []
        for m, n in matches:
            # print str(m.distance) + "" + str(n.distance)
            # if m.distance < 0.90*n.distance:
            #     pp.append(m.distance)
            pp.append(m.distance)
        pp.sort()
        # print pp
        return pp
    except:
        # print "-1"
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
            pp = get_orb_value(img1, img2)
            value = analysis_3(pp)
            vvv = 0.5
            # if value < 52.145:
            if value <= vvv:
                result = "是, 判定为同一个人"
                count_is += 1
            else:
                result = "否,判定为不同的人"
                count_no += 1
            print "value== %s \t 小于%s？< %s >" % ( str(value), vvv, result)
        except:
            continue
    # print "is: %d   no: %d" % (count_is, count_no)
    return count_is, count_no


if __name__ == "__main__":
    print cv2.__version__
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