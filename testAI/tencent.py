from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.bda.v20200324 import bda_client, models
import os
import base64

# os.environ['https_proxy'] = 'proxy.cmcc:8080'
# os.environ['http_proxy'] = 'proxy.cmcc:8080'

# """创建人体库"""
# try:
#     cred = credential.Credential("AKID1tWtpVyXw6sOeecsVM4WnpcFgBQNvDLD", "FyRebL1RbYN3TfeNpsiyEXZLrZ5LSbTA")
#     httpProfile = HttpProfile()
#     httpProfile.endpoint = "bda.tencentcloudapi.com"
#
#     clientProfile = ClientProfile()
#     clientProfile.httpProfile = httpProfile
#     client = bda_client.BdaClient(cred, "ap-beijing", clientProfile)
#
#     req = models.CreateGroupRequest()
#     params = '{\"GroupName\":\"bodySearch\",\"GroupId\":\"1111111\"}'
#     req.from_json_string(params)
#
#     resp = client.CreateGroup(req)
#     print(resp.to_json_string())
#
# except TencentCloudSDKException as err:
#     print(err)

# f = open('/Users/tao/Desktop/testAI/images/20200608121731.jpg', 'rb')
f = open('/Users/tao/Desktop/testAI/similar_images/0194_c1s1_060131_05.jpg', 'rb')
# print(f)
img = base64.b64encode(f.read()).decode('ascii')
# print(img)
"""创建人员"""
# try:
#     cred = credential.Credential("AKID1tWtpVyXw6sOeecsVM4WnpcFgBQNvDLD", "FyRebL1RbYN3TfeNpsiyEXZLrZ5LSbTA")
#     httpProfile = HttpProfile()
#     httpProfile.endpoint = "bda.tencentcloudapi.com"
#
#     clientProfile = ClientProfile()
#     clientProfile.httpProfile = httpProfile
#     client = bda_client.BdaClient(cred, "ap-beijing", clientProfile)
#
#     req = models.CreatePersonRequest()
#     params = '{\"GroupId\":\"1111111\",\"PersonName\":\"testBBodySearch1\",\"PersonId\":\"BodySearch-1\",\"Trace\":{\"Images\":[\""]}}'
#     req.from_json_string(params)
#
#     resp = client.CreateTrace(req)
#     print(resp.to_json_string())
#
# except TencentCloudSDKException as err:
#     print(err)


"""人体搜索"""
try:
    cred = credential.Credential("AKID1tWtpVyXw6sOeecsVM4WnpcFgBQNvDLD", "FyRebL1RbYN3TfeNpsiyEXZLrZ5LSbTA")
    httpProfile = HttpProfile()
    httpProfile.endpoint = "bda.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = bda_client.BdaClient(cred, "ap-beijing", clientProfile)

    req = models.SearchTraceRequest()
    params = '{\"GroupId\":\"1111111\",\"Trace\":{\"Images\":[\"' + img + '\"],\"BodyRects\":[{\"X\":473,\"Y\":182,\"Width\":100,\"Height\":180}]}}'
    # params=params.replace('img',str(img))
    print(params)
    req.from_json_string(params)
    print(req)
    resp = client.SearchTrace(req)
    print(resp.to_json_string())

except TencentCloudSDKException as err:
    print(err)
