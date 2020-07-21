import requests
import json
import base64


def get_json_value_by_key(in_json, target_key, results=None):
    """字典,列表,元组的多类型嵌套"""
    if results is None:
        results = []
    if isinstance(in_json, dict):  # 如果输入数据的格式为dict
        for key in in_json.keys():  # 循环获取key
            data = in_json[key]
            get_json_value_by_key(data, target_key, results=results)  # 回归当前key对于的value

            if key == target_key:  # 如果当前key与目标key相同就将当前key的value添加到输出列表
                results.append(data)

    elif isinstance(in_json, list) or isinstance(in_json, tuple):  # 如果输入数据格式为list或者tuple
        for data in in_json:  # 循环当前列表
            get_json_value_by_key(data, target_key, results=results)  # 回归列表的当前的元素
    return results


def algorhtmReq(image_file):

    url = "http://172.29.168.163/ivr/v1/human_attribute_recognition?access_token="

    token = 'b0a36e186445a3a86e44c7d70fdab5f9.1591761679'

    with open(image_file, "rb") as f:
        img = base64.b64encode(f.read())
    url = url + token

    params = {}
    re = requests.post(url, data={"image": img})
    datas = json.loads(re.content)
    data = datas.get('data')
    code = datas.get('code')
    msg = datas.get('msg')

    print("code=", code, " msg=", msg, " data=", data)
    # data= {'attribute': [{'age': 'old', 'backpack': 'no', 'bag': 'no', 'boots': 'yes', 'downColor': 'blue',
    # 'downShort': 'no', 'downType': 'Pattern', 'facing': 'front', 'glasses': 'yes', 'handbag': 'no', 'hat': 'no',
    # 'holdObjectFront': 'no', 'isFemale': 'no', 'longHair': 'no', 'lowClothPants': 'yes', 'shoesLight': 'no',
    # 'topLong': 'no', 'upColor': 'black', 'upShort': 'yes', 'upType': 'normal', 'xmax': 0.9097859327217125,
    # 'xmin': 0.7018348623853211, 'ymax': 1.6256830601092895, 'ymin': 0.3797814207650273}, ]
    # stander_attributes_dict = {'backpack': '有', 'bag': '有', 'downShort': 'downShort', 'handbag': '有', 'hat': 'hat',
    #                            'lowClothPants': 'lowClothPants', 'topLong': 'topLong', 'upShort': 'upShort'}

    # 构建统一格式
    dict_value_list = data["attribute"]
    result_list = []
    # 识别人数
    total_dict = {'total_num': len(dict_value_list)}
    result_list.append(total_dict)
    for i in dict_value_list:
        # 构建统一字段
        attributes_dict = {"upper_wear": "Null", "upper_color": "Null", "lower_wear": "Null", "lower_color": "Null",
                           "bag": "Null", "headwear": "Null"}
        # upper_wear
        upper_wear_dict = {'topLong': 'topLong', 'upShort': 'upShort'}
        # for key in ["topLong", "upShort"]:
        for key in upper_wear_dict:
            if i[key] == "yes":
                attributes_dict["upper_wear"] = upper_wear_dict[key]
        # upper_color
        attributes_dict["upper_color"] = i["upColor"]
        # lower_wear
        # for key in ["downShort", "lowClothPants"]:
        if i["lowClothPants"] == "yes" and i["downShort"] == "yes":
            attributes_dict["lower_wear"] = "短裤"
        elif i["lowClothPants"] == "yes" and i["downShort"] == "no":
            attributes_dict["lower_wear"] = "长裤"
        elif i["lowClothPants"] == "no":
            attributes_dict["lower_wear"] = "裙子"
        else:
            attributes_dict["lower_wear"] = "未知"
        # lower_color
        attributes_dict["lower_color"] = i["downColor"]
        # bag
        if i["backpack"] == i["bag"] == i["handbag"] == "no":
            attributes_dict["bag"] = "无"
        else:
            attributes_dict["bag"] = "有"
        # headwear
        attributes_dict["headwear"] = i["hat"]

        result_dict = {"position": [i["xmin"], i["ymax"], i["xmax"]-i["xmin"], i["ymax"]-i["ymin"]], "score": "Null"}

        result_dict.update(attributes_dict)
        result_list.append(result_dict)
    result_list = json.dumps(result_list, ensure_ascii=False)
    return result_list


if __name__ == '__main__':
    import os
    import time
    img_path = "/home/cmcc/tao_file/tao_transfer/test/test_dataset/rap/"
    img_list = os.listdir(img_path)
    if ".DS_Store" in img_list:
        img_list.remove(".DS_Store")
    img_list.sort()
    for i in img_list[:2]:
        print(i)
        img_file = os.path.join(img_path, i)
        result = algorhtmReq(img_file)
        print(result)
        time.sleep(1)
