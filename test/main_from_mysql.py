import json
import os

from PIL import Image
import pymysql

from utiles import utiles
from testAI import fix_baidu
from testAI import fix_jingdong
from testAI import fix_kuangshi
from testAI import fix_meitu
from testAI import fix_yingshi
from testAI import fix_jiutian
from testDateset import market
from testDateset import duke
from testDateset import pa_100k
from testDateset import peta
from testDateset import rap


def data_from_mat(path, dataset, name, mapping=False):
    """
    网络接口查询属性
    :param path: mat文件目录
    :param dataset: 查询图片所属数据集
    :param name: 网络接口名字
    :param mapping: 是否映射
    :return:
    """


def data_from_url(image_file, name, mapping=False):
    """
    网络接口查询属性
    :param image_file: 查询图片的路径
    :param name: 网络接口名字
    :param mapping: 是否映射
    :return:
    """
    try:
        # 百度
        if name == "baidu":
            method_name = fix_baidu
            attribute = utiles.infer(method_name, image_file)
        # 京东
        elif name == "jingdong":
            method_name = fix_jingdong
            attribute = utiles.infer(method_name, image_file)
        # 旷视
        elif name == "kuangshi":
            method_name = fix_kuangshi
            attribute = utiles.infer(method_name, image_file)
        # 美图
        elif name == "meitu":
            method_name = fix_meitu
            attribute = utiles.infer(method_name, image_file)
        # 萤石
        elif name == "yingshi":
            method_name = fix_yingshi
            attribute = utiles.infer(method_name, image_file)
        # 九天
        elif name == "jiutian":
            method_name = fix_jiutian
            attribute = utiles.infer(method_name, image_file)
        else:
            attribute = [{'total_num': 0}, {"err": "接口名字有误"}]
        # print(attribute)
    except:
        attribute = [{'total_num': 0},
                     {"position": "Null", "score": "Null", "upper_wear": "Null", "upper_color": "Null",
                      "lower_wear": "Null", "lower_color": "Null", "bag": "Null", "headwear": "Null",
                      "hat": "Null"}]
    # 属性映射
    if mapping is True:
        attribute = utiles.url_attribute_map(attribute, name)
    return attribute


def data_from_json(dataset_name, url_name=None):
    """
    针对已提前保存属性的
    :param dataset_name: 图片所属数据集
    :param url_name: 网路接口名字
    :return: 返回整体属性
    """

    def open_json(json_path):
        with open(json_path, "r") as f:
            data = f.read()
        return data

    # 当前项目所在路径
    path = os.getcwd()
    if url_name:
        # 原始数据---从提前存好的json
        old_path = path + "/dataset_url_json_old/" + dataset_name + "_" + url_name + ".json"
        old_data = open_json(old_path)
        old_data = json.loads(old_data)
        # 映射后的数据---从提前存好的json
        new_path = path + "/dataset_url_json/" + dataset_name + "_" + url_name + ".json"
        new_data = open_json(new_path)
        new_data = json.loads(new_data)
        return old_data, new_data
    else:
        # 原始数据
        old_path = path + "/dataset_json_old/" + dataset_name + "_mat.json"
        old_data = open_json(old_path)
        old_data = json.loads(old_data)
        # 映射后的数据
        new_path = path + "/dataset_json/" + dataset_name + "_mat.json"
        new_data = open_json(new_path)
        new_data = json.loads(new_data)
        return old_data, new_data


def data_from_mysql():
    db = pymysql.connect(host="172.31.242.25", user="gbase", password="ots_analyse_gbase", database="test",
                         port=5050, charset='utf8')  # 打开数据库连接
    cursor = db.cursor()
    sql = "select image_path,new_attribute from new_attribute_data"
    try:
        cursor.execute(sql)
    except:
        db.rollback()
        print("sql语句有误")
    data = cursor.fetchall()  # tuple
    data_dict = {}
    for i in data:
        key = i[0].split("/")[-1].split(".")[0]
        data_dict[key] = eval(i[1])
    return data_dict


def save_mysql(image_name, data_dict, db):
    cursor = db.cursor()  # 创建一个游标对象 cursor
    attribute = data_dict[image_name]
    sql = "insert into test_attribute_newattribute_copy_7_23 values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data = (
        str(attribute["image_path"]),
        str(attribute["image_quality"]),
        str(attribute["attribute"]),
        str(attribute["company"]),
        str(attribute["result"]),
        str(attribute["result_mapping"]),
        # attribute["compare"]["upper_wear"],
        attribute["compare"][0] if attribute["compare"][0] != "Null" else None,
        # attribute["compare"]["upper_color"],
        attribute["compare"][1] if attribute["compare"][1] != "Null" else None,
        # attribute["compare"]["lower_wear"],
        attribute["compare"][2] if attribute["compare"][2] != "Null" else None,
        # attribute["compare"]["lower_color"],
        attribute["compare"][3] if attribute["compare"][3] != "Null" else None,
        # attribute["compare"]["bag"],
        attribute["compare"][4] if attribute["compare"][4] != "Null" else None,
        # attribute["compare"]["headwear"]
        attribute["compare"][5] if attribute["compare"][5] != "Null" else None
    )
    try:
        cursor.execute(sql, data)  # 执行sql语句
        db.commit()  # 提交到数据库执行
    except:
        db.rollback()       # 如果发生错误则回滚
        print("sql语句有误")
    cursor.close()


def start(path, dataset, url_name):
    """
    网络接口查询属性
    :param path: 查询图片的路径
    :param dataset: 查询图片所属数据集
    :param url_name: 网络接口名字
    :return:
    """
    path = os.path.join(path, dataset)
    file_list = os.listdir(path)
    if ".DS_Store" in file_list:
        file_list.remove(".DS_Store")
    file_list.sort()
    # 数据集
    dataset_dict = data_from_mysql()

    # 打开数据库连接
    db = pymysql.connect(host="172.31.242.25", user="gbase", password="ots_analyse_gbase", database="test",
                         port=5050)
    result_dict = {}
    for img in file_list[:]:  # TODO [:2]
        print(img)
        attribute_dict = {"image_path": os.path.join(path, img), "image_quality": "Null", "attribute": "Null",
                          "attribute_mapping": "Null", "company": "Null", "result": "Null", "result_mapping": "Null",
                          "compare": "Null"}
        # 接口
        # 映射前
        url_dict_old = data_from_url(attribute_dict["image_path"], url_name)
        # 映射后
        url_dict_new = data_from_url(attribute_dict["image_path"], url_name, mapping=True)

        # 分辨率
        img_switch = Image.open(attribute_dict["image_path"])  # 读取图片
        w, h = img_switch.size
        attribute_dict["image_quality"] = (w, h)

        img = img.split(".")[0]
        # 一张图片整体属性
        # dataset
        dataset_attribute_dict = dataset_dict[img]
        attribute_dict["attribute"] = dataset_attribute_dict
        # 公司名字
        company = {"baidu": "百度", "jingdong": "京东", "kuangshi": "旷世", "meitu": "美图", "yingshi": "萤石", "jiutian": "九天"}
        attribute_dict["company"] = company[url_name]
        # url
        attribute_dict["result"] = url_dict_old
        attribute_dict["result_mapping"] = url_dict_new  # 存在"total_num": 2, 取第一个
        # 存在"total_num": 2, 取第一个
        url_attribute_dict = url_dict_new[1]
        compare_dict = {}

        # 属性对比
        # 工具
        def util(key):
            if url_attribute_dict[key] == "Null":
                compare_dict[key] = "Null"
            elif url_attribute_dict[key] in dataset_attribute_dict[key]:
                compare_dict[key] = 1
            elif url_attribute_dict[key] not in dataset_attribute_dict[key]:
                compare_dict[key] = 0
        # upper_wear
        util("upper_wear")
        # upper_color
        util("upper_color")
        # lower_wear
        util("lower_wear")
        # lower_color
        util("lower_color")
        # bag
        util("bag")
        # headwear
        util("headwear")
        # print(compare_dict)

        # attribute_dict["compare"] = compare_dict  # 比对属性以字典呈现
        attribute_dict["compare"] = list(compare_dict.values())  # 比对属性以列表呈现
        result_dict[img] = attribute_dict
        # print(result_dict)

        # 保存到mysql数据库
        save_mysql(img, result_dict, db)
        print("数据保存完毕")
    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    test_image_path = os.getcwd() + "/test_dataset"  # 查询图片的路径
    dataset_name = "rap"  # 查询图片所属数据集
    # url_name = "meitu"  # "baidu" "jingdong" "kuangshi" "jiutian"   "meitu" "yingshi"
    url_name_list = ["baidu", "jingdong", "kuangshi", "meitu", "yingshi", "jiutian"]
    for url_name in url_name_list:
        start(test_image_path, dataset_name, url_name)
    # start(test_image_path, dataset_name, url_name)
