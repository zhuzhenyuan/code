# -*- coding: utf-8 -*-

import os


def filter_data(matches):
    try:
        # 筛选 当描述子之间的距离大于两倍的最小距离时,即认为匹配有误.但有时候最小距离会非常小,设置一个经验值30作为下限
        good_matches = []
        for i in matches:
            if int(i) <= max(2*int(matches[0]), 65):
                good_matches.append(i)
        return good_matches
    except:
        return []


# 计算最小值小于给定值
def analysis_1():
    base_path = "./result/orb/"

    txt_list = os.listdir(base_path)

    for txt in txt_list:
        file = open(base_path+txt, "r")
        rows = 0
        count = 0
        for one in file:
            if one == "-1":
                continue

            one_data = one[1:len(one) - 1].split(".0")

            if int(one_data[0]) < 30:
                count += 1
            rows += 1

        file.close()
        print txt + ": " + str(int(count*1.0 / rows * 100))


# 小于某个值的个数在一条记录中的比例，
def analysis_2():
    base_path = "./result/orb/"

    txt_list = os.listdir(base_path)

    for txt in txt_list:
        file = open(base_path+txt, "r")
        rows = 0
        count = 0
        for one in file:
            if one == "-1" or one == "" or one == "\n":
                continue

            one_data = one[1:len(one) - 2].replace(",", "").replace(".0", "").split(" ")

            num_count = 0

            for num in one_data:
                if num is "":
                    one_data.remove(num)
                elif int(num) <= 60:
                    num_count += 1
            try:
                if num_count*1.0 / len(one_data)*100 > 50.0:
                    count += 1
                rows += 1
            except:
                pass


        file.close()
        print txt + ": " + str(int(count*1.0 / rows * 100))


# 计算一条记录的平均值
def analysis_3():
    base_path = "./result/orb/"

    txt_list = os.listdir(base_path)

    for txt in txt_list:
        file = open(base_path + txt, "r")
        rows = 0
        count = 0
        for one in file:
            if one == "-1" or one == "" or one == "\n":
                continue

            one_data = one[1:len(one) - 2].replace(",", "").replace(".0", "").split(" ")

            one_data = filter_data(one_data)
            num_sum = 0

            for num in one_data:
                if num is "":
                    one_data.remove(num)
                else:
                    num_sum += int(num)
            try:
                if num_sum * 1.0 / len(one_data) <= 52.245:
                    count += 1
                rows += 1
            except:
                pass

        file.close()
        print txt + ": " + str(int(count * 1.0 / rows * 100))


if __name__ == "__main__":

    # analysis_1()
    # analysis_2()
    analysis_3()
