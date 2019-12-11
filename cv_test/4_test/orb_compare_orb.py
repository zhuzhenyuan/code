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

    # 筛选 当描述子之间的距离大于两倍的最小距离时,即认为匹配有误.但有时候最小距离会非常小,设置一个经验值30作为下限
    good_matches = []
    for i in matches:
        if i.distance <= max(2*matches[0].distance, 30):
            good_matches.append(i)
    return good_matches


def calc_fangcha(narray):
    # N = len(narray)
    # sum1 = narray.sum()
    # narray2 = narray * narray
    # sum2 = narray2.sum()
    # mean = sum1 / N
    # var = sum2 / N - mean ** 2
    var = np.cov(narray)
    var = np.sqrt(var)
    return var


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


def get_orb_value(img1, train_image):
    # img1 = cv2.imread(query_image, 0)  # queryImage
    img2 = cv2.imread(train_image, 0)  # trainImage

    # Initiate ORB detector  获取值 orb 对象
    orb = cv2.ORB_create()
    # find the keypoints and descriptors with ORB  计算特征
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    try:
        print "des1*********" + str(len(des1))
        print "des2*********" + str(len(des2))
        # create BFMatcher object  获取 BF 对象
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        # Match descriptors.  进行匹配
        matches = bf.match(des1, des2)
        print "matches*********" + str(len(matches))
        pp = []
        for i in matches:
            pp.append(i.distance)
        pp.sort()
        print pp
        # return "匹配个数：" + str(len(matches))
        return str(pp)

        # value = calc_fangcha(test)
        # value = cv2.norm(test, normType=cv2.NORM_L2)
        # print value
        # return value
    except:
        print "-1"
        return -1


def get_result(img1, file_name, img_path):
    try:
        file_result = open(file_name, 'w')
        c1 = 0

        img_dir_list = os.listdir(img_path)
        for img_dir in img_dir_list:
            value = get_orb_value(img1, img_path + img_dir)
            file_result.write(str(value) + "\n")
            print "%s:%s" % (str(file_name), str(c1))
            c1 += 1
        file_result.close()
    except:
        pass


if __name__ == "__main__":

    # name = "zzy"
    # name = "nnh"
    # name = "xxp"
    # name = "yh"
    # name = "ym"
    # name = "zch"

    name_list = ["zzy", "nnh", "xxp", "yh", "ym", "zch"]
    name_list = ["zff"]

    for name in name_list:
        query_image = "./test_data/%s.jpg" % name

        img1 = cv2.imread(query_image, 0)  # queryImage

        get_result(img1, './result/%s_cmp_zff.txt' % name, "./test_data/dst/zff/")
        get_result(img1, './result/%s_cmp_zzy.txt' % name, "./test_data/dst/zzy/")
        get_result(img1, './result/%s_cmp_yh.txt' % name, "./test_data/dst/yh/")
        get_result(img1, './result/%s_cmp_ym.txt' % name, "./test_data/dst/ym/")
        get_result(img1, './result/%s_cmp_xxp.txt' % name, "./test_data/dst/xxp/")
        get_result(img1, './result/%s_cmp_nnh.txt' % name, "./test_data/dst/nnh/")
        get_result(img1, './result/%s_cmp_zch.txt' % name, "./test_data/dst/zch/")
        get_result(img1, './result/%s_cmp_all_img.txt' % name, "./test_data/dst/all_img/")

