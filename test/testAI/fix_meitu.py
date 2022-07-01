import requests
import base64
import json
import time
from io import BytesIO
from PIL import Image


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

    elif isinstance(in_json, (list, tuple)):  # 如果输入数据格式为list或者tuple
        for data in in_json:  # 循环当前列表
            get_json_value_by_key(data, target_key, results=results)  # 回归列表的当前的元素
    return results


def change_img(file, maxwidth=1280, maxheight=1280, minwidth=48, minheight=48):
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


def PIL_to_base64(image):
    output = BytesIO()
    image.save(output, format='png')
    contents = output.getvalue()
    output.close()
    return base64.b64encode(contents)


def algorhtmReq(img_file):
    # 人体框检测
    img = Image.open(img_file)
    # img, scale = change_img(img_file)

    image = open(img_file, 'rb')
    image_read = image.read()
    image_64_encode = base64.b64encode(image_read).decode('utf-8')
    ss = json.dumps(
        {
            "parameter": {
                "rsp_media_type": "jpg",
            },
            "extra": {},
            "media_info_list": [{
                "media_data": image_64_encode,
                "media_profiles": {
                    "media_data_type": "jpg"
                },
                "media_extra": {
                }
            }]
        }
    )
    # print(ss)

    # AIBeauty_url = "https://openapi.mtlab.meitu.com/v1/HumanDetect?api_key=jX5MVzXFR5QJbTBrM5_0oKWRtEPhxopT&api_secret=85Tg83j_Psxe1B3CRFTybR4VFTO98FGB"
    AIBeauty_url = "https://openapi.mtlab.meitu.com/v1/HumanDetect?api_key=NVU00gBh199yQl1qhb_aXwAaeyCXn48e&api_secret=srrQmOIvzShECalRMrI4pQ4X6C54d_XH"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(AIBeauty_url, data=ss, headers=headers)
    ss2 = response.json()
    # print('人体框检测', ss2, type(ss2))
    # print(response.status_code)

    # 构建统一格式
    dict_value = get_json_value_by_key(ss2, 'HumanDetect', results=[])[0]  # 位置信息

    result_list = [{'total_num': 0}]
    for i in dict_value:
        # 超过当前限制qps--访问过快
        time.sleep(0.5)
        a, b, c, d = i
        region = img.crop((a, b, a + c, b + d))
        # print((a, b, a + c, b + d))

        #  服饰识别
        image_read = PIL_to_base64(region)
        image_64_encode = image_read.decode('utf-8')
        ss = json.dumps(
            {
                "parameter": {
                    "rsp_media_type": "jpg",
                },
                "extra": {},
                "media_info_list": [{
                    "media_data": image_64_encode,
                    "media_profiles": {
                        "media_data_type": "jpg"
                    },
                    "media_extra": {
                    }
                }]
            }
        )
        # AIBeauty_url = "https://openapi.mtlab.meitu.com/v1/apperal?api_key=jX5MVzXFR5QJbTBrM5_0oKWRtEPhxopT&api_secret=85Tg83j_Psxe1B3CRFTybR4VFTO98FGB"
        AIBeauty_url = "https://openapi.mtlab.meitu.com/v1/apperal?api_key=NVU00gBh199yQl1qhb_aXwAaeyCXn48e&api_secret=srrQmOIvzShECalRMrI4pQ4X6C54d_XH"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(AIBeauty_url, data=ss, headers=headers)
        ss2 = response.json()
        # print('服饰识别', ss2)
        # print(response.status_code)

        # if response.status_code != 200:
        #     continue

        result_list[0]['total_num'] += 1

        style = {0: "T恤", 1: "衬衫", 2: "毛衣", 3: "卫衣", 4: "风衣", 5: "外套", 6: "牛仔夹克", 7: "棒球服式外套", 8: "正装", 9: "大衣",
                 10: "棉服", 11: "皮夹克"}
        sleeve = {0: "长袖", 1: "短袖", 2: "无袖背心", 3: "吊带", 4: "未知"}
        wear_dic = get_json_value_by_key(ss2, "cloth_type", results=[])[0]
        # 构建统一字段
        attributes_dict = {"upper_wear": [style[wear_dic[0]['type']], sleeve[wear_dic[2]['type']]],
                           # "sleeve": sleeve[wear_dic[2]['type']],
                           "upper_color": "Null", "lower_wear": "Null",
                           "lower_color": "Null",
                           "bag": "Null",
                           "headwear": "Null"}
        result_dict = {
            "position": i,
            "score": "Null",
        } | attributes_dict

        result_list.append(result_dict)

    result_list = json.dumps(result_list, ensure_ascii=False)
    return result_list


if __name__ == "__main__":
    import os
    img_file = '/Users/tao/Desktop/testAI/images/123.png'
    # img_file = '/Users/tao/Desktop/WechatIMG5.png'
    # img_file = '/Users/tao/Desktop/testAI/images/c7b84b32578624c1556adaae765bf62.jpg'  # detect no face
    # img_file = '/Users/tao/Desktop/test/test_dataset/test/CAM17-2014-03-05-20140305114713-20140305115201-tarid371-frame3150-line1.png'
    # img_file = '/Users/tao/Desktop/test/test_dataset/rap/CAM01-2013-12-23-20131223120147-20131223120735-tarid7-frame781-line1.png'

    # img_file = '/Users/tao/Desktop/test/test_dataset/face2/'
    # img_list = os.listdir(img_file)
    # for i in img_list:
    #     print(i)
    #     img_path = os.path.join(img_file, i)
    result = algorhtmReq(img_file)
    print(result)
