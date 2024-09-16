import requests
import json

username = "laowang"  # 替换为你的IAM用户名
password = "lkwn36257?@"  # 替换为你的IAM密码
account_name = "chenghejun"  # 替换为IAM用户所属账号名
region_name = "cn-southwest-2"  # 替换为项目区域名称

# 请求URL和Headers
url = "https://iam.cn-southwest-2.myhuaweicloud.com/v3/auth/tokens"  # 修改区域为你的实际区域
headers = {
    "Content-Type": "application/json"
}

# 构建请求体
payload = {
    "auth": {
        "identity": {
            "methods": ["password"],
            "password": {
                "user": {
                    "name": username,
                    "password": password,
                    "domain": {
                        "name": account_name
                    }
                }
            }
        },
        "scope": {
            "project": {
                "name": region_name
            }
        }
    }
}

# 发起请求获取Token
response = requests.post(url, headers=headers, data=json.dumps(payload))

print("正在获取Token中，请稍等...")

# 检查请求是否成功并输出结果
if response.status_code == 201:
    token = response.headers.get("X-Subject-Token")
    print("你的Token:")
    print(f"{token}")
else:
    print(f"Failed to get token: {response.text}")
