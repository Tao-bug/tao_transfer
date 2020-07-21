import hashlib
import time
import json

from PIL import Image
from io import BytesIO
from wx_sdk import wx_sdk


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


def change_img(file, max_width=2048, max_height=2048, min_width=256, min_height=256):
    image = Image.open(file)  # 读取图片
    w, h = image.size
    if min_width <= w <= max_width and min_height <= h <= max_height:
        # print('is OK.')
        scale = 1
        return image, scale
    elif (1.0 * w / max_width) > (1.0 * h / max_height):
        scale = 1.0 * w / max_width
        new_img = image.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)
        # print((int(w / scale), int(h / scale)))
        return new_img, scale
    else:
        scale = 1.0 * h / max_height
        new_img = image.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)
        # print((int(w / scale), int(h / scale)))
        return new_img, scale


def algorhtmReq(img_file):
    url = 'https://aiapi.jd.com/jdai/human_parsing'

    timestamp = int(time.time() * 1000)
    secretkey = 'ec03b15d7a598e4df6f2ec3cb337c692'

    # sign = hashlib.md5(b'').hexdigest()
    sign_str = secretkey + str(timestamp)
    hl = hashlib.md5()
    hl.update(sign_str.encode(encoding='utf-8'))
    sign = hl.hexdigest()

    params = {
        'muti_det': '2',
        'appkey': '6fde81e80d9b58f9e8e1cdff64f1f74b',
        'timestamp': timestamp,
        'sign': sign
    }

    img_file, scale = change_img(img_file)
    output = BytesIO()
    img_file.save(output, format='png')
    contents = output.getvalue()
    output.close()

    # response = wx_sdk.wx_post_req(url, params, img=img_file)
    response = wx_sdk.wx_post_req(url, params, bodyStr=contents)
    datas = json.loads(response.text)
    # print(datas)

    # 构建统一格式
    dict_value = get_json_value_by_key(datas, 'result', results=[])[0]

    result_list = []
    # 识别人数
    total_dict = {'total_num': len(dict_value['humanDetectionResult'])}
    result_list.append(total_dict)

    for i in range(len(dict_value['humanDetectionResult'])):
        # 从图像数组中特征提取
        stander = {1: '帽子', 5: '上衣', 6: '连衣裙', 7: '大衣', 9: '短裤', 10: '连体裤', 12: '裙子', }
        stander_key = {1: 'hat', 5: 'upper_wear', 6: 'upper_wear', 7: 'upper_wear', 9: 'lower_wear', 10: 'lower_wear',
                       12: 'lower_wear', }
        stander_dict = {}
        for j in stander.keys():
            # print(j)
            for k in dict_value['humanParsingResult'][i]:
                if j in k:
                    stander_dict[stander_key[j]] = stander[j]
                    break
        # 构建统一字段
        attributes_dict = {"upper_wear": "Null", "upper_color": "Null", "lower_wear": "Null", "lower_color": "Null",
                           "bag": "Null", "headwear": "no"}
        for key in stander_dict:
            attributes_dict[key] = stander_dict[key]

        result_dict = {
            "position": [int(j/scale) for j in dict_value['humanDetectionResult'][i][:4]],
            "score": dict_value['humanDetectionResult'][i][-1],
        }
        result_dict.update(attributes_dict)
        result_list.append(result_dict)
    result_list = json.dumps(result_list)
    return result_list


if __name__ == '__main__':
    # img_file = '/Users/tao/Desktop/testAI/images/2b81f41104cf3b31673a2a4227a3f35.jpg'  # 上传图片的位置
    img_file = '/Users/tao/Desktop/testAI/images/123.png'
    result = algorhtmReq(img_file)
    print(result)
