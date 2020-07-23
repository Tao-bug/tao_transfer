from wx_sdk import wx_sdk

url = 'https://aiapi.jd.com/jdai/personreid'
img = '/Users/tao/Desktop/testAI/images/123.png'  # 上传图片的位置
params = {
    'appkey': 'ae10355bd01d00c6602cf4a44c4f7394',
    'secretkey': '43651bd472ba4f0c2c2f4ebd7a6f5d07'
}

response = wx_sdk.wx_post_req(url, params, img=img)
print(response.text)
