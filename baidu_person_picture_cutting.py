import requests
import base64
import json
import os

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


def save_data(save_path, data):
    save_path = os.path.join(save_path, "data.json")
    # data = {"a": 1}
    with open(save_path, "a") as f:
        f.write(json.dumps(data, ensure_ascii=False))
        f.write("\n")


def algorhtmReq(img_file):
    """获取token"""
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    # host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=3cvIcGN5V4LXgSCS59FE83CK&client_secret=xnNWhDM2D9bXIK971y38dzXjDfX33IH4'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=QFyO3Ndq6DZzlBXyHdBKxskV&client_secret=uYnY1XVwjWEdakq7pMGODP7p6xWcVYio'
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
    # 保存原始数据
    data_dict = {img_file: datas}
    save_path = os.path.join(os.getcwd(), "out/")
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_data(save_path, data_dict)

    if "error_code" in datas.keys():
        error_result = {"error_msg": datas["error_msg"],
                        "error_code": datas["error_code"]}
        print("出错了", error_result)
        return

    # 截取人体框
    image, scale = change_img(img_file)
    # 人体框数量
    person_num = datas["person_num"]
    dict_value = get_json_value_by_key(datas, 'person_info', results=[])[0]
    for num in range(person_num):
        # location {'score': 0.9729551672935486, 'top': 321, 'left': 858, 'width': 191, 'height': 499}
        # print(dict_value[num]["location"])
        # if dict_value[num]["location"]["score"] < 0.2:
        #     continue
        x = dict_value[num]["location"]["left"]*scale
        y = dict_value[num]["location"]["top"]*scale
        w = dict_value[num]["location"]["width"]*scale
        h = dict_value[num]["location"]["height"]*scale

        # region = image.crop((a, b, a + c, b + d))
        region = image.crop((x, y, x + w, y + h))
        # 保存图片
        name = img_file.split("/")[-3] + "_" + img_file.split("/")[-2] + "_" + img_file.split("/")[-1].split(".")[0] + "_" + str(num)
        image_name = "score_" + str(int(dict_value[num]["location"]["score"]*100)) + "_" + name + ".png"
        save_image_path = os.path.join(save_path, image_name)
        region.save(save_image_path, "png")


def run():
    data_path = "/Users/tao/Desktop/testAI_many_persons/test_dataset/data/"
    # 拼接图片路径列表
    data_list = os.listdir(data_path)
    data_path_list = [os.path.join(data_path, data) for data in data_list]
    # print(len(data_path_list))
    img_path_list = []
    for data in data_path_list[8:]:
        img_list = [os.path.join(data, img) for img in os.listdir(data)]
        img_path_list.extend(img_list)
    img_path_list.sort()
    print(len(img_path_list))

    # 遍历图片
    for img_file in img_path_list[:]:
        if img_file.split(".")[-1] not in ["jpg", "png"]:
            continue
        print(img_file)
        algorhtmReq(img_file)


if __name__ == '__main__':
    run()
