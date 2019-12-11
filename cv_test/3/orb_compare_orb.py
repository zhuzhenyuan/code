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
import matplotlib.pyplot as plt

# img1 = cv2.imread('a.jpg', 0)  # queryImage
img1 = cv2.imread('c.jpg', 0)  # queryImage
# img1 = cv2.imread('c.jpg', 0)  # queryImage
# img1 = cv2.imread('d.jpg', 0)  # queryImage
# img1 = cv2.imread('e.jpg', 0)  # queryImage
# img1 = cv2.imread('f.jpg', 0)  # queryImage
# img1 = cv2.imread('g.jpg', 0)  # queryImage
# img1 = cv2.imread('h.jpg', 0)  # queryImage
# img1 = cv2.imread('i.jpg', 0)  # queryImage
# img2 = cv2.imread('a.jpg', 0)  # trainImage
# img2 = cv2.imread('b.jpg', 0)  # trainImage
# img2 = cv2.imread('c.jpg', 0)  # trainImage
# img2 = cv2.imread('d.jpg', 0)  # trainImage
# img2 = cv2.imread('e.jpg', 0)  # trainImage
# img2 = cv2.imread('f.jpg', 0)  # trainImage
# img2 = cv2.imread('g.jpg', 0)  # trainImage
# img2 = cv2.imread('h.jpg', 0)  # trainImage
img2 = cv2.imread('b.jpg', 0)  # trainImage

# Initiate ORB detector
orb = cv2.ORB_create()
# find the keypoints and descriptors with ORB
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# print cv2.norm(des1, des2)
# print cv2.norm(des1[:20])
# print cv2.norm(des1[:3], des2[:3])

# print len(kp1)
# print len(des1)
# print "-------------"
# print len(kp2)
# print len(des2)

# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
# Match descriptors.
matches = bf.match(des1, des2)


# Sort them in the order of their distance.
matches = sorted(matches, key=lambda x: x.distance)

# for i in matches[:30]:
# for i in matches:
#     print i.distance
    # print i.trainIdx
    # print i.queryIdx
    # print i.imgIdx
#     print "*****"

# 筛选 当描述子之间的距离大于两倍的最小距离时,即认为匹配有误.但有时候最小距离会非常小,设置一个经验值30作为下限
good_matches = []
for i in matches:
    if i.distance <= max(2*matches[0].distance, 60):
        good_matches.append(i)

test = []
for i in good_matches[:100]:
    test.append(i.distance)
test = np.array(test)

sum = 0

for i in good_matches:
    print i.distance
    sum += i.distance

print "aaa: " + str(sum*1.0/len(good_matches))

print "+++++++++++==="
print cv2.norm(test, normType=cv2.NORM_INF)
print cv2.norm(test, normType=cv2.NORM_L1)
print cv2.norm(test, normType=cv2.NORM_L2)

# Draw first 10 matches.
img3 = cv2.drawMatches(img1, kp1, img2, kp2, good_matches[:20], None,flags=2)  # 前10个匹配

plt.imshow(img3), plt.show()