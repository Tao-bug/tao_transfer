import os
import json
import time

from testAI import fix_baidu
from testAI import fix_jingdong
from testAI import fix_kuangshi
from testAI import fix_meitu
from testAI import fix_yingshi
from testAI import fix_jiutian


def infer(method_name, image_file):
    result = method_name.algorhtmReq(image_file)
    result = json.loads(result)
    # print(result)
    time.sleep(1)  # 防止访问过快
    return result


def save_json(image_json, dataset_name, url_name, save_json_path):
    """
    把记录的属性保存为文件，方便读取
    :param image_json: json数据
    :param dataset_name: 数据集名字
    :param url_name: 接口名
    :param save_json_path: 结果保存的路径
    :return: None
    """
    # save_mat_path = "/Users/tao/Desktop/test/dataset_url_json/"
    # 保存数据集分析结果
    print(len(json.loads(image_json)))
    file_name = dataset_name + "_" + url_name + ".json"
    save_path = os.path.join(save_json_path, file_name)
    with open(save_path, "w") as f:
        f.write(image_json)
    print("完美完成")


def attribute_map(attribute_list, name):
    """属性映射"""
    if name != "meitu":
        # upper_wear  # 萤石待定
        upper_wear_list = ["长袖", "短袖", "长裙", "上衣", "连衣裙", "大衣", "裙子", "T恤", "衬衫", "毛衣", "卫衣", "风衣", "外套", "牛仔夹克", "棒球服式外套",
                           "正装", "棉服", "皮夹克"]
        # lower_wear
        lower_wear_list = ["长裤", "短裤", "短裙", "连体裤"]
        # color
        color_list = ["红", "橙", "黄", "绿", "蓝", "紫", "粉", "黑", "白", "灰", "棕", "不确定", "未知", "black", "white", "red", "green",
                      "blue", "yellow", "magenta", "cyan", "gray", "purple", "orange"]
        # bag
        bag_list = ["无背包", "单肩包", "双肩包", "不确定"]
        # headwear
        headwear_list = ["无帽", "普通帽", "安全帽"]

        # 属性映射
        # upper_wear_stander_dict = {"长袖", "短袖", "连衣裙"}
        upper_wear_stander_dict = {"Null": "Null", "未知": "未知", "长袖": "长袖", "短袖": "短袖", "长裙": "连衣裙", "上衣": "长袖", "连衣裙": "连衣裙",
                                   "大衣": "长袖", "T恤": "短袖", "衬衫": "长袖", "毛衣": "长袖", "卫衣": "长袖", "风衣": "长袖", "外套": "长袖",
                                   "牛仔夹克": "长袖", "棒球服式外套": "长袖", "正装": "长袖", "棉服": "长袖", "皮夹克": "长袖"}
        # lower_wear_stander_dict = {"长裤", "短裤", "短裙"}
        lower_wear_stander_dict = {"Null": "Null", "未知": "未知", "长裤": "长裤", "短裤": "短裤", "短裙": "短裙", "裙子": "短裙", "连体裤": "长裤"}
        # color_stander_dict = {"红", "橙", "黄", "绿", "蓝", "紫", "粉", "黑", "白", "灰", "棕", "未知"}
        color_stander_dict = {"Null": "Null", "红": "红", "橙": "橙", "黄": "黄", "绿": "绿", "蓝": "蓝", "紫": "紫", "粉": "粉",
                              "黑": "黑", "白": "白", "灰": "灰", "棕": "棕", "不确定": "未知", "未知": "未知", "混色": "未知", "black": "黑",
                              "white": "白", "red": "红", "green": "绿", "blue": "蓝", "yellow": "黄", "magenta": "红",
                              "cyan": "蓝", "gray": "灰", "purple": "紫", "orange": "橙"}
        # bag_stander_dict = {"有", "无"}
        bag_stander_dict = {"Null": "Null", "无背包": "无", "单肩包": "有", "双肩包": "有", "不确定": "有", "不背包": "无", "有":"有", "无":"无"}
        # headwear_stander_dict = {"有", "无"}
        headwear_stander_dict = {"Null": "Null", "无帽": "无", "普通帽": "有", "安全帽": "有", "yes": "有", "no": "无", "hat": "有", "不戴帽子": "无"}

        # 原有属性
        for i in range(attribute_list[0]["total_num"]):
            attribute = attribute_list[i + 1]
            if attribute["upper_wear"] in upper_wear_stander_dict.keys():
                attribute["upper_wear"] = upper_wear_stander_dict[attribute["upper_wear"]]
            if attribute["upper_color"] in color_stander_dict.keys():
                attribute["upper_color"] = color_stander_dict[attribute["upper_color"]]
            if attribute["lower_wear"] in lower_wear_stander_dict.keys():
                attribute["lower_wear"] = lower_wear_stander_dict[attribute["lower_wear"]]
            if attribute["lower_color"] in color_stander_dict.keys():
                attribute["lower_color"] = color_stander_dict[attribute["lower_color"]]
            if attribute["bag"] in bag_stander_dict.keys():
                attribute["bag"] = bag_stander_dict[attribute["bag"]]
            if attribute["headwear"] in headwear_stander_dict.keys():
                attribute["headwear"] = headwear_stander_dict[attribute["headwear"]]

    # 美图
    else:
        upper_wear_stander_dict = {"T恤": "短袖", "衬衫": "长袖", "毛衣": "长袖", "卫衣": "长袖", "风衣": "长袖", "外套": "长袖",
                                   "牛仔夹克": "长袖", "棒球服式外套": "长袖", "正装": "长袖", "大衣": "长袖", "棉服": "长袖",
                                   "皮夹克": "长袖",
                                   "长袖": "长袖", "短袖": "短袖", "无袖背心": "短袖", "吊带": "短袖", "未知": "未知"}
        for i in range(attribute_list[0]["total_num"]):
            attribute = attribute_list[i + 1]
            for idx in attribute["upper_wear"]:
                if idx in upper_wear_stander_dict.keys():
                    attribute["upper_wear"] = upper_wear_stander_dict[idx]
    return attribute_list


def main_url(path, dataset, name):
    """
    网络接口查询属性
    :param path: 查询图片的路径
    :param dataset: 查询图片所属数据集
    :param name: 网络接口名字
    :return:
    """
    path = os.path.join(path, dataset)
    file_list = os.listdir(path)
    if ".DS_Store" in file_list:
        file_list.remove(".DS_Store")
    file_list.sort()
    # print(file_list)  # 图片名字
    image_dict = {}
    for img in file_list[:]:  # TODO [:2]
        print(img)
        if name.lower() in ["market", "duke"]:
            image_index = img.split("_")[0]
        else:
            image_index = img.split(".")[0]
        # print(image_index)
        image_file = os.path.join(path, img)  # 图片路径
        try:
            # 百度 ---
            if name == "baidu":
                method_name = fix_baidu
                attribute = infer(method_name, image_file)
            # 京东
            elif name == "jingdong":
                method_name = fix_jingdong
                attribute = infer(method_name, image_file)
            # 旷视
            elif name == "kuangshi":
                method_name = fix_kuangshi
                attribute = infer(method_name, image_file)
            # 美图
            elif name == "meitu":
                method_name = fix_meitu
                attribute = infer(method_name, image_file)
            # 萤石
            elif name == "yingshi":
                method_name = fix_yingshi
                attribute = infer(method_name, image_file)
            # 九天
            elif name == "jiutian":
                method_name = fix_jiutian
                attribute = infer(method_name, image_file)
            else:
                attribute = [{'total_num': 0}, {"err": "接口名字有误"}]
            # print(attribute)
        except:
            attribute = [{'total_num': 0}, {"position": "Null", "score": "Null", "upper_wear": "Null", "upper_color": "Null", "lower_wear": "Null", "lower_color": "Null", "bag": "Null", "headwear": "Null", "hat": "Null"}]

        # 属性映射
        # attribute = attribute_map(attribute, name)

        image_dict[image_index] = attribute  # 有人数统计
    image_dict = json.dumps(image_dict, ensure_ascii=False)  # ensure_ascii=False不转译汉字
    return image_dict


if __name__ == '__main__':
    # 数据集路径
    dataset_path = "test_dataset/"
    # 数据集 "peta"  "pa-100k" "market" "duke" "rap" "test" "APY181031001"
    dataset_name = "rap"
    # 接口名字 "baidu" "jingdong" "kuangshi" "jiutian"   "meitu" "yingshi"
    url_name = "jiutian"
    # r = main(dataset_path, dataset_name, url_name)
    # print(json.loads(r), len(json.loads(r)))

    # result = main_url(dataset_path, dataset_name, url_name)
    # print(json.loads(result), len(json.loads(result)))

    # 保存json
    # 映射前
    #save_mat_path = "/home/cmcc/tao_file/tao_transfer/test/dataset_url_json_old/"
    # 映射后
    with open("/home/cmcc/tao_file/tao_transfer/test/dataset_url_json_old/rap_jiutian.json", "r") as f:
        result = f.read()
    save_mat_path = "/home/cmcc/tao_file/tao_transfer/test/dataset_url_json/"

    save_json(result, dataset_name, url_name, save_mat_path)
