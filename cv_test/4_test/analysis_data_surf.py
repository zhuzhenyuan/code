# -*- coding: utf-8 -*-

import os
import cv2


# 计算最小值小于给定值
def analysis_1():
    try:
        base_path = "./result/surf_k2/"

        txt_list = os.listdir(base_path)

        for txt in txt_list:
            file = open(base_path+txt, "r")
            rows = 0
            count = 0
            for one in file:
                if "-1" in one  or one is "":
                    continue

                one_data = one[1:len(one) - 2].split(", ")

                # if float(one_data[0]) < 0.1:
                if float(one_data[len(one_data)-1])+float(one_data[0]) < 0.75:
                    count += 1
                rows += 1

            file.close()
            print txt + ": " + str(int(count*1.0 / rows * 100))
    except:
        print -1


# 小于某个值的个数在一条记录中的比例，
def analysis_2():
    base_path = "./result/surf_k2/"

    txt_list = os.listdir(base_path)

    for txt in txt_list:
        file = open(base_path+txt, "r")
        rows = 0
        count = 0
        for one in file:
            if one == "-1" or one == "" or one == "\n":
                continue

            one_data = one[1:len(one) - 2].split(", ")

            num_count = 0

            for num in one_data:
                if num is "":
                    one_data.remove(num)
                # elif float(num) <= 0.35:
                elif float(num) <= 0.2:
                # elif float(num) <= 0.3:
                    num_count += 1
            try:
                # if num_count*1.0 / len(one_data) > 0.5:
                if num_count*1.0 / len(one_data) > 0.08:
                # if num_count*1.0 / len(one_data) > 0.23:
                    count += 1
                rows += 1
            except:
                pass


        file.close()
        print txt + ": " + str(int(count*1.0 / rows * 100))


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
def analysis_3():
    base_path = "./result/surf_k2/"

    txt_list = os.listdir(base_path)

    for txt in txt_list:
        file = open(base_path + txt, "r")
        rows = 0
        count = 0
        for one in file:
            if one == "-1" or one == "" or one == "\n":
                continue

            one_data = one[1:len(one) - 2].split(", ")

            one_data = filter_data(one_data)
            num_sum = 0

            for num in one_data:
                if num is "":
                    one_data.remove(num)
                else:
                    num_sum += float(num)
            try:
                if num_sum * 1.0 / len(one_data) <= 0.15:
                    count += 1
                rows += 1
            except:
                pass

        file.close()
        if rows:
            print txt + ": " + str(int(count * 1.0 / rows * 100))


def analysis_4():
    base_path = "./result/surf_k2/"

    txt_list = os.listdir(base_path)

    for txt in txt_list:
        file = open(base_path + txt, "r")
        rows = 0
        count = 0
        for one in file:
            if one == "-1" or one == "" or one == "\n":
                continue

            one_data = one[1:len(one) - 2].split(", ")

            # one_data = filter_data(one_data)
            # print cv2.norm(one_data)
            # return

            num_sum = 0

            for num in one_data:
                if num is "":
                    one_data.remove(num)
                else:
                    num_sum += float(num)
            try:
                if num_sum * 1.0 / len(one_data) <= 0.15:
                    count += 1
                rows += 1
            except:
                pass

        file.close()
        if rows:
            print txt + ": " + str(int(count * 1.0 / rows * 100))


if __name__ == "__main__":

    # analysis_1()
    # analysis_2()
    # analysis_3()
    analysis_4()
