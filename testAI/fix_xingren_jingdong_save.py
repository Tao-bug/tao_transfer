import hashlib
import time
import json
import os

from PIL import Image
from io import BytesIO
from wx_sdk import wx_sdk


def get_json_value_by_key(in_json, target_key, results=[]):
    """字典,列表,元组的多类型嵌套"""
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


def change_img(file, max_width=800, max_height=800, min_width=300, min_height=300):
    image = Image.open(file)  # 读取图片
    w, h = image.size
    if min_width <= w <= max_width and min_height <= h <= max_height:
        # print('is OK.')
        scale = 1
        new_img = image
    elif (1.0 * w / max_width) > (1.0 * h / max_height):
        scale = 1.0 * w / max_width
        new_img = image.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)
        # print((int(w / scale), int(h / scale)), "1")
    else:
        scale = 1.0 * h / max_height
        new_img = image.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)
        # print((int(w / scale), int(h / scale)), "2")

    output = BytesIO()
    new_img.save(output, format='png')
    contents = output.getvalue()
    output.close()
    return contents, scale


def algorhtmReq(img_file, params_tuple):
    url = 'https://aiapi.jd.com/jdai/personreid'
    timestamp = int(time.time() * 1000)
    # secretkey = '8569938395247b228a1e356bf40d89bc'
    secretkey = params_tuple[0]

    sign_str = secretkey + str(timestamp)
    hl = hashlib.md5()
    hl.update(sign_str.encode(encoding='utf-8'))
    sign = hl.hexdigest()

    params = {
        'muti_det': '2',
        # 'appkey': '30598bbc33f844e4cf33bfc77181a616',
        'appkey': params_tuple[1],
        'timestamp': timestamp,
        'sign': sign
    }

    # image size must be between 256X256 and 4096X4096
    # image size exceeds 2M
    contents, scale = change_img(img_file)

    # response = wx_sdk.wx_post_req(url, params, img=img_file)
    response = wx_sdk.wx_post_req(url, params, bodyStr=contents)
    datas = json.loads(response.text)
    # print(datas)
    if datas["code"] != "10000":
        print(datas["msg"])
    if datas["result"]["status"] != 0:
        print(datas["result"]["message"])
    # 构建统一格式
    # attributes
    attributes = get_json_value_by_key(datas, 'personreidResult', results=[])[0]
    # print(attributes)

    # 位置信息--x1,y1,x2,y2,score分别表示预测出的人体矩形框的左上角坐标，右下角坐标，以及置信度。
    # 返归的矩形框按照置信度高低排序，当未检测到人体时，返回空array[]
    dict_value = get_json_value_by_key(datas, 'humanDetectionResult', results=[])[0]
    # print(dict_value)  # [[317, 16, 785, 1399, 0.9080960154533386]]
    result_list = []
    # 识别人数
    total_dict = {'total_num': len(dict_value)}
    result_list.append(total_dict)

    for i in range(len(dict_value)):
        result_dict = {
            "position": [int(j/scale) for j in dict_value[i][:4]],
            "score": dict_value[i][-1],
            'attributes': attributes[i]
        }
        result_list.append(result_dict)

    # print(result_list)
    return result_list


def save_attributes(image_path, number, params_tuple):
    with open("query_json/query_attributes_dict.json", "r") as f:
        data = f.read()
    data = json.loads(data)
    print("初始记录的图片数：", len(data))

    image_list = os.listdir(image_path)
    if ".DS_Store" in image_list:
        image_list.remove(".DS_Store")
    if "Thumbs.db" in image_list:
        image_list.remove("Thumbs.db")
    image_list.sort()
    attributes_dict = {}
    for img in image_list[len(data):number]:
        print(img)
        image_index = img.split(".")[0]
        try:
            attributes = algorhtmReq(os.path.join(image_path, img), params_tuple)
            attributes_dict[image_index] = attributes
        except Exception as e:
            attributes_dict[image_index] = []
            err_data = img + ","
            print("有异常", e)
            # 记录异常图片名字
            with open("query_json/err.log", "a") as err:
                err.write(err_data)
    # print(attributes_dict)
    data.update(attributes_dict)
    print("已经记录的图片数：", len(data))
    attributes_dict = json.dumps(data)
    save_path = "query_json/query_attributes_dict.json"
    with open(save_path, "w") as f:
        f.write(attributes_dict)
    print("记录完成")


if __name__ == '__main__':
    # (secretkey, appkey)
    params_dict = {0: ("8569938395247b228a1e356bf40d89bc", "30598bbc33f844e4cf33bfc77181a616"),  # 自己
                   1: ("ba80ca6c6f4bbf35a1c2692e9f879430", "542c18a0f3bcbe4b3fd0be5a7c3cf544"),
                   2: ("19599754bcc377cfffb2d7ad1b7bdea4", "35939ef5e77e2cb6072d73674baae58e"),
                   3: ("ec03b15d7a598e4df6f2ec3cb337c692", "6fde81e80d9b58f9e8e1cdff64f1f74b"),  # 华姐
                   4: ("22c61b1aab019b3604b0a101f1cf49d6", "4b1f76865cc2aecb240be43e3590cf06"),
                   5: ("05c7ce454b4938310c7e62846235ee3d", "6f0f0bf38039326c9831dd15d0257f4a"),
                   6: ("ff6f9e8e0907368210562e98b156d156", "ba1579bca4dd55991e0e1b4795313f32"),  # 陈阳
                   7: ("45fb54eef131e15a590b29df37369091", "7a88006075dc94f30a5d106bba9b266d"),
                   8: ("fd003cd2d0c7aa245ff80a43647a50a6", "f61d2042090948753bb07bdc810d0a62"),
                   9: ("28946001a9afe55ec83c74965deeaceb", "75515088f0d7bb94f1c4b05ec832e625"),  #
                   10: ("c07d0fdef0acb0a075e0502c4e085a93", "8e4c1e8694b70e06256cb0c1486fec1f"),  #
                   }

    # for params in params_dict:
    # for params in [1, 2, 4, 5, 7, 8, 9]:  #
    for params in range(8, 9):  #
        path = "/Users/tao/Desktop/Person-Attribute-Recognition-MarketDuke/dataset/Market-1501/query"
        # 第几张了
        num = 1500
        # 保存attributes
        save_attributes(path, num, params_dict[params])

    # path = "/Users/tao/Desktop/Person-Attribute-Recognition-MarketDuke/dataset/Market-1501/query/0021_c5s1_002176_00.jpg"
    # path = "/Users/tao/Desktop/testAI/similar_images/0194_c1s1_060031_01.jpg"
    # algorhtmReq(path)

