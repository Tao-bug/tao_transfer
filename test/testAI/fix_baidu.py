import requests
import base64
import json

from PIL import Image
from io import BytesIO


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


def change_img(file, maxwidth=4096, maxheight=4096, minwidth=48, minheight=48):
    image = Image.open(file)  # 读取图片
    w, h = image.size
    if minwidth <= w <= maxwidth and minheight <= h <= maxheight:
        # print('is OK.')
        scale = 1
        return image, scale
    elif (1.0 * w / maxwidth) > (1.0 * h / maxheight):
        scale = 1.0 * w / maxwidth
        new_img = image.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)
        return new_img, scale
    else:
        scale = 1.0 * h / maxheight
        new_img = image.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)
        return new_img, scale


class HumanAnalysis(object):
    """人体检测和属性识别"""

    def __init__(self):
        pass

    @staticmethod
    def get_file_content(filepath):
        # 图片处理
        image, scale = change_img(filepath)
        output = BytesIO()
        image.save(output, format='png')
        contents = output.getvalue()
        output.close()
        # print(base64.b64encode(contents))
        return base64.b64encode(contents), scale


def algorhtmReq(img_file):
    """获取token"""
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=P57FL8KbPcqFIIRWkLLYET3B&client_secret=4tk7hnTfm2E8iut56ITSciQ46klsRpgf'
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_attr"
    response = requests.get(host)
    access_token = None
    if response:
        access_token = response.json()["access_token"]

    clint = HumanAnalysis()
    image, scale = clint.get_file_content(img_file)
    params = {"image": image}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    datas = None
    if response:
        datas = json.loads(response.content)
    # print(datas)

    if "error_code" in datas.keys():
        error_result = {"error_msg": datas["error_msg"],
                        "error_code": datas["error_code"]}
        return json.dumps(error_result)

    # 构建统一格式
    dict_value = get_json_value_by_key(datas, 'person_info', results=[])[0]
    result_list = []
    # 识别人数
    total_dict = {'total_num': len(dict_value)}
    result_list.append(total_dict)

    for i in dict_value:
        # 构建统一字段
        attributes_dict = {"upper_wear": "Null", "upper_color": "Null", "lower_wear": "Null", "lower_color": "Null",
                           "bag": "Null", "headwear": "Null"}
        for key in attributes_dict:
            attributes_dict[key] = i['attributes'][key]['name']

        result_dict = {
            "position": [int(i['location']['top']/scale),
                         int(i['location']['left']/scale),
                         int(i['location']['width']/scale),
                         int(i['location']['height']/scale)],
            "score": i['location']['score'],
        }
        result_dict.update(attributes_dict)
        result_list.append(result_dict)

    result_list = json.dumps(result_list, ensure_ascii=False)
    return result_list


if __name__ == '__main__':

    # img_file = "/Users/tao/Desktop/testAI/images/20200608121731.jpg"
    img_file = "/Users/tao/Desktop/WechatIMG128.jpeg"
    # img_file = "/Users/tao/Desktop/testAI/images/123.png"
    # result = (algorhtmReq(img_file))
    result = json.loads(algorhtmReq(img_file))
    print(result)
