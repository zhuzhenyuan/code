# -*- coding: utf-8 -*-
import os
import shutil

def get_imlist(path):
    """
    返回目录中所有 jpg 图像的文件名列表
    :param path:
    :return:
    """
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]


def copy_image():
    base_dir = "./test_data/lfw_mtcnnpy_160/"
    dist_dir = "./test_data/all_img/"

    count = 0
    dir_list = os.listdir(base_dir)
    for tmp_dir in dir_list:
        img_dir = os.listdir(base_dir + tmp_dir)
        for img in img_dir:
            file_dir1 = base_dir + tmp_dir + '/' + img
            file_dir2 = dist_dir + img
            shutil.copy(file_dir1, file_dir2)
            if os.path.isfile(file_dir2):
                print("Success__" + str(count))
                count += 1
    print("********************")
    print("all is： " + str(count) + "_-zhang")
    print("********************")


if __name__ == "__main__":
    copy_image()

