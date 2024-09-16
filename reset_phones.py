import requests
import json
import time
import datetime
import pandas
import random

def get_token():
    try:
        url = "https://iam.myhuaweicloud.com/v3/auth/tokens"
        auth ={
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "name": "laowang",
                            "domain": {
                                "name": "chenghejun"
                            },
                            "password": "lkwn36257?@"
                        }
                    }
                },
                "scope": {
                    "project": {
                        "name": "cn-southwest-2"
                    }
                }
            }
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url ,data=json.dumps(auth))
        result_headers = response.headers
        token = result_headers['X-Subject-Token']
        # print(token)
        return token
    except Exception as e:
        print(e)
        raise Exception("get_token failed :{}".format(e))

def search_util(url ,parameter ,rqtype ,token):
    try:
        if token == None:
            token = get_token()
        #print(token)
        # auth = HTTPBasicAuth("X-Auth-Token", token)
        headers = {"Content-Type": "application/json" ,"X-Auth-Token": token}
        response = {}
        if  parameter != None:
            if rqtype == "get":
                response = requests.get(url ,headers=headers ,data=json.dumps(parameter))
            if rqtype == "post" :
                #print(json.dumps(parameter))
                response = requests.post(url ,headers=headers ,data=json.dumps(parameter))
        if  parameter == None:
            if rqtype == "get":
                response = requests.get(url ,headers=headers)
            if rqtype == "post" :
                response = requests.post(url ,headers=headers)


        result = response.json()
        # print(result)
        return result
    except Exception as e:
        print(e)
        raise Exception("run  query failed")


# ssh -L 20000:10.237.0.43:5555 0a7472a0be80250b2f22c001a123b171@159.138.159.49 -i /root/hw-hk-phone-key.pem -Nf -o ServerAliveInterval=30
# airtest run  tets-phone.air --device Android:///127.0.0.1:20000

# vpn_evn()
# clear_google_evn()
# chrome_evn()
# superproxy_vpn_evn()

# google_play_evn()

# offer_redirect(offer_id="22667575",app_id="1286",type_name="5a720d4d0000001d",package_name="com.kingsgroup.sos",destroy_time=15)
url_servers = "https://cph.cn-southwest-2.myhuaweicloud.com/v1/e228b8e265a549e094a63d113f491437/cloud-phone/servers"
parameter   =  {"offset" :0 ,"limit" :10}
url_phones  = "https://cph.cn-southwest-2.myhuaweicloud.com/v1/e228b8e265a549e094a63d113f491437/cloud-phone/phones?offset=0&limit=3"

def bath_reset():
    url = "https://cph.cn-southwest-2.myhuaweicloud.com/v1/e228b8e265a549e094a63d113f491437/cloud-phone/phones/batch-reset"
    print("****************************开始批量重置云手机******************************")
    try:
        token = get_token()
        phones = search_util(url = url_phones ,parameter = None ,rqtype = "get",token = token)["phones"]
        #print(phones)
        reset_phones =[]
        for item in phones:
            #print(item)
            phone_id = item["phone_id"]
            phone_temp = {"phone_id": phone_id, "property": get_cloud_phone_property_v1()}
            reset_phones.append(phone_temp)


        headers = {"Content-Type": "application/json", "X-Auth-Token": token}
        phone_settings = {"image_id":"24070320240823e001100a2100000d98","phones": reset_phones}
        print(phone_settings)
        #1：下发改机指令
        response = search_util(url = url ,parameter = phone_settings ,rqtype = "post",token = token)
        print("*******************************")
        print(response)
        print("*******************************")
        request_id = response["request_id"]
        job_request_url = "https://cph.cn-southwest-2.myhuaweicloud.com/v1/e228b8e265a549e094a63d113f491437/cloud-phone/jobs?request_id="+request_id
        print(job_request_url)
        #2：检查job 状态
        while (True):
            time.sleep(5)
            bath_reset_response = search_util( url = job_request_url ,parameter = None ,rqtype = "get",token = token )
            print(bath_reset_response)
            bath_reset_status = bath_reset_response["jobs"]
            success_count = 0
            for status_tmp in bath_reset_status:
               # 1:表示运行中
               # 2:表示成功
               # -1:表示失败
                if status_tmp['status'] == 2:
                    success_count += 1
            print("phones: {}/{}   resetting ,will check jobs next 5 s ".format(success_count, len(bath_reset_status)))

            if success_count == len(bath_reset_status):
                print("all :{} phones reset done ".format(success_count))
                break
        print("*************************所有云手机已重置完成******************************")
        # 3：检查手机状态，
        while (True):
            time.sleep(5)
            phones = search_util(url=url_phones, parameter=None, rqtype="get", token=token)["phones"]
            #print(phones)
            phone_run_status_count = 0
            for phone_temp in phones:
                #print(phone_temp)
                # 1:表示运行中
                # 2:表示成功
                # -1:表示失败
                if phone_temp['status'] == 2:
                    phone_run_status_count += 1
            print("phones: {}/{}   running ,will check phone status next 5 s ".format(phone_run_status_count,
                                                                                len(phones)))

            if phone_run_status_count == len(phones):
                print("all :{} phones running  ".format(phone_run_status_count))
                break

        return True
    except Exception as e:
        print(e)
        raise Exception("reset phone error")


# search_util(url_phones,parameter)

#bath_reset()
# phones = search_util(url_phones,parameter,None)["phones"]
# print(phones)

def get_cloud_phone_property():

    properties = ""
    index = random.randint(1, 490)
    df = pandas.read_csv("phones-sample.csv",skiprows=index,nrows=1,header=None,names=['device_brand_name','device_type_name','os_ver_name'])

    print(df)
    for row in df.index:
       print(row)
       #iloc[:3]
       phone_brand = df.iloc[row]['device_brand_name']
       phone_type =  df.iloc[row]['device_type_name']
       os_version =  df.iloc[row]['os_ver_name']
       wifi_name = "wifi-"+str(random.randint(1,10000))
       #google_adv_id = row["google_adv_id"]
       properties = "{\"phone_brand\":\""+str(phone_brand)+"\",\"phone_type\":\""+str(phone_type)+"\"," \
                    "\"os_version\":\""+str(os_version)+"\",\"wifi_name\":\"wifi-"+str(wifi_name)+"\"," \
                    "\"build_id\":\"N2G47H\",\"gsm_country\":\"a\"," \
                    "\"gsm_number\":\"0\",\"gsm_operator\":\"a\"," \
                    "\"sim_country\":\"a\",\"sim_number\":\"0\"," \
                    "\"sim_operator\":\"a\",\"ro.product.board\":\"msm8937\"," \
                    "\"ro.product.manufacturer\":\"Xiaomi\",\"ro.product.name\":\"rolex\"," \
                    "\"ro.board.platform\":\"msm8937\",\"ro.permission.changed\":\"1\"," \
                    "\"ro.build.product\":\"rolex\",\"persist.sys.locale\":\"en-IN\"," \
                    "\"ro.product.device\":\"rolex\",\"ro.bootimage.build.fingerprint\":\"Xiaomi/rolex/rolex:7.1.2/N2G47H/V10.2.1.0.NCCMIXM:user/release-keys\"," \
                    "\"ro.build.fingerprint\":\"Xiaomi/rolex/rolex:7.1.2/N2G47H/V10.2.1.0.NCCMIXM:user/release-keys\",\"ro.build.host\":\"mi-server\"," \
                    "\"ro.build.user\":\"builder\",\"ro.build.version.incremental\":\"V10.2.1.0.NCCMIXM\"," \
                    "\"ro.bootloader\":\"unknown\",\"ro.build.date.utc\":\"1230739303\"," \
                    "\"ro.build.description\":\"rolex-user 7.1.2 N2G47H V10.2.1.0.NCCMIXM release-keys\"," \
                    "\"ro.build.version.release\":\"7.1.2\",\"ro.hardware\":\"qcom\",\"ro.build.display.id\":\"N2G47H\"," \
                    "\"ro.build.flavor\":\"rolex-user\",\"ro.product.locale\":\"en-GB\"," \
                    "\"com.cph.sensor.vendor\":\"bcom\",\"com.cph.system.app.install_time\":\"1230739475\"," \
                    "\"gsm.sim.state\":\"NOT_READY\",\"ro.build.id\":\"N2G47H\",\"ro.baseband\":\"msm\"," \
                    "\"ro.hardware.gpurenderer\":\"Adreno (TM) 418\",\"gsm.version.baseband\":\"\"}"\
           #.format("phone_brand","phone_type","os_version","wifi_name")
       return properties

def get_device_info(index):
    i = 1
    with open("devices.json", 'r') as f:
        for line in f.readlines():
            if i == index:
                #print(eval(line))
                return eval(line)
            i += 1

def check_null(device_detail,key):
    try:
        if key in device_detail:
            return device_detail[key]
        else:
            return ""
    except Exception as e:
        return ""
        #raise Exception("reset phone error")


def get_cloud_phone_property_v1():
    try:
        index = random.randint(1, 9999)
        device_detail = get_device_info(index)
        bottom_height = check_null(device_detail, "bottom_height")
        create_time = check_null(device_detail, "create_time")
        device_name = check_null(device_detail, "device_name")
        dpi = check_null(device_detail,"dpi")
        gaid = check_null(device_detail,"gaid")
        id = check_null(device_detail,"id")
        imei = check_null(device_detail,"imei")
        non_name = check_null(device_detail,"non_name")
        ro_bootimage_build_date_utc = check_null(device_detail,"ro.bootimage.build.date.utc")
        ro_build_description = check_null(device_detail,"ro.build.description")
        ro_build_fingerprint = check_null(device_detail,"ro.build.fingerprint")
        ro_build_host = check_null(device_detail,"ro.build.host")
        ro_build_id = check_null(device_detail,"ro.build.id")
        ro_build_product = check_null(device_detail,"ro.build.product")
        ro_build_tags = check_null(device_detail,"ro.build.tags")
        ro_build_type = check_null(device_detail,"ro.build.type")
        ro_build_user = check_null(device_detail,"ro.build.user")
        ro_build_version_all_codenames = check_null(device_detail,"ro.build.version.all_codenames")
        ro_build_version_codename = check_null(device_detail,"ro.build.version.codename")
        ro_build_version_incremental = check_null(device_detail,"ro.build.version.incremental")
        ro_build_version_release = check_null(device_detail,"ro.build.version.release")
        ro_build_version_sdk = check_null(device_detail,"ro.build.version.sdk")
        ro_product_board = check_null(device_detail,"ro.product.board")
        ro_product_brand = check_null(device_detail,"ro.product.brand")
        ro_product_cpu_abi = check_null(device_detail,"ro.product.cpu.abi")
        ro_product_cpu_abilist = check_null(device_detail,"ro.product.cpu.abilist")
        ro_product_cpu_abilist32 = check_null(device_detail,"ro.product.cpu.abilist32")
        ro_product_cpu_abilist64 = check_null(device_detail,"ro.product.cpu.abilist64")
        ro_product_device = check_null(device_detail,"ro.product.device")
        ro_product_manufacturer = check_null(device_detail,"ro.product.manufacturer")
        ro_product_model = check_null(device_detail,"ro.product.model")
        ro_product_name = check_null(device_detail,"ro.product.name")
        ro_serialno = check_null(device_detail,"ro.serialno")
        ro_sf_lcd_density = check_null(device_detail,"ro.sf.lcd_density")
        screen_height = check_null(device_detail,"screen_height")
        screen_width = check_null(device_detail,"screen_width")
        top_height = check_null(device_detail,"top_height")
        total_df = check_null(device_detail,"total_df")
        total_m = check_null(device_detail,"total_m")
        user_agent = check_null(device_detail,"user_agent")
        wifi_mac = check_null(device_detail,"wifi_mac")
        ro_bootloader = check_null(device_detail, "ro.bootloader")

        properties = {}

       #设备字段梳理说明
        # 修改ro.build.date.utc值，会自动同步修改ro.bootimage.build.date.utc
        if ro_bootimage_build_date_utc != "":
           properties["ro.build.date.utc"] = ro_bootimage_build_date_utc
        if ro_product_model != "":
           properties["ro.product.model"] = ro_product_model
        if ro_product_brand != "":
           properties["ro.product.brand"] = ro_product_brand
        if ro_sf_lcd_density != "":
           properties["ro.hardware.dpi"] = ro_sf_lcd_density
        if ro_serialno != "":
           properties["ro.serialno"] = ro_serialno
        # screen_width[重要]
        if screen_width != "":
           properties["ro.hardware.width"] = screen_width
        # screen_height[重要]
        if screen_height != "":
           properties["ro.hardware.height"] = screen_height
        if wifi_mac != "":
           properties["ro.com.cph.mac_address"] = wifi_mac
        if imei != "":
           properties["sys.prop.writeimei"] = imei
        if ro_bootloader != "":
           properties["ro.bootloader"] = ro_bootloader
        if ro_build_description != "":
           properties["ro.build.description"] = ro_build_description
        if ro_build_fingerprint != "":
           properties["ro.build.fingerprint"] = ro_build_fingerprint
        if ro_build_host != "":
           properties["ro.build.host"] = ro_build_host
        if ro_build_id != "":
           properties["ro.build.id"] = ro_build_id
        if ro_build_product != "":
           properties["ro.build.product"] = ro_build_product
        if ro_build_user != "":
           properties["ro.build.user"] = ro_build_user
        if ro_build_version_incremental != "":
           properties["ro.build.version.incremental"] = ro_build_version_incremental
        if ro_build_version_release != "":
           properties["ro.build.version.release"] = ro_build_version_release
        if ro_product_manufacturer != "":
           properties["ro.product.manufacturer"] = ro_product_manufacturer
        if ro_product_name != "":
           properties["ro.product.name"] = ro_product_name
        if ro_product_board != "":
           properties["ro.product.board"] = ro_product_board
        if ro_product_device != "":
           properties["ro.product.device"] = ro_product_device

       #华为 API 不支持
       #properties["ro.build.tags"] = ro_build_tags
       #properties["ro.build.type"] = ro_build_type
       #properties["ro.build.version.all_codenames"] = ro_build_version_all_codenames
       #properties["ro.build.version.codename"] = ro_build_version_codename
       #properties["ro.build.version.sdk"] = ro_build_version_sdk
       #properties["ro.product.cpu.abi"] = ro_product_cpu_abi
       #properties["ro.product.cpu.abilist"] = ro_product_cpu_abilist
       #properties["ro.product.cpu.abilist32"] = ro_product_cpu_abilist32 [重要]
       #properties["ro.product.cpu.abilist642"] = ro_product_cpu_abilist64 [重要]
       #properties["ro.sf.lcd_density"] = ro_sf_lcd_density [重要]
       #修改ro.hardware.dpi，会自动修改ro.sf.lcd_density
       #dpi[重要]
       #bottom_height[重要]
       #top_height[重要]
       # gaid[重要]
       #total_m[重要]
       #total_df[重要]
       #OAID，Android 10 上支持
       #device_name[重要]
       #user_agent[重要]
       #android_id[重要]
       # bluetooth_address
       # non_name
       #真机库没有
       # bluetooth_name

        properties_str = json.dumps(properties)
        #properties_encode = json.dumps(properties_str)
        return properties_str
    except Exception as e:
        return ""




if __name__ == '__main__':
    #print(get_cloud_phone_property_v1())
    bath_reset()
    #url_phones = "https://cph.ap-southeast-1.myhuaweicloud.com/v1/0a7472a0be80250b2f22c001a123b171/cloud-phone/phones?offset=0&limit=20"
    #token = get_token()
    #phones = search_util(url=url_phones, parameter=None, rqtype="get", token=token)["phones"]
    #print(phones)
    #print("all cloud phone reset done")
