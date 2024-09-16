# coding: utf-8

import os
import json
from dotenv import load_dotenv
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcph.v1.region.cph_region import CphRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcph.v1 import *
from colorama import init, Fore

init(autoreset=True)

if __name__ == "__main__":
    # 加载 .env 文件中的环境变量
    load_dotenv()

    ak = os.getenv("CLOUD_SDK_AK")
    sk = os.getenv("CLOUD_SDK_SK")

    credentials = BasicCredentials(ak, sk)

    client = CphClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(CphRegion.value_of("cn-southwest-2")) \
        .build()

    # 读取 cloud_phones_list.json 文件
    with open('cloud_phones_list.json', 'r') as f:
        data = json.load(f)
    
    phone_ids = [phone['phone_id'] for phone in data['phones']]

    print(Fore.YELLOW + "开始批量修改云手机属性")

    # 修改云手机属性 
    for phone_id in phone_ids:
        try:
            request = UpdateCloudPhonePropertyRequest()
            listPhonesbody = [
                ModelProperty(
                    phone_id=phone_id,
                    _property='{"ro.permission.changed":"1","ro.install.auto":"1","ro.com.cph.non_root":"0","ro.com.cph.notification_disable":"1"}'
                )
            ]
            request.body = UpdateCloudPhonePropertyRequestBody(
                phones=listPhonesbody
            )
            response = client.update_cloud_phone_property(request)
            print(Fore.GREEN + f"完成修改云手机属性  Phone ID: {phone_id}")
            # print(response)
        except exceptions.ClientRequestException as e:
            print(Fore.RED + f"修改云手机属性失败: {phone_id}")
            print(Fore.RED + str(e.status_code))
            print(Fore.RED + e.request_id)
            print(Fore.RED + e.error_code)
            print(Fore.RED + e.error_msg)