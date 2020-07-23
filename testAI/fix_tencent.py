from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.bda.v20200324 import bda_client, models
import os
import base64
from PIL import Image
from io import BytesIO


def change_img(file, max_width=1000, max_height=1500, min_width=600, min_height=600):
    image = Image.open(file)  # 读取图片
    w, h = image.size
    if min_width <= w <= max_width and min_height <= h <= max_height:
        print('is OK.')
        scale = 1
        # image = image.convert('RGB')  # 保存为.jpg格式才需要
        new_img = image
    elif (1.0 * w / max_width) > (1.0 * h / max_height):
        scale = 1.0 * w / max_width
        new_img = image.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)
        # image = new_img.convert('RGB')  # 保存为.jpg格式才需要
        print((int(w / scale), int(h / scale)), "1")
    else:
        scale = 1.0 * h / max_height
        new_img = image.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)
        # image = new_img.convert('RGB')  # 保存为.jpg格式才需要
        print((int(w / scale), int(h / scale)), "2")

    output = BytesIO()
    new_img.save(output, format='png')
    contents = output.getvalue()
    output.close()

    # new_img.save("123_new.jpg")
    return contents, scale


def algorhtmReq(image_file):
    # f = open(image_file, 'rb')
    # print(type(f))
    contents, scale = change_img(image_file)
    img = base64.b64encode(contents).decode('ascii')
    # img = base64.b64encode(f.read()).decode('ascii')
    # print(img)
    # print(type(img))
    """人体搜索"""
    try:
        cred = credential.Credential("AKID1tWtpVyXw6sOeecsVM4WnpcFgBQNvDLD", "FyRebL1RbYN3TfeNpsiyEXZLrZ5LSbTA")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "bda.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法
        clientProfile.httpProfile = httpProfile
        client = bda_client.BdaClient(cred, "ap-beijing", clientProfile)

        req = models.SearchTraceRequest()
        params = '{\"GroupId\":\"1111111\",\"Trace\":{\"Images\":[\"' + img + '\"],\"BodyRects\":[{\"X\":473,\"Y\":182,\"Width\":100,\"Height\":180}]}}'
        # params=params.replace('img',str(img))
        # print(params)
        req.from_json_string(params)
        # print(req)
        resp = client.SearchTrace(req)
        respond = eval(resp.to_json_string())
        msg_dict = {-1001: "输入图片不合法", -1002: "输入图片不能构成轨迹"}
        if respond["InputRetCode"] in msg_dict:
            print(msg_dict[respond["InputRetCode"]])
        else:
            print(respond)
    except TencentCloudSDKException as err:
        print(err)


if __name__ == '__main__':
    # img_file = "/Users/tao/Desktop/testAI/images/20200608121731.jpg"
    # img_file = "/Users/tao/Desktop/testAI/similar_images/1005_c6s2_123918_01.jpg"
    img_file = "/Users/tao/Desktop/Person-Attribute-Recognition-MarketDuke/dataset/Market-1501/query/0004_c6s3_089492_00.jpg"
    # img_file = "/Users/tao/Desktop/testAI/similar_images/1029_c3s2_133319_02.jpg"
    # change_img(img_file)
    # img_file = "/Users/tao/Desktop/testAI/123_new.jpg"
    algorhtmReq(img_file)
