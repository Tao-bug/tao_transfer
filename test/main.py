import json
import os

from PIL import Image
import pymysql


def data_from_mat(dataset_name):
    pass


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

    if url_name:
        # 原始数据---从提前存好的json
        old_path = "/home/cmcc/tao_file/tao_transfer/test/dataset_url_json_old/" + dataset_name + "_" + url_name + ".json"
        old_data = open_json(old_path)
        old_data = json.loads(old_data)
        # 映射后的数据---从提前存好的json
        new_path = "/home/cmcc/tao_file/tao_transfer/test/dataset_url_json/" + dataset_name + "_" + url_name + ".json"
        new_data = open_json(new_path)
        new_data = json.loads(new_data)
        return old_data, new_data
    else:
        # 原始数据
        old_path = "/home/cmcc/tao_file/tao_transfer/test/dataset_json_old/" + dataset_name + "_mat.json"
        old_data = open_json(old_path)
        old_data = json.loads(old_data)
        # 映射后的数据
        new_path = "/home/cmcc/tao_file/tao_transfer/test/dataset_json/" + dataset_name + "_mat.json"
        new_data = open_json(new_path)
        new_data = json.loads(new_data)
        return old_data, new_data


def create_mysql_table():
    db = pymysql.connect(host="172.31.242.25", user="gbase", password="ots_analyse_gbase", database="test",
                         port=5050)  # 打开数据库连接
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS TEST_ATTRIBUTE")
    sql = """CREATE TABLE test_attribute (
             image_path varchar(1024) not null,
             image_quality varchar(20),
             attribute varchar(1024),
             attribute_mapping varchar(1024),
             company varchar(128),
             result varchar(1024),
             result_mapping varchar(1024),
             compare_upper_wear enum('1','0','Null'),
             compare_upper_color enum('1','0','Null'),
             compare_lower_wear enum('1','0','Null'),
             compare_lower_color enum('1','0','Null'),
             compare_bag enum('1','0','Null'),
             compare_headwear enum('1','0','Null'))"""
    try:
        cursor.execute(sql)  # 执行sql语句
        # db.commit()  # 提交到数据库执行
        print("表创建成功")
    except:
        db.rollback()       # 如果发生错误则回滚
        print("sql语句有误")
    db.close()


def save_mysql(image_name, data_dict, db):
    # db = pymysql.connect(host="172.31.242.25", user="gbase", password="ots_analyse_gbase", database="test", port=5050)  # 打开数据库连接
    cursor = db.cursor()  # 创建一个游标对象 cursor
    # 使用 execute() 方法执行 SQL , 如果表存在则删除
    # 使用预处理语句创建表
    # data_dict = {'CAM01-2013-12-23-20131223120147-20131223120735-tarid3-frame493-line1': {'image_path': '/Users/tao/Desktop/test/test_dataset/rap/CAM01-2013-12-23-20131223120147-20131223120735-tarid3-frame493-line1.png', 'image_quality': "(122, 410)", 'attribute': {'clothing': ['ub-Cotton', 'lb-LongTrousers'], 'upper_color': ['ub-ColorBlack'], 'lower_color': ['lb-ColorGreen'], 'headwear': ['hs-Hat'], 'bag': ['attachment-PlasticBag'], 'footwear': ['shoes-Leather']}, 'attribute_mapping': {'upper_color': ['黑'], 'lower_color': ['绿'], 'headwear': ['有'], 'bag': ['有'], 'footwear': ['有'], 'upper_wear': ['长袖'], 'lower_wear': ['长裤']}, 'company': '百度', 'result': [{'total_num': 1}, {'position': [2, 0, 111, 401], 'score': 0.9748985767364502, 'upper_wear': '长袖', 'upper_color': '黑', 'lower_wear': '长裤', 'lower_color': '绿', 'bag': '无背包', 'headwear': '普通帽'}], 'result_mapping': [{'total_num': 1}, {'position': [2, 0, 111, 401], 'score': 0.9748985767364502, 'upper_wear': '长袖', 'upper_color': '黑', 'lower_wear': '长裤', 'lower_color': '绿', 'bag': '无', 'headwear': '有'}], 'compare': [1, 1, 1, 1, 0, 1]}}
    # attribute = data_dict["CAM01-2013-12-23-20131223120147-20131223120735-tarid3-frame493-line1"]
    attribute = data_dict[image_name]
    data = (
        # num,
        str(attribute["image_path"]),
        str(attribute["image_quality"]),
        str(attribute["attribute"]),
        str(attribute["attribute_mapping"]),
        str(attribute["company"]),
        str(attribute["result"]),
        str(attribute["result_mapping"]),
        # attribute["compare"]["upper_wear"],
        str(attribute["compare"][0]),
        # attribute["compare"]["upper_color"],
        str(attribute["compare"][1]),
        # attribute["compare"]["lower_wear"],
        str(attribute["compare"][2]),
        # attribute["compare"]["lower_color"],
        str(attribute["compare"][3]),
        # attribute["compare"]["bag"],
        str(attribute["compare"][4]),
        # attribute["compare"]["headwear"]
        str(attribute["compare"][5])
    )
    sql = """insert into test_attribute values {}""".format(data)
    # print(sql)
    try:
        cursor.execute(sql)  # 执行sql语句
        db.commit()  # 提交到数据库执行
    except:
        db.rollback()       # 如果发生错误则回滚
        print("sql语句有误")
    cursor.close()
    # db.close()


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

    # 对于没提前保存的
    # 数据集
    # 接口

    # 对于提前保存好的json数据
    # 数据集
    dataset_dict_old, dataset_dict_new = data_from_json(dataset)
    # 接口
    url_dict_old, url_dict_new = data_from_json(dataset, url_name)

    # 打开数据库连接
    db = pymysql.connect(host="172.31.242.25", user="gbase", password="ots_analyse_gbase", database="test",
                         port=5050)
    result_dict = {}
    for img in file_list[:]:  # TODO [:2]
        attribute_dict = {"image_path": os.path.join(path, img), "image_quality": "Null", "attribute": "Null",
                          "attribute_mapping": "Null", "company": "Null", "result": "Null", "result_mapping": "Null",
                          "compare": "Null"}

        # 图片路径===>这是写图片的名字还是什么？？？
        # 分辨率
        img_switch = Image.open(attribute_dict["image_path"])  # 读取图片
        w, h = img_switch.size
        attribute_dict["image_quality"] = (w, h)

        img = img.split(".")[0]
        # 一张图片整体属性
        # dataset
        dataset_attribute_dict_old = dataset_dict_old[img]
        dataset_attribute_dict = dataset_dict_new[img]
        attribute_dict["attribute"] = dataset_attribute_dict_old
        attribute_dict["attribute_mapping"] = dataset_attribute_dict
        # 公司名字
        company = {"baidu": "百度", "jingdong": "京东", "kuangshi": "旷世", "meitu": "美图", "yingshi": "萤石", "jiutian": "九天"}
        attribute_dict["company"] = company[url_name]
        # url
        url_attribute_list_old = url_dict_old[img]
        url_attribute_list = url_dict_new[img]  # 存在"total_num": 2, 取第一个
        attribute_dict["result"] = url_attribute_list_old
        attribute_dict["result_mapping"] = url_attribute_list
        # 存在"total_num": 2, 取第一个
        url_attribute_dict = url_attribute_list[1]
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

    # print(result_dict)
    # result_dict = json.dumps(result_dict, ensure_ascii=False)
    # return result_dict


if __name__ == '__main__':
    test_image_path = "/home/cmcc/tao_file/tao_transfer/test/test_dataset"  # 查询图片的路径
    dataset_name = "rap"  # 查询图片所属数据集
    url_name = "jiutian"  # "baidu" "jingdong" "kuangshi" "jiutian"   "meitu" "yingshi"
    # url_name_list = ["baidu", "jingdong", "kuangshi", "meitu", "yingshi", "jiutian"]
    # for url_name in url_name_list:
    #     start(test_image_path, dataset_name, url_name)

    start(test_image_path, dataset_name, url_name)

    # create_mysql_table()
