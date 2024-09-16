# coding: utf-8

import os
import json
from dotenv import load_dotenv
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcph.v1.region.cph_region import CphRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcph.v1 import *

if __name__ == "__main__":

    load_dotenv()

    # 从环境变量中获取 CLOUD_SDK_AK 和 CLOUD_SDK_SK
    ak = os.getenv('CLOUD_SDK_AK')
    sk = os.getenv('CLOUD_SDK_SK')

    # 检查 AK 和 SK 是否获取成功
    if not ak or not sk:
        print("请确保在 .env 文件中设置 CLOUD_SDK_AK 和 CLOUD_SDK_SK的环境变量")
        exit(1)

    credentials = BasicCredentials(ak, sk)

    client = CphClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(CphRegion.value_of("cn-southwest-2")) \
        .build()

    try:
        # Load server IDs and phone IDs from cloud_phones_list.json
        with open("cloud_phones_list.json", "r") as file:
            phones_data = json.load(file)

        # Extract server_ids and phone_ids
        listServerIdsbody = [phone["server_id"] for phone in phones_data["phones"]]
        listPhoneIdsbody = [phone["phone_id"] for phone in phones_data["phones"]]

        # Load APK paths from environment variable
        apk_paths = os.getenv('obs_apk_paths').split(',')

        # Prepare the request for each APK
        for apk_path in apk_paths:
            request = InstallApkRequest()
            request.body = InstallApkRequestBody(
                server_ids=listServerIdsbody,
                phone_ids=listPhoneIdsbody,
                content=apk_path,
                command="install"
            )
            
            # Print installation message
            print(f"正在安装 {apk_path} 到手机中，请稍等...")

            # Send the request
            response = client.install_apk(request)
            
            # Check response and print success message
            if response and hasattr(response, 'jobs'):
                print(f"{apk_path} 安装成功！")
                # print("任务信息：")
                # for job in response.jobs:
                #     print(f"phone_id: {job.phone_id},   jod_id: {job.job_id}")
                print("所有任务均已成功执行，稍等几分钟后即可在手机上检查")
            else:
                print(f"{apk_path} 安装失败，未找到任务信息。")

    except exceptions.ClientRequestException as e:
        print("安装请求失败:")
        print(f"状态码: {e.status_code}")
        print(f"请求 ID: {e.request_id}")
        print(f"错误代码: {e.error_code}")
        print(f"错误信息: {e.error_msg}")
    except FileNotFoundError:
        print("文件 'cloud_phones_list.json' 未找到。")
    except json.JSONDecodeError:
        print("解码 'cloud_phones_list.json' 中的 JSON 时出错。")
    except KeyError as e:
        print(f"键错误: {e} - 请检查 JSON 文件的结构。")
    except Exception as e:
        print(f"发生意外错误: {e}")
