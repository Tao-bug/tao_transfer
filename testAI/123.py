#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : 123.py
@Time    : 2020/7/23 下午8:33
@Author  : XXX
@Email   : XXXX@163.com
@Software: PyCharm
"""
import json


with open("query_json/query_attributes_dict.json", "r") as j:
    data = j.read()
    
data = json.loads(data)

for key in data:
    if not data[key]:
        print(key)
        with open("query_json/err.log", "a") as e:
            e.write(key + ".jpg,")


