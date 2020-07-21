import urllib.request
import urllib.error
import time
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


def algorhtmReq(img_file):
    http_url = 'https://api-cn.faceplusplus.com/humanbodypp/v1/detect'
    key = "Isz8av-cOGPGWASSF57lp1l1L1JroyK5"
    secret = "jWqDp_3M_VTOPROnrR98U-_ul8uwPb_D"

    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    data.append('--%s' % boundary)
    # 图片处理
    # 图片要求
    # 图片格式：JPG(JPEG)，PNG
    # 图片像素尺寸：最小 48*48 像素，最大 1280*1280 像素
    # 图片文件大小：2 MB
    image, scale = change_img(img_file)
    output = BytesIO()
    image.save(output, format='png')
    contents = output.getvalue()
    output.close()

    data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(contents)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
    data.append('1')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
    data.append(
        "gender,upper_body_cloth,lower_body_cloth")
    data.append('--%s--\r\n' % boundary)

    for i, d in enumerate(data):
        if isinstance(d, str):
            data[i] = d.encode('utf-8')

    http_body = b'\r\n'.join(data)

    # build http request
    req = urllib.request.Request(url=http_url, data=http_body)

    # header
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)

    try:
        # post data to server
        resp = urllib.request.urlopen(req, timeout=5)
        # get response
        qrcont = resp.read()
        # if you want to load as json, you should decode first,
        # for example: json.loads(qrount.decode('utf-8'))
        datas = json.loads(qrcont.decode('utf-8'))
        # print(datas)
    except urllib.error.HTTPError as e:
        # print(e.read().decode('utf-8'))
        return e.read().decode('utf-8')

    # 构建统一格式
    dict_value = get_json_value_by_key(datas, 'humanbodies', results=[])[0]  # 位置信息
    result_list = []
    # 识别人数
    total_dict = {'total_num': len(dict_value)}
    result_list.append(total_dict)
    for i in dict_value:
        # 构建统一字段
        attributes_dict = {"upper_wear": "Null",
                           "upper_color": i['attributes']['upper_body_cloth']['upper_body_cloth_color'],
                           "lower_wear": "Null",
                           "lower_color": i['attributes']['lower_body_cloth']['lower_body_cloth_color'],
                           "bag": "Null",
                           "headwear": "Null"}

        position = i.pop('humanbody_rectangle')
        confidence = i.pop('confidence')
        result_dict = {
            "position": [int(position['top'] / scale),
                         int(position['left'] / scale),
                         int(position['width'] / scale),
                         int(position['height'] / scale)],
            "score": confidence,
        }
        result_dict.update(attributes_dict)
        result_list.append(result_dict)

    result_list = json.dumps(result_list)
    return result_list


if __name__ == '__main__':
    # img_file = r"/Users/tao/Desktop/testAI/images/20200608121731.jpg"
    # img_file = r"/Users/tao/Desktop/testAI/images/123.png"
    img_file = r"/Users/tao/Desktop/test/test_dataset/test2/CAM01-2013-12-23-20131223120147-20131223120735-tarid3-frame493-line1.png"
    # img_file = r"/Users/tao/Desktop/testAI/images/2b81f41104cf3b31673a2a4227a3f35.jpg"
    result = algorhtmReq(img_file)
    print(result)
