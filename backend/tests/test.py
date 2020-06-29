# coding=utf-8
# auther：Liul5
# date：10/12/2019 11:04 AM
# tools：PyCharm
# Python：3.7.3

import requests
import json

url = "http://10.212.42.180:5000/api/v1/users/test"

payload = {
    "username": "lucas",
    "password": "1234"
}
headers = {
    'Content-Type': "application/json",
    }

response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

print(response.text)