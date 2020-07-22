import json
import time

import pymysql


def infer(method_name, image_file):
    result = method_name.algorhtmReq(image_file)
    result = json.loads(result)
    # print(result)
    time.sleep(1)  # 防止访问过快
    return result


def url_attribute_map(attribute_list, name):
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


def dataset_attribute_map(images_dict, dataset):
    """属性映射"""
    images_dict = json.loads(images_dict)
    # 属性值为空列表，代表不具备该属性
    # 属性映射
    # upper_wear_stander_dict = {"长袖", "短袖", "连衣裙"}
    upper_wear_stander_dict = {"Null": "未知", "upper_wear_null":"未知","ub-Shirt":"长袖", "ub-Sweater":"长袖", "ub-Vest":"短袖","ub-TShirt":"短袖","ub-Cotton":"长袖","ub-Jacket":"长袖","ub-SuitUp":"长袖","ub-Tight":"长袖","ub-ShortSleeve":"短袖","ub-Others":"未知", "lb-Dress":"连衣裙",
                               "upperBodyFormal":"长袖","upperBodyJacket":"长袖","upperBodyLongSleeve":"长袖", "upperBodyNoSleeve":"短袖","upperBodyPlaid":"长袖","upperBodyShortSleeve":"短袖","upperBodyThinStripes":"长袖","upperBodySuit":"长袖","upperBodySweater":"长袖",
                               "upperBodyThickStripes":"长袖","upperBodyTshirt":"短袖","upperBodyOther":"未知","upperBodyVNeck":"短袖","ShortSleeve":"短袖","LongSleeve":"长袖","LongCoat":"长袖","long upper body clothing":"长袖","short upper body clothing":"短袖","dress":"连衣裙",
                               "long sleeve":"长袖","short sleeve":"短袖",}
    # lower_wear_stander_dict = {"长裤", "短裤", "短裙"}
    lower_wear_stander_dict = {"Null": "未知","lower_wear_null":"未知","lb-LongTrousers": "长裤", "lb-Shorts": "短裤", "lb-Skirt": "短裙","lb-ShortSkirt": "短裙","lb-LongSkirt": "短裙", "lb-Jeans": "长裤","lb-TightTrousers": "长裤",
                               "lowerBodyCasual":"长裤","lowerBodyHotPants":"短裤","lowerBodyJeans":"长裤","lowerBodyLongSkirt": "短裙","lowerBodyPlaid":"长裤","lowerBodyThinStripes":"长裤","lowerBodyShorts": "短裤","lowerBodyShortSkirt": "短裤",
                               "lowerBodySuits": "长裤","lowerBodyTrousers":"长裤","Trousers":"长裤","Shorts": "短裤","Skirt&Dress":"短裙","pants":"长裤",}
    # color_stander_dict = {"红", "橙", "黄", "绿", "蓝", "紫", "粉", "黑", "白", "灰", "棕", "未知"}
    color_stander_dict = {"Null": "未知","up-ColorRed": "红", "ub-ColorOrange":"橙", "ub-ColorYellow":"黄", "ub-ColorGreen":"绿", "ub-ColorBlue":"蓝", "ub-ColorPurple":"紫", "ub-ColorPink":"粉", "ub-ColorBlack":"黑", "ub-ColorWhite":"白", "ub-ColorGray":"灰", "ub-ColorSilver":"灰", "ub-ColorBrown":"棕", "ub-ColorMixture":"未知", "ub-ColorOther":"未知", "lb-ColorMixture":"未知","lb-ColorOther":"未知","lb-ColorBlack":"黑", "lb-ColorWhite":"白", "lb-ColorRed":"红", "lb-ColorGreen":"绿","lb-ColorBlue":"蓝", "lb-ColorYellow":"黄", "lb-ColorGray":"灰", "lb-ColorSilver":"灰","lb-ColorBrown":"棕","lb-ColorPurple":"紫", "lb-ColorPink":"粉","lb-ColorOrange":"橙","Black": "黑","Brown":"棕","Pink":"粉","White": "白", "Red": "红", "Green": "绿", "Blue": "蓝", "Yellow": "黄", "Grey": "灰", "Purple": "紫", "Orange": "橙",
                          "black":"黑","white":"白", "red":"红","purple":"紫","gray":"灰","blue":"蓝","green":"绿","brown":"棕","pink":"粉",}
    # bag_stander_dict = {"有", "无"}
    bag_stander_dict = {"Null":"无", "attachment-Backpack":"有", "attachment-ShoulderBag":"有", "attachment-HandBag":"有", "attachment-WaistBag":"有","attachment-PlasticBag":"有","attachment-PaperBag":"有","attachment-Other":"有","HandBag":"有","ShoulderBag":"有","carryingMessengerBag":"有","carryingPlasticBags":"有","ackpack":"有","backpack":"有",}
    # headwear_stander_dict = {"有", "无"}
    headwear_stander_dict = {"Null":"无", "hs-Hat":"有", "accessoryHat":"有","Hat":"有","hat":"有"}

    # 原有属性==>映射
    for img_idx in images_dict.keys():
        # clothing
        if images_dict[img_idx]["clothing"] != "Null":
            clothing_list = images_dict[img_idx].pop("clothing")
            images_dict[img_idx]["upper_wear"] = []
            images_dict[img_idx]["lower_wear"] = []
            for i in clothing_list:
                # upper_wear
                if i in upper_wear_stander_dict.keys():
                    images_dict[img_idx]["upper_wear"].append(upper_wear_stander_dict[i])
                # lower_wear
                elif i in lower_wear_stander_dict.keys():
                    images_dict[img_idx]["lower_wear"].append(lower_wear_stander_dict[i])
        # upper_color
        if images_dict[img_idx]["upper_color"] != "Null":
            upper_color_list = images_dict[img_idx]["upper_color"]
            images_dict[img_idx]["upper_color"] = []
            for i in upper_color_list:
                if i in color_stander_dict.keys():
                    images_dict[img_idx]["upper_color"].append(color_stander_dict[i])
        # lower_color
        if images_dict[img_idx]["lower_color"] != "Null":
            lower_color_list = images_dict[img_idx]["lower_color"]
            images_dict[img_idx]["lower_color"] = []
            for i in lower_color_list:
                if i in color_stander_dict.keys():
                    images_dict[img_idx]["lower_color"].append(color_stander_dict[i])
        # bag
        if images_dict[img_idx]["bag"] != "Null":
            images_dict[img_idx]["bag"] = ["有"]
        else:
            images_dict[img_idx]["bag"] = ["无"]
        # headwear
        if images_dict[img_idx]["headwear"] != "Null":
            images_dict[img_idx]["headwear"] = ["有"]
        else:
            images_dict[img_idx]["headwear"] = ["无"]
        # footwear
        if dataset != "market":
            if images_dict[img_idx]["footwear"] != "Null":
                images_dict[img_idx]["footwear"] = ["有"]
            else:
                images_dict[img_idx]["footwear"] = ["无"]
    images_dict = json.dumps(images_dict, ensure_ascii=False)  # ensure_ascii=False不转译汉字
    return images_dict


def create_mysql_table():
    db = pymysql.connect(host="172.31.242.25", user="gbase", password="ots_analyse_gbase", database="test",
                         port=5050)  # 打开数据库连接
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS TEST_ATTRIBUTE")
    sql = """CREATE TABLE `test_attribute` (
      `image_path` varchar(1024) NOT NULL,
      `image_quality` varchar(20) DEFAULT NULL,
      `attribute` varchar(1024) DEFAULT NULL,
      `attribute_mapping` varchar(1024) DEFAULT NULL,
      `company` varchar(128) DEFAULT NULL,
      `result` varchar(1024) DEFAULT NULL,
      `result_mapping` varchar(1024) DEFAULT NULL,
      `compare_upper_wear` int(11) DEFAULT NULL,
      `compare_upper_color` int(11) DEFAULT NULL,
      `compare_lower_wear` int(11) DEFAULT NULL,
      `compare_lower_color` int(11) DEFAULT NULL,
      `compare_bag` int(11) DEFAULT NULL,
      `compare_headwear` int(11) DEFAULT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8"""
    try:
        cursor.execute(sql)  # 执行sql语句
        print("表创建成功")
    except:
        db.rollback()       # 如果发生错误则回滚
        print("sql语句有误")
    db.close()


if __name__ == '__main__':
    create_mysql_table()
