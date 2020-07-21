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


def change_img(file):
    img_switch = Image.open(file)  # 读取图片
    w, h = img_switch.size
    w_scale = w/1000
    h_scale = h/1000
    img_deal = img_switch.resize((1000, 1000), Image.ANTIALIAS)  # 转化图片
    img_deal = img_deal.convert('RGB')  # 保存为.jpg格式才需要
    return img_deal, w_scale, h_scale


def PIL_to_base64(image):
    output = BytesIO()
    image.save(output, format='png')
    contents = output.getvalue()
    output.close()
    string = base64.b64encode(contents)
    return string


def change_img1(file, max_width=4100, max_height=2196, min_width=1600, min_height=1800):
    # 800*600 px -- 4096*2160 px (但宽不能大于4096 px 且高不能大于2160 px)
    image = Image.open(file)  # 读取图片
    w, h = image.size
    print(w, h)
    if min_width <= w <= max_width and min_height <= h <= max_height:
        # print('is OK.')
        # image = image.convert('RGB')  # 保存为.jpg格式才需要
        scale = 1
        return image, scale
    elif (1.0 * w / max_width) > (1.0 * h / max_height):
        scale = 1.0 * w / max_width
        new_img = image.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)
        # new_img = new_img.convert('RGB')  # 保存为.jpg格式才需要
        print((int(w / scale), int(h / scale), scale), "1")
        return new_img, scale
    else:
        scale = 1.0 * h / max_height
        new_img = image.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)
        # new_img = new_img.convert('RGB')  # 保存为.jpg格式才需要
        print((int(w / scale), int(h / scale), scale), "2")
        return new_img, scale


def algorhtmReq(img_file):
    host = "https://open.ys7.com/api/lapp/token/get?appKey=ec387de50ca04b5ca3d10e5290ebb901&appSecret=5352271e3b6ed93928fcf2aa76072546"
    request_url = "https://open.ys7.com/api/lapp/intelligence/human/analysis/body"
    response = requests.post(host)
    access_token = None
    if response:
        access_token = response.json()["data"]["accessToken"]

    # 图片处理
    # 图片，分辨率范围：50W~900W像素，图片最大2M；
    # 图片大小 800*600 px -- 4096*2160 px (但宽不能大于4096 px 且高不能大于2160 px)
    # region, w, h = change_img(img_file)
    region, w, h = change_img(img_file)
    image_read = PIL_to_base64(region)
    string = image_read.decode('utf-8')
    # img = image_read.decode('utf-8')

    # img, scale = change_img1(img_file)
    # output = BytesIO()
    # img.save(output, format='png')
    # contents = output.getvalue()
    # output.close()
    # string = base64.b64encode(contents).decode('utf-8')

    # params = {"image": img}
    # print(img)
    params = {"image": string}
    request_url = "%s?accessToken=%s&dataType=1" % (request_url, access_token)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    datas = None
    if response:
        datas = json.loads(response.content)
    # print(datas)

    # 构建统一格式
    dict_value = get_json_value_by_key(datas, 'data', results=[])[0]
    result_list = []
    # 识别人数
    total_dict = {'total_num': len(dict_value)}
    result_list.append(total_dict)

    for i in dict_value:
        position = i.pop('rect')
        # 构建统一字段
        attributes_dict = {"upper_wear": i['jacetType']['des'],
                           "upper_color": i['jacetColor']['des'],
                           "lower_wear": i['trousersType']['des'],
                           "lower_color": i['trousersColor']['des'],
                           "bag": i['bag']['des'],
                           "headwear": i['hat']['des']}
        result_dict = {
            "position": [int(position['x']/w), int(position['y']/h), int(position['width']/w), int(position['height']/h)],
            # "position": [int(position['x']/scale), int(position['y']/scale), int(position['width']/scale), int(position['height']/scale)],
            # "position": [position['x'], position['y'], position['width'], position['height']],
            "score": "Null"
        }
        result_dict.update(attributes_dict)
        result_list.append(result_dict)
    # print(result_list)
    result_list = json.dumps(result_list, ensure_ascii=False)
    return result_list


if __name__ == '__main__':
    # img_file = '/Users/tao/Desktop/testAI/images/2b81f41104cf3b31673a2a4227a3f35.jpg'
    img_file = '/Users/tao/Desktop/testAI/images/123.png'
    # img_file = r"/Users/tao/Desktop/test/test_dataset/APY181031001/Square0001_001_002_39744.jpg"
    # img_file = '/Users/tao/Desktop/testAI/images/c7b84b32578624c1556adaae765bf62.jpg'  # detect no face
    # img_file = '/Users/tao/Desktop/test/test_dataset/test/CAM17-2014-03-05-20140305114713-20140305115201-tarid371-frame3150-line1.png'
    # img_file = '/Users/tao/Desktop/testAI/images/20200608121731.jpg'
    # img_file = '/Users/tao/Desktop/test/test_dataset/face'
    # img_file = '/Users/tao/Desktop/WechatIMG128.jpeg'
    # img_list = os.listdir(img_file)
    # for i in img_list:
    #     img_path = os.path.join(img_file, i)
    result = algorhtmReq(img_file)
    # print(result)
