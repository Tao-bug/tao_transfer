#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import json


def read_mat_json(mat_json_path, dataset_name):
    file_name = dataset_name.lower() + "_mat.json"
    data_path = os.path.join(mat_json_path, file_name)
    with open(data_path, "r") as f:
        data = f.read()
    return data


def look_up(mat_json_path, image_path, dataset_name):
    """
    在数据集mat文件记录的属性中查找图片对应属性
    :param mat_json_path: 保存mat中读取属性的json文件路径
    :param image_path: 样本图片数据集路径
    :param dataset_name: 数据集名字"market" "duke" "peta" "pa-100k"
    :return: 每个样本图片对应数据集mat记录的属性
    """
    # 数据集全部图片及属性
    result_dict = read_mat_json(mat_json_path, dataset_name)

    # 查询属性
    path = os.path.join(image_path, dataset_name.lower())
    file_list = os.listdir(path)
    if ".DS_Store" in file_list:
        file_list.remove(".DS_Store")
    file_list.sort()
    image_lab = {}
    for img in file_list:
        if dataset_name.lower() in ["market", "duke"]:
            image_index = img.split("_")[0]
        else:
            image_index = img.split(".")[0]
        images_dict = json.loads(result_dict)
        image_lab[image_index] = images_dict[image_index]
    image_lab = json.dumps(image_lab)
    return image_lab


if __name__ == '__main__':
    # 保存mat读取属性的文件路径
    mat_file_path = "dataset_json/"
    # 样本图片数据集
    image_file_path = "test_dataset/"
    # 数据集名字"market" "duke" "peta" "pa-100k" "rap"
    data_set_name = "rap"
    result = look_up(mat_file_path, image_file_path, data_set_name)
    print(result, len(json.loads(result)))


