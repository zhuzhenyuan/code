# -*- coding: utf-8 -*-

def a1():
    print "a1"
    ff = open("./result/ff/ff.txt")
    count = 0
    sum = 0
    max = 0
    for i in ff:
        if i.startswith("@"):
            l = i.split("@")
            if float(l[1]) < 60:
                sum += float(l[1])
                count += 1
                if max < float(l[1]):
                    max = float(l[1])
    print sum * 1.0 / count
    print max


def a2():
    print "a2"
    ff = open("./result/ff/ff2.txt")
    count = 0
    sum = 0
    max = 0
    for i in ff:
        if i.startswith("@"):
            l = i.split("@")
            if float(l[1]) < 60:
                sum += float(l[1])
                count += 1
                if max < float(l[1]):
                    max = float(l[1])
    print sum * 1.0 / count
    print max

def a3():
    print "a3"
    ff = open("./result/ff/ff3.txt")
    count = 0
    sum = 0
    max = 0
    for i in ff:
        if i.startswith("@"):
            l = i.split("@")
            if float(l[1]) < 60:
                sum += float(l[1])
                count += 1
                if max < float(l[1]):
                    max = float(l[1])
    print sum * 1.0 / count
    print max


def a4():
    print "a4"
    ff = open("./result/ff/ff4.txt")
    count = 0
    sum = 0
    max = 0
    all = 0
    cc = 0
    for i in ff:
        all += 1
        # if "是" in i:
        #     cc += 1
        if i.startswith("@"):
            cc += 1
            l = i.split("@")
            if float(l[1]) < 60:
                sum += float(l[1])
                count += 1
                if max < float(l[1]):
                    max = float(l[1])
    print sum * 1.0 / count
    print max
    print cc*1.0/all

def a5():
    print "a5"
    ff = open("./result/ff/ff5.txt")
    count = 0
    sum = 0
    max = 0
    all = 0
    cc = 0
    for i in ff:
        all += 1
        # if "是" in i:
        #     cc += 1
        if i.startswith("@"):
            cc += 1
            l = i.split("@")
            if float(l[1]) < 60:
                sum += float(l[1])
                count += 1
                if max < float(l[1]):
                    max = float(l[1])
    print sum * 1.0 / count
    print max
    print cc*1.0/all

def a6():
    print "a5"
    ff = open("./result/ff/ff5.txt")
    count = 0
    sum = 0
    max = 0
    all = 0
    cc = 0
    for i in ff:
        all += 1
        # if "是" in i:
        #     cc += 1
        if i.startswith("@"):
            cc += 1
            l = i.split("@")
            if float(l[1]) < 60:
                sum += float(l[1])
                count += 1
                if max < float(l[1]):
                    max = float(l[1])
    print sum * 1.0 / count
    print max
    print cc*1.0/all


if __name__ == "__main__":

    a1()
    a2()
    a3()
    a4()
    a5()
    a6()


