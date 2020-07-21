import requests
import json
import base64

url = "http://172.29.168.163/ivr/v1/human_attribute_recognition?access_token="

token = 'b0a36e186445a3a86e44c7d70fdab5f9.1591761679'

with open("C:/Users/cmcc/Desktop/1.jpg", "rb") as f:
    base64 = base64.b64encode(f.read())
url = url + token

params = {}
re = requests.post(url, data={"image": base64})
datas = json.loads(re.content)
data = datas.get('data')
code = datas.get('code')
msg = datas.get('msg')

print("code=", code, " msg=", msg, " data=", data)