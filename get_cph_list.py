# coding: utf-8

import os
import json
from dotenv import load_dotenv
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcph.v1.region.cph_region import CphRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcph.v1 import *

if __name__ == "__main__":
    # 加载 .env 文件中的环境变量
    load_dotenv()

    # 从环境变量中获取 Access_Key 和 Secret_Key
    ak = os.getenv('CLOUD_SDK_AK')
    sk = os.getenv('CLOUD_SDK_SK')

    # 检查 AK 和 SK 是否获取成功
    if not ak or not sk:
        print("请确保在 .env 文件中设置 Access_Key 和 Secret_Key的环境变量")
        exit(1)

    # 创建认证信息
    credentials = BasicCredentials(ak, sk)

    # 创建云手机客户端并设置区域
    client = CphClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(CphRegion.value_of("cn-southwest-2")) \
        .build()

    try:
        # 构造查询云手机的请求
        request = ListCloudPhonesRequest()
        request.limit = 200
        response = client.list_cloud_phones(request)

        # 将响应转换为字典格式
        phone_list = response.to_dict()

        # 将云手机列表保存到文件中
        with open("cloud_phones_list.json", "w", encoding="utf-8") as file:
            json.dump(phone_list, file, ensure_ascii=False, indent=4)

        print("云手机列表已成功保存到 cloud_phones_list.json 文件中")

    except exceptions.ClientRequestException as e:
        # 打印错误信息
        print(f"Status Code: {e.status_code}")
        print(f"Request ID: {e.request_id}")
        print(f"Error Code: {e.error_code}")
        print(f"Error Message: {e.error_msg}")
